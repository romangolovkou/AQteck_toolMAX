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
        self.setMinimumSize(60, 60)
        self.proxy_lay = QHBoxLayout(self)
        self.proxy_lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.proxy_lay)

    def change_oriental(self):
        cur_group_layout = self.proxy_lay.itemAt(0)
        if isinstance(cur_group_layout, QHBoxLayout):
            self.proxy_lay.removeItem(cur_group_layout)
            self.group_layout = Group_LayV(self, *self.buttons)
            self.proxy_lay.addLayout(self.group_layout)
            cur_group_layout.deleteLater()
        elif isinstance(cur_group_layout, QVBoxLayout):
            self.proxy_lay.removeItem(cur_group_layout)
            self.group_layout = Group_LayH(self, *self.buttons)
            self.proxy_lay.addLayout(self.group_layout)
            cur_group_layout.deleteLater()


class AQ_device_action_group(AQ_toolbar_group_template):
    def __init__(self, parent=None):
        super().__init__(parent)
    # кнопка 1
        self.ico_btn_add_devise = QIcon(PROJ_DIR + 'Icons/Add_device.png')
        self.btn_add_devices = AQ_ToolButton('Add Devices', self.ico_btn_add_devise)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        # self.btn_add_devices.clicked.connect(self.change_oriental)
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
        self.proxy_lay.addLayout(self.group_layout)


class AQ_param_action_group(AQ_toolbar_group_template):
    def __init__(self, parent=None):
        super().__init__(parent)
    # кнопка 1
        self.ico_btn_read = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_read = AQ_ToolButton('Read parameters', self.ico_btn_read)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        # self.btn_read.clicked.connect(self.change_oriental)
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
        self.proxy_lay.addLayout(self.group_layout)


class AQ_utils_group(AQ_toolbar_group_template):
    def __init__(self, parent=None):
        super().__init__(parent)
    # кнопка 1
        self.ico_btn_rtc = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_rtc = AQ_ToolButton('Real-time clock', self.ico_btn_rtc)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        # self.btn_rtc.clicked.connect(self.change_oriental)
        self.buttons.append(self.btn_rtc)
    # кнопка 2
        self.ico_btn_pass = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_pass = AQ_ToolButton('Password', self.ico_btn_pass)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_pass)
    # кнопка 3
        self.ico_btn_calib = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_calib = AQ_ToolButton('Calibration', self.ico_btn_calib)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_calib)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.proxy_lay.addLayout(self.group_layout)


class AQ_archieve_group(AQ_toolbar_group_template):
    def __init__(self, parent=None):
        super().__init__(parent)
    # кнопка 1
        self.ico_btn_save_log = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn_save_log = AQ_ToolButton('Save log data', self.ico_btn_save_log)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_save_log)
    # кнопка 2
        self.ico_btn_log_settings = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.btn__log_settings = AQ_ToolButton('Data logging settings', self.ico_btn_log_settings)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn__log_settings)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.proxy_lay.addLayout(self.group_layout)



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

