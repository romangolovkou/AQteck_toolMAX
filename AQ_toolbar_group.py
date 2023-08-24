from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QMenu, QAction, QBoxLayout, \
                            QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QPixmap, QFont, QIntValidator, QRegExpValidator, QColor, QStandardItemModel, \
                        QStandardItem, QTransform, QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer, QRect, QSize
from AQ_toolbar_button import AQ_ToolButton

PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'


class AQ_toolbar_group_template(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons = []
        self.group_layout = 0

    def change_oriental(self):
        if isinstance(self.layout(), QHBoxLayout):
            self.layout().deleteLater()
            self.group_layout = Group_LayV(self, *self.buttons)
            self.setLayout(self.group_layout)
        elif isinstance(self.layout(), QVBoxLayout):
            self.layout().deleteLater()
            self.group_layout = Group_LayH(self, *self.buttons)
            self.setLayout(self.group_layout)


class AQ_device_action_group(AQ_toolbar_group_template):
    def __init__(self, parent=None):
        super().__init__(parent)
    # кнопка 1
        self.ico_btn_add_devise = QIcon(PROJ_DIR + 'Icons/Add_device.png')
        self.btn_add_devices = AQ_ToolButton('Add Devices', self.ico_btn_add_devise)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_add_devices)
    # кнопка 2
        self.ico_btn_delete_device = QIcon(PROJ_DIR + 'Icons/Delete_device.png')
        self.btn_delete_devices = AQ_ToolButton('Delete Devices', self.ico_btn_delete_device)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_delete_devices)
    # кнопка 3
        self.ico_btn_ip_adresses = QIcon(PROJ_DIR + 'Icons/ip_adresses.png')
        self.btn_delete_devices = AQ_ToolButton('IP Addresses', self.ico_btn_ip_adresses)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_delete_devices)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.setLayout(self.group_layout)


class AQ_param_action_group(AQ_toolbar_group_template):
    def __init__(self, parent=None):
        super().__init__(parent)
    # кнопка 1
        self.ico_btn_read = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_read = AQ_ToolButton('Read parameters', self.ico_btn_read)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_read)
    # кнопка 2
        self.ico_btn_write = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_write = AQ_ToolButton('Write parameters', self.ico_btn_write)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_write)
    # кнопка 3
        self.ico_btn_factory_settings = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_factory_settings = AQ_ToolButton('Factory settings', self.ico_btn_factory_settings)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_factory_settings)
    # кнопка 4
        self.ico_btn_watch_list = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_watch_list = AQ_ToolButton('Watch list', self.ico_btn_watch_list)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_watch_list)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.setLayout(self.group_layout)


class AQ_utils_group(AQ_toolbar_group_template):
    def __init__(self, parent=None):
        super().__init__(parent)
    # кнопка 1
        self.ico_btn_read = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_read = AQ_ToolButton('Real-time clock', self.ico_btn_read)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_read)
    # кнопка 2
        self.ico_btn_write = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_write = AQ_ToolButton('Password', self.ico_btn_write)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_write)
    # кнопка 3
        self.ico_btn_factory_settings = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_factory_settings = AQ_ToolButton('Calibration', self.ico_btn_factory_settings)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_factory_settings)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.setLayout(self.group_layout)


class AQ_archieve_group(AQ_toolbar_group_template):
    def __init__(self, parent=None):
        super().__init__(parent)
    # кнопка 1
        self.ico_btn_read = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_read = AQ_ToolButton('Save log data', self.ico_btn_read)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_read)
    # кнопка 2
        self.ico_btn_write = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_write = AQ_ToolButton('Data logging settings', self.ico_btn_write)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_write)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.setLayout(self.group_layout)




class Group_LayH(QHBoxLayout):
    def __init__(self, parent=None, *buttons):
        super().__init__(parent)
        self.setContentsMargins(2, 0, 2, 0)
        self.setSpacing(0)
        for button in buttons:
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            self.addWidget(button)

class Group_LayV(QVBoxLayout):
    def __init__(self, parent=None, *buttons):
        super().__init__(parent)
        self.setContentsMargins(2, 0, 2, 0)
        self.setSpacing(0)
        count = len(buttons)
        for button in buttons:
            if count > 2:
                button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            else:
                button.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.addWidget(button)

