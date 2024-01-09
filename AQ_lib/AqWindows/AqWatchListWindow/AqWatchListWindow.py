import csv
import os

from PySide6.QtCore import Qt, QSettings, QModelIndex
from PySide6.QtGui import QScreen, QStandardItem
from PySide6.QtWidgets import QWidget, QFrame, QTableWidget, QDialog, QTableWidgetItem, QLineEdit, QFileDialog

import ModbusTableDataFiller
from AqBaseDevice import AqBaseDevice
from AqBaseTreeItems import AqParamManagerItem, AqCatalogItem
from AqCustomDialogWindow import QDialog, loadDialogJsonStyle
from AqTreeView import AqTreeView
from AqWatchListCore import AqWatchListCore
from AqWatchListTreeViewModel import AqWatchListTreeViewModel
from AqWatchedItem import WatchedItem
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

        self.tree_model_for_view = AqWatchListTreeViewModel()
        self.ui.treeView.setModel(self.tree_model_for_view)

        AqWatchListCore.signals.watch_item_change.connect(self.add_new_parameter)
        AqWatchListCore.signals.watch_item_remove.connect(self.remove_parameter)

        AqWatchListWidget._inited = True

    def customAdjustSize(self, *args):
        self.ui.tableView.adjustSize()
        self.adjustSize()
        super().adjustSize()

    def add_new_parameter(self, watchItem: WatchedItem):
        # last_row = None
        row_count = self.tree_model_for_view.invisibleRootItem().rowCount()
        for row in range(row_count):
            # Якщо такий вотч-ітем вже додано до вікна, то видаляємо його стару версію з моделі
            child_item = self.tree_model_for_view.invisibleRootItem().child(row)
            if child_item.watchItem == watchItem:
                index = self.tree_model_for_view.indexFromItem(child_item)
                # last_row = index.row()
                self.tree_model_for_view.removeRow(index.row())
                break

        watch_catalog_item = AqWatchListCatalogItem(watchItem)

        for item in watchItem.items:
            watch_catalog_item.appendRow(self.create_new_row_for_tree_view(item))

        root = self.tree_model_for_view.invisibleRootItem()
        # if last_row is None:
        root.appendRow(watch_catalog_item)
        # else:
        #     root.insertRow(last_row, watch_catalog_item)

        self.ui.treeView.setModel(self.tree_model_for_view)
        self.ui.treeView.setExpanded(self.tree_model_for_view.indexFromItem(watch_catalog_item), True)

    def remove_parameter(self, watchItem: WatchedItem):
        row_count = self.tree_model_for_view.invisibleRootItem().rowCount()
        for row in range(row_count):
            # Якщо такий вотч-ітем вже додано до вікна, то видаляємо його стару версію з моделі
            child_item = self.tree_model_for_view.invisibleRootItem().child(row)
            if child_item.watchItem == watchItem:
                index = self.tree_model_for_view.indexFromItem(child_item)
                self.tree_model_for_view.removeRow(index.row())
                break

    def create_new_row_for_tree_view(self, item):
        parameter_attributes = item.data(Qt.UserRole)
        name = parameter_attributes.get('name', 'err_name')

        parameter_item = AqParamManagerItem(item)
        parameter_item.setData(parameter_attributes, Qt.UserRole)
        value_item = QStandardItem()
        parameter_item.setFlags(parameter_item.flags() & ~Qt.ItemIsEditable)
        value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)

        return [parameter_item, value_item]


class AqWatchParamManagerItem(AqParamManagerItem):
    def __init__(self, sourse_item):
        super().__init__(sourse_item)


class AqWatchListCatalogItem(AqParamManagerItem):
    def __init__(self, watchItem):
        self._watchItem = watchItem
        param_attributes = dict()
        param_attributes['name'] = watchItem.device.name
        param_attributes['R_Only'] = 0
        param_attributes['W_Only'] = 0
        param_attributes['is_catalog'] = 1
        fake_sourse_item = AqCatalogItem(param_attributes)
        super().__init__(fake_sourse_item)
        self.setData(param_attributes, Qt.UserRole)

    @property
    def watchItem(self):
        return self._watchItem
