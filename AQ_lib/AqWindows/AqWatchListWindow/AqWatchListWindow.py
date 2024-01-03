import csv
import os

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QScreen, QStandardItem
from PySide6.QtWidgets import QWidget, QFrame, QTableWidget, QDialog, QTableWidgetItem, QLineEdit, QFileDialog

import ModbusTableDataFiller
from AqBaseTreeItems import AqParamManagerItem
from AqCustomDialogWindow import QDialog, loadDialogJsonStyle
from AqWatchListCore import AqWatchListCore
from AqWatchListTableViewModel import AqWatchListTableViewModel
from AqWindowTemplate import AqDialogTemplate
from AqSettingsFunc import get_last_path, save_last_path
from DeviceModels import AqDeviceParamListModel


class AqWatchListWidget(AqDialogTemplate):
    _instances = None
    _inited = False

    def __new__(cls, *args, **kwargs):
        if cls._instances is not None:
            return cls._instances
        else:
            cls._instances = super().__new__(cls, *args, **kwargs)
            return cls._instances

    def __init__(self, _ui, parent=None):
        if AqWatchListWidget._inited is True:
            return
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.maximizeBtnEnable = False
        self.resizeFrameEnable = [True, 5]

        self.name = 'Watch list'

        self.watch_list_table_model = AqWatchListTableViewModel()

        AqWatchListCore.signals.watch_item_add.connect(self.add_new_parameter)

        AqWatchListWidget._inited = True
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # loadDialogJsonStyle(self, self.ui)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)


        # self.ui.saveBtn.clicked.connect(self.saveToFile)
        #
        # self.device_str = ''.join((dev_info.name, ' S/N: ', dev_info.serial))
        # self.ui.deviceInfoLabel.setText(self.device_str)
        #
        # self.ui.tableView.clear()
        # self.ui.tableView.fillModbusData(dev_info.param_list)
        # self.ui.infoFrame.setData(dev_info.network_info)
        #
        # self.ui.tableView.horizontalHeader().sectionResized.connect(self.customAdjustSize)
        # self.customAdjustSize()

    def customAdjustSize(self, *args):
        self.ui.tableView.adjustSize()
        self.adjustSize()
        super().adjustSize()

    def add_new_parameter(self, item):

        parameter_attributes = item.data(Qt.UserRole)
        if parameter_attributes is not None:
            if parameter_attributes.get('is_catalog', 0) == 1:
                for row in range(item.rowCount()):
                    child_item = item.child(row)
                    self.add_new_parameter(child_item, model)
            else:
                root = self.watch_list_table_model.invisibleRootItem()
                root.appendRow(self.create_new_row_for_table_view(item, model))

    def create_new_row_for_table_view(self, item, model):
        parameter_attributes = item.data(Qt.UserRole)
        device = model.device
        device_data = device.get_device_data()

        param_item = AqWatchParamManagerItem(item.get_sourse_item(), device, model)

        value_item = QStandardItem()
        device_item = QStandardItem()

        value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)
        device_item.setFlags(device_item.flags() & ~Qt.ItemIsEditable)

        return [param_item, value_item, device_item]

class AqWatchParamManagerItem(AqParamManagerItem):
    def __init__(self, sourse_item, device, tree_view_model=None):
        param_attributes = sourse_item.data(Qt.UserRole)
        super().__init__(sourse_item)
        self.sourse_item = sourse_item
        self.device = device
        self.tree_view_model = tree_view_model
        self.editor_object = None
        self.param_status = 'ok'
        self.setData(self.param_status, Qt.UserRole + 1)
