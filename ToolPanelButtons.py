from PyQt5.QtWidgets import QPushButton, QToolButton, QFrame
from PyQt5.QtCore import Qt, QTimer, QRect, QSize
from PyQt5.QtGui import QIcon, QPalette, QPixmap, QFont


class TemplateToolButton(QToolButton):
    def __init__(self, icon, parent=None):
        super().__init__(parent)
        self.setText("TestButton")
        self.setGeometry(0, 0, 65, 65)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setStyleSheet("QToolButton {color: #D0D0D0;}"
                           "QToolButton:hover {background-color: #9d4d4f;}")
        self.setFont(QFont("Verdana", 9))  # Задаем шрифт и размер


class AddDeviceButton(TemplateToolButton):
    def __init__(self, icon, parent=None):
        super().__init__(parent)
        self.setText("Add Device")
        self.setIcon(icon)
        icon_size = QSize(65, 65)  # Установите нужные значения ширины и высоты иконки
        self.setIconSize(icon_size)


class Btn_AddDevices(TemplateToolButton):
    def __init__(self, icon, parent=None):
        super().__init__(parent)
        self.setText("Add Devices")
        self.setIcon(icon)
        icon_size = QSize(65, 65)  # Установите нужные значения ширины и высоты иконки
        self.setIconSize(icon_size)
        self.setStyleSheet("QToolButton {color: #D0D0D0;}"
                           "QToolButton:hover {background-color: #429061;}")


class Btn_DeleteDevices(TemplateToolButton):
    def __init__(self, icon, parent=None):
        super().__init__(parent)
        self.setText("Delete Devices")
        self.setIcon(icon)
        icon_size = QSize(65, 65)  # Установите нужные значения ширины и высоты иконки
        self.setIconSize(icon_size)
        self.setStyleSheet("QToolButton {color: #D0D0D0;}"
                           "QToolButton:hover {background-color: #429061;}")


class Btn_IPAdresess(TemplateToolButton):
    def __init__(self, icon, parent=None):
        super().__init__(parent)
        self.setText("IP Adresses")
        self.setIcon(icon)
        icon_size = QSize(65, 65)  # Установите нужные значения ширины и высоты иконки
        self.setIconSize(icon_size)
        self.setStyleSheet("QToolButton {color: #D0D0D0;}"
                           "QToolButton:hover {background-color: #429061;}")


class Btn_Read(TemplateToolButton):
    def __init__(self, icon, parent=None):
        super().__init__(parent)
        self.setText("Read parameters")
        self.setIcon(icon)
        icon_size = QSize(65, 65)  # Установите нужные значения ширины и высоты иконки
        self.setIconSize(icon_size)
        self.setStyleSheet("QToolButton {color: #D0D0D0;}"
                           "QToolButton:hover {background-color: #429061;}")


class Btn_Write(TemplateToolButton):
    def __init__(self, icon, parent=None):
        super().__init__(parent)
        self.setText("Write parameters")
        self.setIcon(icon)
        icon_size = QSize(65, 65)  # Установите нужные значения ширины и высоты иконки
        self.setIconSize(icon_size)
        self.setStyleSheet("QToolButton {color: #D0D0D0;}"
                           "QToolButton:hover {background-color: #429061;}")


class Btn_FactorySettings(TemplateToolButton):
    def __init__(self, icon, parent=None):
        super().__init__(parent)
        self.setText("Factory settings")
        self.setIcon(icon)
        icon_size = QSize(65, 65)  # Установите нужные значения ширины и высоты иконки
        self.setIconSize(icon_size)
        self.setStyleSheet("QToolButton {color: #D0D0D0;}"
                           "QToolButton:hover {background-color: #9d4d4f;}")


class Btn_WatchList(TemplateToolButton):
    def __init__(self, icon, parent=None):
        super().__init__(parent)
        self.setText("Watch list")
        self.setIcon(icon)
        icon_size = QSize(65, 65)  # Установите нужные значения ширины и высоты иконки
        self.setIconSize(icon_size)
        self.setStyleSheet("QToolButton {color: #D0D0D0;}"
                           "QToolButton:hover {background-color: #9d4d4f;}")

class VLine_separator(QFrame):
    def __init__(self, height, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.VLine)
        self.setFixedSize(1, height - 10)
        self.setStyleSheet("background-color: #5caa62;\n")
