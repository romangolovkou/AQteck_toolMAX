import struct

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableView, QHeaderView, QAbstractItemView

from AQ_ParamsDelegateEditors import AqUintTreeLineEdit, AqEnumROnlyTreeLineEdit, AQ_IpTreeLineEdit, \
    AqIntTreeLineEdit, AqFloatTreeLineEdit, AqStringTreeLineEdit, AqDateTimeLineEdit, AQ_TreeLineEdit


class AQ_DeviceInfoTableView(QTableView):
    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.setModel(model)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("""QTableView {color: #D0D0D0;}
                           QTableView::item { padding-left: 3px; }
                           QTableView:item:!focus { background-color: transparent; color: #D0D0D0}""")
        # self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)

        row_height = 25
        row_count = self.model().rowCount()
        for i in range(row_count):
            self.setRowHeight(i, row_height)
        self.setFixedHeight(row_height * row_count + 2)

    def setModel(self, model):
        super().setModel(model)
        root = model.invisibleRootItem()
        self.traverse_items_show_delegate(root)

    def traverse_items_show_delegate(self, item):
        for row in range(item.rowCount()):
            child_item = item.child(row)
            parameter_attributes = child_item.data(Qt.UserRole)
            if parameter_attributes is not None:
                if parameter_attributes.get('is_catalog', 0) == 1:
                    self.traverse_items_show_delegate(child_item)
                else:
                    index = self.model().index(row, 1, item.index())
                    _editor = self.get_editor_by_type(parameter_attributes)
                    editor = _editor(parameter_attributes, self)
                    self.setIndexWidget(index, editor)
                    value = index.data(Qt.UserRole)
                    if parameter_attributes.get('type', '') == 'float':    # HADRCODE
                        float_value = struct.unpack('!f', bytes.fromhex(value))[0]
                        editor.set_value(round(float_value, 7))
                    else:
                        editor.set_value(int(value, 16))

    def get_editor_by_type(self, param_attributes):
        param_type = param_attributes.get('type', '')
        if param_type == 'enum':
            editor = AqEnumROnlyTreeLineEdit
        elif param_type == 'unsigned':
            if param_attributes.get('visual_type', '') == 'ip_format':
                editor = AQ_IpTreeLineEdit
            else:
                editor = AqUintTreeLineEdit
        elif param_type == 'signed':
            editor = AqIntTreeLineEdit
        elif param_type == 'float':
            editor = AqFloatTreeLineEdit
        elif param_type == 'string':
            editor = AqStringTreeLineEdit
        elif param_type == 'date_time':
            editor = AqDateTimeLineEdit
        else:
            editor = AQ_TreeLineEdit

        return editor


# class AQ_ParamListInfoTableView(QTableView):
#     def __init__(self, model, parent=None):
#         super().__init__(parent)
#
#         self.verticalHeader().setVisible(False)
#         self.horizontalHeader().setVisible(False)
#         # self.horizontalHeader().setStyleSheet(
#         #     "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
#         self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.setStyleSheet("""QTableView {border: none; color: #D0D0D0;}
#                            QTableView::item { padding-left: 3px; }
#                            QTableView:item:!focus { background-color: transparent; color: #D0D0D0}""")
#         self.setShowGrid(False)
#         # self.setSortingEnabled(True)
#         self.setEditTriggers(QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
#         self.setModel(model)
#         row_height = 25
#         row_count = self.model().rowCount()
#         for i in range(row_count):
#             self.setRowHeight(i, row_height)
#         self.setFixedHeight(row_height * row_count)
