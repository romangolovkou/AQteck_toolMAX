from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from AQ_ToolbarButton import AQ_ToolButton

PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'


class AQ_toolbar_group_template(QWidget):
    def __init__(self, event_manager, parent=None):
        super().__init__(parent)
        self.event_manager = event_manager
        self.buttons = []
        self.group_layout = 0
        self.setMinimumSize(60, 60)
        self.proxy_lay = QHBoxLayout(self)
        self.proxy_lay.setContentsMargins(0, 2, 0, 2)
        self.setLayout(self.proxy_lay)
        self.cur_oriental = 0 # 0-Горизонтально, 1-Вертикально

    def change_oriental(self):
        cur_group_layout = self.proxy_lay.itemAt(0)
        if isinstance(cur_group_layout, QHBoxLayout):
            self.proxy_lay.removeItem(cur_group_layout)
            self.group_layout = Group_LayV(self, *self.buttons)
            self.proxy_lay.addLayout(self.group_layout)
            self.cur_oriental = 1
            cur_group_layout.deleteLater()
        elif isinstance(cur_group_layout, QVBoxLayout):
            self.proxy_lay.removeItem(cur_group_layout)
            self.group_layout = Group_LayH(self, *self.buttons)
            self.proxy_lay.addLayout(self.group_layout)
            self.cur_oriental = 0
            cur_group_layout.deleteLater()

    def get_cur_oriental(self):
        return self.cur_oriental


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


class AQ_device_action_group(AQ_toolbar_group_template):
    def __init__(self, event_manager, parent=None):
        super().__init__(event_manager, parent)
    # кнопка 1
        self.ico_btn_add_devise = QIcon('Icons/Add_device.png')
        self.btn_add_devices = AQ_ToolButton('Add Devices', self.ico_btn_add_devise)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.btn_add_devices.clicked.connect(lambda: self.event_manager.emit_event('open_AddDevices'))
        self.buttons.append(self.btn_add_devices)
    # кнопка 2
        self.ico_btn_delete_device = QIcon('Icons/Delete_device.png')
        self.btn_delete_devices = AQ_ToolButton('Delete Devices', self.ico_btn_delete_device)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.btn_delete_devices.clicked.connect(lambda: self.event_manager.emit_event('delete_cur_active_device'))
        self.buttons.append(self.btn_delete_devices)
    # кнопка 3
    #     self.ico_btn_ip_adresses = QIcon('Icons/ip_adresses.png')
    #     self.btn_ip_adresses = AQ_ToolButton('IP Addresses', self.ico_btn_ip_adresses)
    #     # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
    #     self.buttons.append(self.btn_ip_adresses)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.proxy_lay.addLayout(self.group_layout)


class AQ_param_action_group(AQ_toolbar_group_template):
    def __init__(self, event_manager, parent=None):
        super().__init__(event_manager, parent)
    # кнопка 1
        self.ico_btn_read = QIcon('Icons/test_Button.png')
        self.btn_read = AQ_ToolButton('Read parameters', self.ico_btn_read)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.btn_read.clicked.connect(lambda: self.event_manager.emit_event('read_params_cur_active_device'))
        self.buttons.append(self.btn_read)
    # кнопка 2
        self.ico_btn_write = QIcon('Icons/test_Button.png')
        self.btn_write = AQ_ToolButton('Write parameters', self.ico_btn_write)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.btn_write.clicked.connect(lambda: self.event_manager.emit_event('write_params_cur_active_device'))
        self.buttons.append(self.btn_write)
    # кнопка 3
    #     self.ico_btn_factory_settings = QIcon('Icons/test_Button.png')
    #     self.btn_factory_settings = AQ_ToolButton('Factory settings', self.ico_btn_factory_settings)
    #     # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
    #     self.buttons.append(self.btn_factory_settings)
    # кнопка 4
    #     self.ico_btn_watch_list = QIcon('Icons/test_Button.png')
    #     self.btn_watch_list = AQ_ToolButton('Watch list', self.ico_btn_watch_list)
    #     # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
    #     self.btn_watch_list.clicked.connect(lambda: self.event_manager.emit_event('open_WatchList'))
    #     self.buttons.append(self.btn_watch_list)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.proxy_lay.addLayout(self.group_layout)


class AQ_utils_group(AQ_toolbar_group_template):
    def __init__(self, event_manager, parent=None):
        super().__init__(event_manager, parent)
    # кнопка 1
        self.ico_btn_set_slave_id = QIcon('Icons/test_Button.png')
        self.btn_set_slave_id = AQ_ToolButton('Set slave id', self.ico_btn_set_slave_id)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.btn_set_slave_id.clicked.connect(lambda: self.event_manager.emit_event('open_SetSlaveId'))
        self.buttons.append(self.btn_set_slave_id)
    # # кнопка 1
    #     self.ico_btn_rtc = QIcon('Icons/test_Button.png')
    #     self.btn_rtc = AQ_ToolButton('Real-time clock', self.ico_btn_rtc)
    #     # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
    #     # self.btn_rtc.clicked.connect(self.change_oriental)
    #     self.buttons.append(self.btn_rtc)
    # # кнопка 2
    #     self.ico_btn_pass = QIcon('Icons/test_Button.png')
    #     self.btn_pass = AQ_ToolButton('Password', self.ico_btn_pass)
    #     # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
    #     self.buttons.append(self.btn_pass)
    # # кнопка 3
    #     self.ico_btn_calib = QIcon('Icons/test_Button.png')
    #     self.btn_calib = AQ_ToolButton('Calibration', self.ico_btn_calib)
    #     # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
    #     self.buttons.append(self.btn_calib)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.proxy_lay.addLayout(self.group_layout)


class AQ_archieve_group(AQ_toolbar_group_template):
    def __init__(self, event_manager, parent=None):
        super().__init__(event_manager, parent)
    # кнопка 1
        self.ico_btn_save_log = QIcon('Icons/test_Button.png')
        self.btn_save_log = AQ_ToolButton('Save log data', self.ico_btn_save_log)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_save_log)
    # кнопка 2
        self.ico_btn_log_settings = QIcon('Icons/test_Button.png')
        self.btn_log_settings = AQ_ToolButton('Data logging settings', self.ico_btn_log_settings)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_log_settings)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.proxy_lay.addLayout(self.group_layout)


class AQ_firmware_group(AQ_toolbar_group_template):
    def __init__(self, event_manager, parent=None):
        super().__init__(event_manager, parent)
    # кнопка 1
        self.ico_btn_fw_upd_loc = QIcon('Icons/test_Button.png')
        self.btn_fw_upd_loc = AQ_ToolButton('Firmware update local', self.ico_btn_fw_upd_loc)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_fw_upd_loc)
    # кнопка 2
        self.ico_btn_fw_upd_onl = QIcon('Icons/test_Button.png')
        self.btn_fw_upd_onl = AQ_ToolButton('Firmware update online', self.ico_btn_fw_upd_onl)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.buttons.append(self.btn_fw_upd_onl)
    # кнопка 3
        self.ico_btn_reboot = QIcon('Icons/test_Button.png')
        self.btn_reboot = AQ_ToolButton('Restart device', self.ico_btn_reboot)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.btn_reboot.clicked.connect(lambda: self.event_manager.emit_event('restart_cur_active_device'))
        self.buttons.append(self.btn_reboot)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.proxy_lay.addLayout(self.group_layout)


class AQ_other_group(AQ_toolbar_group_template):
    def __init__(self, event_manager, parent=None):
        super().__init__(event_manager, parent)
    # кнопка 1
        self.ico_btn_param_list = QIcon('Icons/test_Button.png')
        self.btn_param_list = AQ_ToolButton('Parameter list', self.ico_btn_param_list)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.btn_param_list.clicked.connect(lambda: self.event_manager.emit_event('open_ParameterList'))
        self.buttons.append(self.btn_param_list)
    # кнопка 2
        self.ico_btn_device_info = QIcon('Icons/test_Button.png')
        self.btn_device_info = AQ_ToolButton('Device information', self.ico_btn_device_info)
        # тут вставить привязку к функции self.btn_add_devices.clicked.connect(???)
        self.btn_device_info.clicked.connect(lambda: self.event_manager.emit_event('open_DeviceInfo'))
        self.buttons.append(self.btn_device_info)

    # Створюємо початковий горизонтальний лейаут
        self.group_layout = Group_LayH(self, *self.buttons)
        self.proxy_lay.addLayout(self.group_layout)





