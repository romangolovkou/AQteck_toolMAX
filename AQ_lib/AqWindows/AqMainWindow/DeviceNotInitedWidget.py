from PySide6.QtCore import QSize
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QWidget

from AqTranslateManager import AqTranslateManager
from ui_DeviceInitWidget import Ui_DeviceInitWidget


class DeviceInitWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_DeviceInitWidget()
        self.ui.setupUi(self)

        self.ui.label_2.hide()

        self.movie = QMovie('UI/icons/AQannimation.gif')
        self.movie.setScaledSize(QSize(282, 158))
        self.ui.CatLabel.setMovie(self.movie)
        AqTranslateManager.subscribe(self.retranslate)

    def retranslate(self):
        self.ui.retranslateUi(self)

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()
