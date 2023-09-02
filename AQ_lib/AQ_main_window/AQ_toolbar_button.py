from PyQt5.QtWidgets import QPushButton, QToolButton, QFrame
from PyQt5.QtCore import Qt, QTimer, QRect, QSize
from PyQt5.QtGui import QIcon, QPalette, QPixmap, QFont


class AQ_ToolButton(QToolButton):
    def __init__(self, text, icon, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, 65, 65)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setStyleSheet("QToolButton {color: #D0D0D0;}"
                           "QToolButton:hover {background-color: #429061;}")
        self.setFont(QFont("Verdana", 9))  # Задаем шрифт и размер
        self.setText(text)
        self.setIcon(icon)
        icon_size = QSize(65, 65)  # Установите нужные значения ширины и высоты иконки
        self.setIconSize(icon_size)
