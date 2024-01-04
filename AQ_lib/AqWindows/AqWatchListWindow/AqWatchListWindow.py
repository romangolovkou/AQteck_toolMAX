import csv
import os

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QScreen, QStandardItem
from PySide6.QtWidgets import QWidget, QFrame, QTableWidget, QDialog, QTableWidgetItem, QLineEdit, QFileDialog

import ModbusTableDataFiller
from AqBaseTreeItems import AqParamManagerItem
from AqCustomDialogWindow import QDialog, loadDialogJsonStyle
from AqTreeView import AqTreeView
from AqWatchListCore import AqWatchListCore
from AqWatchListTableViewModel import AqWatchListTableViewModel
from AqWatchListTreeViewModel import AqWatchListTreeViewModel
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

        # self.watch_list_table_model = AqWatchListTableViewModel()
        self.tree_model_for_view = AqWatchListTreeViewModel(self.event_manager)
        # self.ui.treeView = AqTreeView(self.ui.tableFrame)
        # self.ui.treeView.setGeometry(0, 0, 330, 240)#self.ui.tableFrame.width(), self.ui.tableFrame.height())
        self.ui.treeView.setModel(self.tree_model_for_view)

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

    def ex_add_new_parameter(self, item, model):

        parameter_attributes = item.data(Qt.UserRole)
        if parameter_attributes is not None:
            if parameter_attributes.get('is_catalog', 0) == 1:
                for row in range(item.rowCount()):
                    child_item = item.child(row)
                    self.add_new_parameter(child_item, model)
            else:
                root = self.watch_list_table_model.invisibleRootItem()
                root.appendRow(self.create_new_row_for_table_view(item, model))

    def add_new_parameter(self, watchItem):

        # parameter_attributes = item.data(Qt.UserRole)
        # if parameter_attributes is not None:
        #     if parameter_attributes.get('is_catalog', 0) == 1:
        #         for row in range(item.rowCount()):
        #             child_item = item.child(row)
        #             self.add_new_parameter(child_item, model)
        #     else:
        # watch_catalog_item = AqParamManagerItem(watchItem)
        watch_catalog_item = QStandardItem()
        root = self.tree_model_for_view.invisibleRootItem()
        for item in watchItem.items:
            watch_catalog_item.appendRow(self.create_new_row_for_tree_view(item))

        root.appendRow(watch_catalog_item)
        # size_view = self.ui.treeView.geometry()
        # size_view = self.ui.treeView.geometry()

    # def create_device_tree_for_view(self, device: AqBaseDevice):
    #     device_tree = device.device_tree
    #     if device_tree is not None:
    #         tree_model_for_view = AqTreeViewItemModel(device, self.event_manager)
    #         tree_model_for_view.setColumnCount(6)
    #         tree_model_for_view.setHorizontalHeaderLabels(
    #             ["Name", "Value", "Lower limit", "Upper limit", "Unit", "Default value"])
    #         donor_root_item = device_tree.invisibleRootItem()
    #         new_root_item = tree_model_for_view.invisibleRootItem()
    #         self.traverse_items_create_new_tree_for_view(donor_root_item, new_root_item)
    #         return tree_model_for_view

    # def traverse_items_create_new_tree_for_view(self, item, new_item):
    #     for row in range(item.rowCount()):
    #         child_item = item.child(row)
    #         if child_item is not None:
    #             parameter_attributes = child_item.data(Qt.UserRole)
    #             if parameter_attributes is not None:
    #                 if parameter_attributes.get('is_catalog', 0) == 1:
    #                     name = parameter_attributes.get('name', 'err_name')
    #                     catalog = AqParamManagerItem(child_item)
    #                     catalog.setData(parameter_attributes, Qt.UserRole)
    #                     catalog.setFlags(catalog.flags() & ~Qt.ItemIsEditable)
    #                     self.traverse_items_create_new_tree_for_view(child_item, catalog)
    #                     new_item.appendRow(catalog)
    #                 else:
    #                     new_item.appendRow(self.create_new_row_for_tree_view(child_item))

    def create_new_row_for_tree_view(self, item):
        parameter_attributes = item.data(Qt.UserRole)
        name = parameter_attributes.get('name', 'err_name')

        parameter_item = AqParamManagerItem(item)
        parameter_item.setData(parameter_attributes, Qt.UserRole)
        value_item = QStandardItem()
        # min_limit_item = self.get_min_limit_item(parameter_attributes)
        # max_limit_item = self.get_max_limit_item(parameter_attributes)
        # unit_item = self.get_unit_item(parameter_attributes)
        # default_item = self.get_default_value_item(parameter_attributes)
        # Встановлюємо флаг не редагуємого ітему, всім ітемам у строці окрім ітема value
        parameter_item.setFlags(parameter_item.flags() & ~Qt.ItemIsEditable)
        value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)
        # min_limit_item.setFlags(min_limit_item.flags() & ~Qt.ItemIsEditable)
        # max_limit_item.setFlags(max_limit_item.flags() & ~Qt.ItemIsEditable)
        # unit_item.setFlags(unit_item.flags() & ~Qt.ItemIsEditable)
        # default_item.setFlags(default_item.flags() & ~Qt.ItemIsEditable)

        return [parameter_item, value_item] #, min_limit_item, max_limit_item, unit_item, default_item]


class AqWatchParamManagerItem(AqParamManagerItem):
    def __init__(self, sourse_item):
        # param_attributes = sourse_item.data(Qt.UserRole)
        super().__init__(sourse_item)
        # self.sourse_item = sourse_item
        # self.editor_object = None
        # self.param_status = 'ok'
        # self.setData(self.param_status, Qt.UserRole + 1)
