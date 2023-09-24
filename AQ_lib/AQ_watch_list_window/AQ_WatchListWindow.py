from AQ_CustomWindowTemplates import AQ_FullDialog

class AQ_DialogWatchList(AQ_FullDialog):
    def __init__(self, event_manager, parent):
        window_name = 'Watch list'
        super().__init__(event_manager, window_name)
        self.window_name = window_name
        self.setGeometry(100, 100, 600, 500)

    def resize_window(self, pos_x, pos_y, width, height):
        super().resize_window(pos_x, pos_y, width, height)

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     # Переопределяем метод resizeEvent и вызываем resize для main_window_frame
    #     self.main_window_frame.resize(self.width(), self.height())
    #     event.accept()
