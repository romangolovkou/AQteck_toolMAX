from PySide2.QtGui import QGuiApplication
from PySide2.QtWidgets import QApplication

from AQ_CustomWindowTemplates import AQ_FullDialog
from AQ_WatchListManagerFrame import AQ_WatchListManagerFrame


class AQ_DialogWatchList(AQ_FullDialog):
    def __init__(self, event_manager, parent):
        window_name = 'Watch list'
        super().__init__(event_manager, window_name)
        self.window_name = window_name
        self.setGeometry(0, 0, 500, 300)
        # Получаем геометрию основного экрана
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        self.move(screen_geometry.width() - self.width() - 100,
                  screen_geometry.height() // 5)

        # Створюємо головний фрейм
        self.watch_list_manager_frame = AQ_WatchListManagerFrame(self.event_manager, self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.watch_list_manager_frame.setGeometry(4, self.main_window_frame.title_bar_frame.height(), self.width() - 8,
                                                  self.height() - self.main_window_frame.title_bar_frame.height() - 4)
        event.accept()
