from PyQt5.QtWidgets import QApplication

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
        self.main_window_frame.setGeometry(1, 0, self.width() - 2,
                                           self.height() - 1)
        self.screen_geometry = QApplication.desktop().screenGeometry()
        self.move(self.screen_geometry.width() // 2 - self.width() // 2,
                  self.screen_geometry.height() // 2 - self.height() // 2,)

        # Рєєструємо обробники подій
        self.event_manager.register_event_handler('minimize_' + window_name, self.showMinimized)
        self.event_manager.register_event_handler('close_' + window_name, self.close)
        self.event_manager.register_event_handler('dragging_' + window_name, self.move)

        #Створюємо головний фрейм
        self.param_list_manager_frame = AQ_ParamListManagerFrame(self.device, self.event_manager, self)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Переопределяем метод resizeEvent и вызываем resize для main_window_frame
        self.title_bar_frame.resize(self.width(), self.title_bar_frame.height())
        self.param_list_manager_frame.setGeometry(0, self.title_bar_frame.height(), self.width(),
                                                  self.height() - self.title_bar_frame.height())
        event.accept()






