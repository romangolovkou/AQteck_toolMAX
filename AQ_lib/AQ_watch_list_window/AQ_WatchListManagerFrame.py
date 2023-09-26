import csv
import os

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QStandardItem, QFont, QStandardItemModel, QColor
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTableView, QLineEdit

from AQ_CustomTreeItems import AQ_ParamManagerItem
from AQ_CustomWindowTemplates import AQ_Label
from AQ_ParamListTableView import AQ_ParamListTableView, AQ_ParamListInfoTableView
from AQ_ParamListTableViewItemModel import AQ_TableViewItemModel
from AQ_SettingsFunc import get_last_path, save_last_path
from AQ_WatchListTableView import AQ_WatchListTableView
from AQ_WatchListTableViewItemModel import AQ_WatchListTableViewItemModel


class AQ_WatchListManagerFrame(QFrame):
    def __init__(self, event_manager, parent=None):
        super().__init__(parent)
        self.event_manager = event_manager
        self.parent = parent
        self.setStyleSheet("background-color: transparent;")

        self.event_manager.register_event_handler('add_item_to_watch_list', self.add_new_parameter)

        # Створюємо нову модель для відображення параметрів
        self.watch_list_table_model = AQ_WatchListTableViewItemModel(self.event_manager, self)

        # Створюємо головний лейаут
        self.watch_list_layout = AQ_WatchListLayout(self.watch_list_table_model, self.event_manager, self)

    def add_new_parameter(self, item, model):
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

        param_item = AQ_WatchParamManagerItem(item.get_sourse_item(), device, model)

        value_item = QStandardItem()
        device_item = QStandardItem()

        value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)
        device_item.setFlags(device_item.flags() & ~Qt.ItemIsEditable)

        return [param_item, value_item, device_item]


class AQ_WatchListLayout(QVBoxLayout):
    def __init__(self, watch_table_model, event_manager, parent):
        super().__init__(parent)

        self.parent = parent
        self.event_manager = event_manager
        self.watch_table_model = watch_table_model
        self.setContentsMargins(5, 5, 5, 5)  # Устанавливаем отступы макета
        self.setAlignment(Qt.AlignTop)  # Установка выравнивания вверху макета

    # Створюємо таблицю з параметрами
        self.watch_table_view = AQ_WatchListTableView(self.watch_table_model, parent)

    # Додаємо всі створені віджети в порядку відображення
        self.addWidget(self.watch_table_view)


class AQ_WatchParamManagerItem(AQ_ParamManagerItem):
    def __init__(self, sourse_item, device, tree_view_model=None):
        param_attributes = sourse_item.data(Qt.UserRole)
        super().__init__(sourse_item)
        self.sourse_item = sourse_item
        self.device = device
        self.tree_view_model = tree_view_model
        self.editor_object = None
        self.param_status = 'ok'
        self.setData(self.param_status, Qt.UserRole + 1)

