import logging

from PySide import QtGui, QtCore

from .ui_tcp_connect_dialog import Ui_TCPConnectDialog

logger = logging.getLogger(__name__)


class TCPConnectDialog(QtGui.QDialog, Ui_TCPConnectDialog):
    def __init__(self, devices, connected_location_strs, rescan_func,
                 parent=None):
        super().__init__(parent)

        self.connected_location_strs = connected_location_strs
        self.rescan_func = rescan_func

        self.device_by_row = []

        self.setupUi(self)
        self.extra_ui_setup()

        self.tableWidget.itemSelectionChanged.connect(self.selection_changed)

        self.add_device_rows(devices)
        self.selection_changed()

    def extra_ui_setup(self):
        header = self.tableWidget.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.ResizeToContents)

        self.rescanButton = self.buttonBox.button(QtGui.QDialogButtonBox.Reset)
        self.rescanButton.setText(self.tr("Rescan"))
        self.rescanButton.clicked.connect(self.rescan)

        self.tableWidget.cellDoubleClicked.connect(self.double_click_cb)
        self.tableWidget.itemDoubleClicked.connect(self.double_click_cb)

    def double_click_cb(self, row=None, column=None):
        self.accept()

    def sort_devices(self, all_devices):
        def key_func(t):
            device, _connected_bool = t
            adv = device.tcp_get_advertisement()
            return (adv.connected, adv.serial_number)
        return sorted(all_devices, key=key_func)

    def add_device_row(self, device, connected):
        # add a blank row
        row_index = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_index)
        self.device_by_row.append(device)

        adv = device.tcp_get_advertisement()

        if connected:
            item_flags = QtCore.Qt.NoItemFlags
            available_str = "No (tab already open)"
        elif adv.connected:
            item_flags = QtCore.Qt.NoItemFlags
            available_str = "No (in use)"
        else:
            item_flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
            available_str = "Yes"

        serial_number_item = QtGui.QTableWidgetItem(adv.serial_number)
        serial_number_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 0, serial_number_item)

        user_tag1_item = QtGui.QTableWidgetItem(adv.user_tag1)
        user_tag1_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 1, user_tag1_item)

        user_tag2_item = QtGui.QTableWidgetItem(adv.user_tag2)
        user_tag2_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 2, user_tag2_item)

        board_info_str = "{} rev {}".format(adv.board_type, adv.board_rev)
        board_info_item = QtGui.QTableWidgetItem(board_info_str)
        board_info_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 3, board_info_item)

        build_info_item = QtGui.QTableWidgetItem(adv.build_info)
        build_info_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 4, build_info_item)

        build_date_item = QtGui.QTableWidgetItem(adv.build_date)
        build_date_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 5, build_date_item)

        available_item = QtGui.QTableWidgetItem(available_str)
        available_item.setFlags(item_flags)
        self.tableWidget.setItem(row_index, 6, available_item)

    def add_device_rows(self, devices):
        all_devices = []
        for device in devices:
            location_str = device.get_location_string()
            connected_bool = location_str in self.connected_location_strs
            all_devices.append((device, connected_bool))

        for device, connected_bool in self.sort_devices(all_devices):
            self.add_device_row(device, connected_bool)

    def get_selected_devices(self):
        selected_devices = []
        for index in self.tableWidget.selectionModel().selectedRows():
            selected_devices.append(self.device_by_row[index.row()])
        return selected_devices

    def selection_changed(self):
        ok_button = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        if self.tableWidget.selectionModel().hasSelection():
            ok_button.setEnabled(True)
        else:
            ok_button.setEnabled(False)

    def rescan(self):
        self.rescanButton.setEnabled(False)

        # clear the existing devices
        self.tableWidget.setRowCount(0)
        self.device_by_row.clear()

        # update the UI one last time before doing the scan
        QtCore.QCoreApplication.processEvents()

        new_devices = self.rescan_func()
        self.add_device_rows(new_devices)
        self.selection_changed()

        self.rescanButton.setEnabled(True)
