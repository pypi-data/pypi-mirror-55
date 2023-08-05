import datetime
import json
import logging
import lzma
import os
import struct

import numpy
from PySide import QtGui, QtCore

from . import util
from ..info_dialog import InfoDialog

logger = logging.getLogger(__name__)


def get_save_file(default_name, parent=None):
    settings = QtCore.QSettings()

    # find the directory from settings
    directory = settings.value("fileSaveDirectory")
    if directory and type(directory) == str:
        if not os.path.isdir(directory):
            directory = None

    if not directory:
        directory = ""

    file_and_dir = os.path.join(directory, default_name)

    # ask the user for the file name
    caption = "Save File"
    file_filter = "Comma Seperated Value Files (*.csv);;All Files (*.*)"
    val = QtGui.QFileDialog.getSaveFileName(parent, caption, file_and_dir,
                                            file_filter)
    output_path = val[0]

    if output_path:
        # save the directory
        output_dir = os.path.dirname(output_path)
        settings.setValue("fileSaveDirectory", output_dir)
        return output_path
    else:
        return None


def file_information(parent=None):
    ret = util.load_single_file(parent)
    if ret is None:
        return  # error message displayed, or user cancelled
    _file_infos, header = ret

    dialog = InfoDialog(header)
    dialog.exec_()


def raw_export(parent=None):
    filename = util.get_packdata_file(parent)
    if filename is None:
        return  # user cancelled

    try:
        # open the compressed file, and figure out how many bytes it has
        rawfile = open(filename, 'rb')
        rawfile.seek(0, os.SEEK_END)
        rawlen = rawfile.tell()
        rawfile.seek(0, os.SEEK_SET)

        # open the LZMA wrapper object
        lzmafile = lzma.LZMAFile(rawfile, "rb")

        # read the header
        header_leader = struct.unpack(">dI", lzmafile.read(12))
        header_bytes = lzmafile.read(header_leader[1])

        if len(header_bytes) == 0:
            message = "Empty header in {}!".format(filename)
            logger.error(message)
            QtGui.QMessageBox.critical(parent, "Error", message)
            return  # error

        try:
            header_str = header_bytes.decode("UTF-8")
            header = json.loads(header_str)
        except:
            message = "Could not parse file header!"
            logger.exception(message)
            QtGui.QMessageBox.critical(parent, "Error", message)
            return
    except:
        message = "Could not open file {}!".format(filename)
        logger.exception(message)
        QtGui.QMessageBox.critical(parent, "Error", message)
        return  # error

    # ask the user for the json file name
    default_json_filename = os.path.splitext(filename)[0] + ".json"
    caption = "Save JSON File"
    json_file_filter = "JSON Files (*.json);;All Files (*.*)"
    val = QtGui.QFileDialog.getSaveFileName(
        parent, caption, default_json_filename, json_file_filter)
    json_filename = val[0]

    if json_filename:
        with open(json_filename, 'wt') as f:
            json.dump(header, f, sort_keys=True, indent=4)

    # ask the user for the packet file name
    default_packet_filename = os.path.splitext(filename)[0] + ".packet"
    caption = "Save Packet File"
    packet_file_filter = "Packet Files (*.packet);;All Files (*.*)"
    val = QtGui.QFileDialog.getSaveFileName(
        parent, caption, default_packet_filename, packet_file_filter)
    packet_filename = val[0]

    if not packet_filename:
        # user didn't want to save a packet file, just exit now
        return

    packet_file = open(packet_filename, 'wt')

    packet_leader = struct.Struct(">dI")
    stream_packet_length = header['stream_packet_length']

    # create a progress dialog box
    window_flags = (QtCore.Qt.MSWindowsFixedSizeDialogHint)
    progress = QtGui.QProgressDialog("Loading Data...", "Abort", 0,
                                     rawlen, parent, window_flags)
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.forceShow()

    # make sure it gets at least one value different than rawlen
    progress.setValue(0)

    process_countdown = 0

    try:
        while True:
            leader_bytes = lzmafile.read(packet_leader.size)

            if not leader_bytes:
                break  # file is finished

            leader = packet_leader.unpack(leader_bytes)
            packet_timestamp = leader[0]
            packet_bytes = lzmafile.read(leader[1])

            packet_dt = datetime.datetime.fromtimestamp(packet_timestamp,
                                                        datetime.timezone.utc)
            packet_time_string = "{} ".format(
                packet_dt.strftime('%Y-%m-%dT%H:%M:%S.%f'))

            for i in range(len(packet_bytes) // stream_packet_length):
                start = i * stream_packet_length
                packet = packet_bytes[start:start + stream_packet_length]
                packet_string = ", ".join(map("0x{:02x}".format, packet))

                packet_file.write(packet_time_string)
                packet_file.write('[' + packet_string + ']\n')

            progress.setValue(rawfile.tell())

            # update the window periodically
            if process_countdown == 0:
                process_countdown = 100
                QtCore.QCoreApplication.processEvents()
            else:
                process_countdown -= 1

            # abort if required
            if progress.wasCanceled():
                return  # user cancelled
    except:
        progress.cancel()
        m = "Error while processing data in file {}!".format(filename)
        logger.exception(m)
        QtGui.QMessageBox.critical(parent, "Error", m)
        return

    logger.debug("Finished reading {}.".format(filename))
