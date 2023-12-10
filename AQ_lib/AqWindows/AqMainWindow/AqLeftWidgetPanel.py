from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget

from AQ_EventManager import AQ_EventManager


class AqLeftPanelAddWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.event_manager = AQ_EventManager.get_global_event_manager()
        # Создаем палитру с фоновыми цветами
        self.normal_palette = self.palette()
        self.hover_palette = QPalette()
        self.hover_palette.setColor(QPalette.Window, QColor("#16191d"))
        self.setPalette(self.hover_palette)

    def enterEvent(self, event):
        # Применяем палитру при наведении
        self.setPalette(self.hover_palette)
        self.setAutoFillBackground(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Возвращаем обычную палитру при уходе курсора
        self.setPalette(self.normal_palette)
        self.setAutoFillBackground(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('widget "openAddDeviceWindow" was called')
            self.event_manager.emit_event('open_AddDevices')
        super().mousePressEvent(event)
