from PySide2.QtGui import QGuiApplication
from PySide2.QtWidgets import QApplication

from AQ_CustomWindowTemplates import AQ_SimplifiedDialog
from AQ_DeviceInfoManagerFrame import AQ_DeviceInfoManagerFrame


class AQ_DialogDeviceInfo(AQ_SimplifiedDialog):
    def __init__(self, device, event_manager, parent):
        window_name = 'Device information'
        super().__init__(event_manager, window_name)

        self.setObjectName("AQ_Dialog_device_information")
        self.parent = parent
        self.event_manager = event_manager
        self.device = device
        self.setGeometry(0, 0, 500, 500)
        self.main_window_frame.setGeometry(0, 0, self.width(),
                                           self.height())
        # Получаем геометрию основного экрана
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        self.move(screen_geometry.width() // 2 - self.width() // 2,
                  screen_geometry.height() // 2 - self.height() // 2,)

        # Створюємо головний фрейм
        self.device_info_manager_frame = AQ_DeviceInfoManagerFrame(self.device, self.event_manager, self)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Переопределяем метод resizeEvent и вызываем resize window_frame
        self.device_info_manager_frame.setGeometry(0, self.main_window_frame.title_bar_frame.height(), self.width(),
                                                  self.height() - self.main_window_frame.title_bar_frame.height())
        event.accept()
