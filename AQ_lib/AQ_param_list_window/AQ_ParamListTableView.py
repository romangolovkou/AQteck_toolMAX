from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QTableView, QHeaderView, QAbstractItemView

from AQ_ParamListTableViewItemModel import AQ_TableViewItemModel


class AQ_ParamListTableView(QTableView):
    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.setModel(model)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        self.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.setStyleSheet("""QTableView {color: #D0D0D0;}
                           QTableView::item { padding-left: 3px; }""")
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)


class AQ_ParamListInfoTableView(QTableView):
    def __init__(self, device, parent=None):
        super().__init__(parent)

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        # self.horizontalHeader().setStyleSheet(
        #     "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("""QTableView {border: none; color: #D0D0D0;}
                           QTableView::item { padding-left: 3px; }
                           QTableView:item:!focus { background-color: transparent; color: #D0D0D0}""")
        self.setShowGrid(False)
        # self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
        self.setModel(self.create_info_list_for_view(device))
        row_height = 25
        row_count = self.model().rowCount()
        for i in range(row_count):
            self.setRowHeight(i, row_height)
        self.setFixedHeight(row_height * row_count)



    def create_info_list_for_view(self, device):
        device_data = device.get_device_data()
        network_info_list = device_data.get('network_info', None)
        if network_info_list is not None:
            info_table_model_for_view = QStandardItemModel()
            info_table_model_for_view.setColumnCount(1)
            new_root_item = info_table_model_for_view.invisibleRootItem()
            for i in range(len(network_info_list)):
                item_row = QStandardItem(network_info_list[i])
                item_row.setFlags(item_row.flags() & ~Qt.ItemIsEditable)
                new_root_item.appendRow(item_row)

            return info_table_model_for_view
