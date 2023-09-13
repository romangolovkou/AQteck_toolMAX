from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QLineEdit, QStyledItemDelegate
from custom_window_templates import AQ_IP_tree_QLineEdit, \
                                    AQ_int_tree_QLineEdit, AQ_uint_tree_QLineEdit, AQ_float_tree_QLineEdit
from AQ_communication_func import is_valid_ip



class AQ_ValueTreeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.changed_dict = {}  # Словник для флагів змін значення
        self.error_dict = {}  # Словник для флагів наявності помилок у значеннях
        self.set_by_prog_flag_dict = {}  # Словник для флагів змін значення зсередини коду (не користувачем)

    def createEditor(self, parent, option, index):
        param_manager_item_index = index.sibling(index.row(), 0)
        manager_item = self.parent().model().itemFromIndex(param_manager_item_index)
        try:
            editor = manager_item.get_editor()
            param_attributes = manager_item.get_param_attributes()
            editor = editor(param_attributes, parent)
            # editor.textChanged.connect(self.commit_editor_data)
            editor.set_new_value_handler(manager_item.save_new_value)
            manager_item.save_editor_object(editor)
            return editor

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            print('no editor')

    # def commit_editor_data(self):
    #     editor = self.sender()  # Получаем отправителя события
    #     if editor:
    #         self.commitData.emit(editor)  # Вызываем commitData для делегата


    # def commit_editor_data(self):
    #     editor = self.sender()  # Получаем отправителя события
    #     if editor:
    #         if isinstance(editor, QComboBox):
    #             self.commitData.emit(editor)  # Вызываем commitData для делегата
    #         else:
    #             if editor.text() != '':
    #                 self.commitData.emit(editor)  # Вызываем commitData для делегата

    # def setEditorData(self, editor, index):
    #     delegate_attributes = index.data(Qt.UserRole)
    #     if delegate_attributes is not None:
    #         if delegate_attributes.get('type', '') == 'enum':
    #             user_data = index.data(Qt.EditRole)
    #             if user_data is not None:
    #                 editor.setCurrentIndex(user_data)
    #         if delegate_attributes.get('type', '') == 'unsigned' or \
    #                 delegate_attributes.get('type', '') == 'signed' or delegate_attributes.get('type', '') == 'float':
    #             user_data = index.data(Qt.EditRole)
    #             if user_data is not None:
    #                 if self.value_is_valid(index, delegate_attributes.get('type', '')):
    #                     editor.setText(str(user_data))
    #                     self.set_error_flag(index, False)
    #                 else:
    #                     self.set_error_flag(index, True)
    #         elif delegate_attributes.get('type', '') == 'string':
    #             user_data = index.data(Qt.EditRole)
    #             if user_data is not None:
    #                 editor.setText(str(user_data))
    #
    #         set_by_program_flag = self.set_by_prog_flag_dict.get(index, True)
    #         if set_by_program_flag is not True:
    #             self.set_item_chandeg_flag(index, True)
    #             new_index = index.sibling(index.row(), 0)
    #             self.parent().setLineColor(new_index, '#429061')
    #         else:
    #             self.set_by_prog_flag_dict[index] = False
    #
    #         have_error = self.error_dict.get(index, False)
    #         if have_error is True:
    #             new_index = index.sibling(index.row(), 0)
    #             self.parent().setLineColor(new_index, '#9d4d4f')

    def setModelData(self, editor, model, index):
        delegate_attributes = index.data(Qt.UserRole)
        if delegate_attributes is not None:
            if delegate_attributes.get('type', '') == 'enum':
                model.setData(index, editor.currentIndex())
            elif delegate_attributes.get('type', '') == 'unsigned':
                if delegate_attributes.get('visual_type', '') == 'ip_format':
                    ip = editor.text()
                    if is_valid_ip(ip):
                        model.setData(index, ip)
                else:
                    user_data = editor.text()
                    if user_data != '':
                        model.setData(index, int(user_data, 10))
            elif delegate_attributes.get('type', '') == 'signed':
                user_data = editor.text()
                if user_data != '' and user_data != '-':
                    model.setData(index, int(user_data, 10))
            elif delegate_attributes.get('type', '') == 'string':
                user_data = editor.text()
                if user_data != '':
                    model.setData(index, user_data)
            elif delegate_attributes.get('type', '') == 'float':
                user_data = editor.text()
                if user_data != '' and user_data != '-':
                    model.setData(index, float(user_data))


class AQ_NameTreeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_item_color(self, index, color):
        self.color_dict[index] = color

    def paint(self, painter, option, index):
        param_status = index.data(Qt.UserRole  + 1)  # Получаем данные
        if param_status is not None:
            painter.save()

            # # Определяем цвет фона из словаря или белый цвет по умолчанию
            if param_status == 'changed':
                background_color = QColor('#429061')
            elif param_status == 'error':
                background_color = QColor('#9d4d4f')
            else:
                background_color = QColor('transparent')

            painter.fillRect(option.rect, background_color)
            painter.restore()
            super().paint(painter, option, index)
