from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QWidget

from ui_DeviceInitWidget import Ui_DeviceInitWidget


class DeviceInitWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_DeviceInitWidget()
        self.ui.setupUi(self)

        self.movie = QMovie(u":/images/icons/cat.gif")
        self.ui.CatLabel.setMovie(self.movie)

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()
