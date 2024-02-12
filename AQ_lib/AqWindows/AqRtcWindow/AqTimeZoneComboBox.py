from PySide6.QtWidgets import QComboBox

from time_zones import time_zones_list_en


class AqTimeZoneComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Получаем список часовых поясов
        self.addItems(time_zones_list_en)

    def set_item_text_by_shift(self, time_shift):
        # Получение списка всех элементов
        all_items = [self.itemText(i) for i in range(self.count())]

        shift_str = str(time_shift)

        for item_text in all_items:
            if shift_str in item_text:
                self.setCurrentText(item_text)
                return

