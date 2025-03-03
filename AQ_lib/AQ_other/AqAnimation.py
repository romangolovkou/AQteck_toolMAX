from PySide6.QtCore import QSize
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QWidget, QLabel

from AqTranslateManager import AqTranslateManager
from ui_DeviceInitWidget import Ui_DeviceInitWidget


class AqAnimation(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.movie = QMovie('UI/icons/AQannimation.gif')
        x = self.width()
        y = self.height()
        self.movie.setScaledSize(QSize(self.width(), self.height()))
        self.setMovie(self.movie)

    # def retranslate(self):
    #     self.ui.retranslateUi(self)

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()

    def set_movie_size(self, x, y):
        self.movie.setScaledSize(QSize(x, y))

    def resize(self, qsize):
        super().resize(qsize)
        self.movie.setScaledSize(qsize)

