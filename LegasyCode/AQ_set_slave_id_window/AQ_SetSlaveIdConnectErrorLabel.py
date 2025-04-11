from PySide2.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget

from AQ_CustomWindowTemplates import AQ_Label


class AQ_ConnectErrorLabel(QWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, width, height)
        self.connect_err_label = AQ_Label("<html>The connection to device could not be established.<br>"
                                         "Check the connection lines and network parameters and repeat "
                                         "the search.<html>", self)
        self.connect_err_label.setStyleSheet("background-color: #9d2d30; color: #D0D0D0; \n")
        self.connect_err_label.setFont(QFont("Verdana", 12))  # Задаем шрифт и размер
        self.connect_err_label.setAlignment(Qt.AlignCenter)
        self.connect_err_label.setFixedSize(self.width(), 50)
        self.connect_err_label.move(0, self.height())
        self.connect_err_label.show()
        # Создаем анимацию для перемещения плашки вверх и вниз
        self.animation = QPropertyAnimation(self.connect_err_label, b"geometry")
        # Показываем плашку с помощью анимации
        start_rect = self.connect_err_label.geometry()
        end_rect = QRect(start_rect.x(), start_rect.y() - 50, start_rect.width(), start_rect.height())
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.setDuration(800)  # Продолжительность анимации в миллисекундах
        self.animation.start()

        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.hide_connect_err_label)

    def hide_connect_err_label(self):
        # Скрываем плашку с помощью анимации
        start_rect = self.connect_err_label.geometry()
        end_rect = QRect(start_rect.x(), start_rect.y() + 50, start_rect.width(), start_rect.height())
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.setDuration(800)  # Продолжительность анимации в миллисекундах
        self.animation.start()
        QTimer.singleShot(900, self.deleteLater)
