from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyledItemDelegate


class AQ_ValueTreeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        param_manager_item_index = index.sibling(index.row(), 0)
        manager_item = self.parent().model().itemFromIndex(param_manager_item_index)
        try:
            editor = manager_item.get_editor()
            param_attributes = manager_item.get_param_attributes()
            editor = editor(param_attributes, parent)
            editor.set_manager_item_handler(manager_item.save_new_value)
            manager_item.save_editor_object(editor)
            return editor

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            print('no editor')

    def setModelData(self, editor, model, index):
        # Заглушуємо стандартний механізм додавання введених через delegate-editor значень у ітем
        # розташований в колонці Value.
        # У нашому випадку вся робота з delegate-editor відбувається через AQ_ParamManagerItem
        # що розташований у першій колонці та містить назву параметру, а стандартний механізм
        # розміщює введене значення "позаду" delegate-editor у Value-ітем у Qt.EditRole або Qt.DisplayRole
        # через що на єкрані видно подвійне відображення значення, якщо у delegate-editor
        # встановлений прозорий фон
        pass


class AQ_NameTreeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):

        param_status = index.data(Qt.UserRole + 1)  # Получаем данные
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
            self.check_parent_catalog(index)

    def check_parent_catalog(self, index):
        error_flag = 0
        changed_flag = 0
        parent_index = index.parent()
        if parent_index.isValid():
            child_count = index.model().rowCount(parent_index)
            # Перебираем индексы дочерних элементов
            for row in range(child_count):
                child_index = index.model().index(row, 0, parent_index)  # Получаем индекс дочернего элемента
                # Получаем данные userRole по индексу
                status = index.model().data(child_index, Qt.UserRole + 1)
                if status == 'error':
                    error_flag += 1
                elif status == 'changed':
                    changed_flag += 1

            if error_flag > 0:
                cat_status = 'error'
            elif changed_flag > 0:
                cat_status = 'changed'
            else:
                cat_status = 'ok'

            index.model().setData(parent_index, cat_status, Qt.UserRole + 1)

