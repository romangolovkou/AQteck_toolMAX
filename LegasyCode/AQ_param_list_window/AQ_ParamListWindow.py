from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication

from AQ_CustomWindowTemplates import AQ_SimplifiedDialog
from AQ_ParamListManagerFrame import AQ_ParamListManagerFrame


class AQ_DialogParamList(AQ_SimplifiedDialog):
    def __init__(self, device, event_manager, parent):
        window_name = 'Parameter list'
        super().__init__(event_manager, window_name)

        self.setObjectName("AQ_Dialog_parameter_list")
        self.parent = parent
        self.event_manager = event_manager
        self.device = device
        self.setGeometry(0, 0, 900, 800)
        self.main_window_frame.setGeometry(0, 0, self.width(),
                                           self.height())
        # Получаем геометрию основного экрана
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        self.move(screen_geometry.width() // 2 - self.width() // 2,
                  screen_geometry.height() // 2 - self.height() // 2,)

        #Створюємо головний фрейм
        self.param_list_manager_frame = AQ_ParamListManagerFrame(self.device, self.event_manager, self)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Переопределяем метод resizeEvent и вызываем resize для main_window_frame
        self.param_list_manager_frame.setGeometry(0, self.main_window_frame.title_bar_frame.height(), self.width(),
                                                  self.height() - self.main_window_frame.title_bar_frame.height())
        event.accept()






