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

    # def set_item_chandeg_flag(self, index, flag):
    #         self.changed_dict[index] = flag
    #
    # def set_by_prog_flag(self, index, flag):
    #         self.set_by_prog_flag_dict[index] = flag
    #
    # def set_error_flag(self, index, flag):
    #         self.error_dict[index] = flag
    #
    # def value_is_valid(self, index, param_type):
    #     user_data = index.data(Qt.EditRole)
    #     min_limit_index = index.sibling(index.row(), 2)
    #     max_limit_index = index.sibling(index.row(), 3)
    #     min_limit = min_limit_index.data(Qt.DisplayRole)
    #     max_limit = max_limit_index.data(Qt.DisplayRole)
    #
    #     if param_type == 'unsigned' or param_type == 'signed':
    #         if min_limit is not None:
    #             try:
    #                 min_limit = int(min_limit)
    #             except:
    #                 print("min_limit не є числом")
    #                 return False
    #             if user_data < min_limit:
    #                 return False
    #         if max_limit is not None:
    #             try:
    #                 max_limit = int(max_limit)
    #             except:
    #                 print("max_limit не є числом")
    #                 return False
    #             if user_data > int(max_limit):
    #                 return False
    #     elif param_type == 'float':
    #         if min_limit is not None:
    #             try:
    #                 min_limit = float(min_limit)
    #             except:
    #                 print("min_limit не є числом")
    #                 return False
    #             if user_data < min_limit:
    #                 return False
    #         if max_limit is not None:
    #             try:
    #                 max_limit = float(max_limit)
    #             except:
    #                 print("max_limit не є числом")
    #                 return False
    #             if user_data > float(max_limit):
    #                 return False
    #
    #     return True

    def createEditor(self, parent, option, index):
        param_mamager_item_index = index.sibling(index.row(), 0)
        manager_item = self.parent().model().itemFromIndex(param_mamager_item_index)
        try:
            editor = manager_item.get_editor()
            param_attributes = manager_item.get_param_attributes()
            editor = editor(param_attributes, parent)
            manager_item.save_editor_object(editor)
            return editor

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            print('no editor')

        # # Получаем данные из модели для текущего индекса
        # delegate_attributes = index.data(Qt.UserRole)
        # if delegate_attributes is not None:
        #     if delegate_attributes.get('type', '') == 'enum':
        #         combo_box = QComboBox(parent)
        #         combo_box.view().setStyleSheet("color: #D0D0D0;")
        #         combo_box.setStyleSheet("QComboBox { border: 0px solid #D0D0D0; color: #D0D0D0; }")
        #         enum_strings = delegate_attributes.get('enum_strings', '')
        #         for i in range(len(enum_strings)):
        #             enum_str = enum_strings[i]
        #             combo_box.addItem(enum_str)
        #         combo_box.currentIndexChanged.connect(self.commit_editor_data)
        #         return combo_box
        #     elif delegate_attributes.get('type', '') == 'unsigned':
        #         if not (delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0):
        #             if delegate_attributes.get('visual_type', '') == 'ip_format':
        #                 editor = AQ_IP_tree_QLineEdit(parent)
        #                 font = QFont("Segoe UI", 9)
        #                 editor.setFont(font)
        #                 editor.setStyleSheet("border: none; border-style: outset; color: #D0D0D0;")
        #                 editor.textChanged.connect(self.commit_editor_data)
        #             else:
        #                 min_limit_index = index.sibling(index.row(), 2)
        #                 max_limit_index = index.sibling(index.row(), 3)
        #                 min_limit = min_limit_index.data(Qt.DisplayRole)
        #                 if min_limit is not None:
        #                     min_limit = int(min_limit)
        #
        #                 max_limit = max_limit_index.data(Qt.DisplayRole)
        #                 if max_limit is not None:
        #                     max_limit = int(max_limit)
        #                 editor = AQ_uint_tree_QLineEdit(min_limit, max_limit, parent)
        #                 font = QFont("Segoe UI", 9)
        #                 editor.setFont(font)
        #                 editor.setStyleSheet("border: none; border-style: outset; color: #D0D0D0;")  # Устанавливаем стиль
        #                 editor.textChanged.connect(self.commit_editor_data)
        #             return editor
        #     elif delegate_attributes.get('type', '') == 'signed':
        #         if not (delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0):
        #             min_limit_index = index.sibling(index.row(), 2)
        #             max_limit_index = index.sibling(index.row(), 3)
        #             min_limit = min_limit_index.data(Qt.DisplayRole)
        #             if min_limit is not None:
        #                 min_limit = int(min_limit)
        #
        #             max_limit = max_limit_index.data(Qt.DisplayRole)
        #             if max_limit is not None:
        #                 max_limit = int(max_limit)
        #
        #             editor = AQ_int_tree_QLineEdit(min_limit, max_limit, parent)
        #             font = QFont("Segoe UI", 9)
        #             editor.setFont(font)
        #             editor.setStyleSheet("border: none; border-style: outset; color: #D0D0D0;")  # Устанавливаем стиль
        #             editor.textChanged.connect(self.commit_editor_data)
        #             return editor
        #     elif delegate_attributes.get('type', '') == 'string':
        #         if not (delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0):
        #             editor = QLineEdit(parent)
        #             font = QFont("Segoe UI", 9)
        #             editor.setFont(font)
        #             editor.setStyleSheet("border: none; border-style: outset; color: #D0D0D0;")  # Устанавливаем стиль
        #             editor.textChanged.connect(self.commit_editor_data)
        #             return editor
        #     elif delegate_attributes.get('type', '') == 'float':
        #         if not (delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0):
        #             min_limit_index = index.sibling(index.row(), 2)
        #             max_limit_index = index.sibling(index.row(), 3)
        #             min_limit = min_limit_index.data(Qt.DisplayRole)
        #             if min_limit is not None:
        #                 min_limit = float(min_limit)
        #
        #             max_limit = max_limit_index.data(Qt.DisplayRole)
        #             if max_limit is not None:
        #                 max_limit = float(max_limit)
        #
        #             editor = AQ_float_tree_QLineEdit(min_limit, max_limit, parent)
        #             font = QFont("Segoe UI", 9)
        #             editor.setFont(font)
        #             editor.setStyleSheet("border: none; border-style: outset; color: #D0D0D0;")  # Устанавливаем стиль
        #             editor.textChanged.connect(self.commit_editor_data)
        #             return editor
    # def commit_editor_data(self):
    #     editor = self.sender()  # Получаем отправителя события
    #     if editor:
    #         if isinstance(editor, QComboBox):
    #             self.commitData.emit(editor)  # Вызываем commitData для делегата
    #         else:
    #             if editor.text() != '':
    #                 self.commitData.emit(editor)  # Вызываем commitData для делегата

    def setEditorData(self, editor, index):
        delegate_attributes = index.data(Qt.UserRole)
        if delegate_attributes is not None:
            if delegate_attributes.get('type', '') == 'enum':
                user_data = index.data(Qt.EditRole)
                if user_data is not None:
                    editor.setCurrentIndex(user_data)
            if delegate_attributes.get('type', '') == 'unsigned' or \
                    delegate_attributes.get('type', '') == 'signed' or delegate_attributes.get('type', '') == 'float':
                user_data = index.data(Qt.EditRole)
                if user_data is not None:
                    if self.value_is_valid(index, delegate_attributes.get('type', '')):
                        editor.setText(str(user_data))
                        self.set_error_flag(index, False)
                    else:
                        self.set_error_flag(index, True)
            elif delegate_attributes.get('type', '') == 'string':
                user_data = index.data(Qt.EditRole)
                if user_data is not None:
                    editor.setText(str(user_data))

            set_by_program_flag = self.set_by_prog_flag_dict.get(index, True)
            if set_by_program_flag is not True:
                self.set_item_chandeg_flag(index, True)
                new_index = index.sibling(index.row(), 0)
                self.parent().setLineColor(new_index, '#429061')
            else:
                self.set_by_prog_flag_dict[index] = False

            have_error = self.error_dict.get(index, False)
            if have_error is True:
                new_index = index.sibling(index.row(), 0)
                self.parent().setLineColor(new_index, '#9d4d4f')

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
        self.color_dict = {}  # Словарь для хранения цветов фона

    def set_item_color(self, index, color):
        self.color_dict[index] = color

    def paint(self, painter, option, index):
        data = index.data(Qt.DisplayRole)  # Получаем данные
        if data is not None:
            painter.save()

            # Определяем цвет фона из словаря или белый цвет по умолчанию
            background_color = self.color_dict.get(index, QColor('#1e1f22'))
            painter.fillRect(option.rect, background_color)
            painter.restore()
            super().paint(painter, option, index)