from PySide6.QtWidgets import QComboBox

from time_zones import time_zones_list_en


class AqTimeZoneComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Получаем список часовых поясов
        self.addItems(time_zones_list_en)
