from PySide6.QtCore import QCoreApplication

import AqUiWorker
from Custom_Widgets import QMainWindow, loadJsonStyle
from AQ_EventManager import AQ_EventManager
from AppCore import Core
from ui_form import Ui_MainWindow

version_path = "version.txt"


class AqMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui)

        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.event_manager = AQ_EventManager.get_global_event_manager()
        try:
            with open(version_path, 'r') as file:
                version_str = file.read()
        except:
            version_str = 'unknown version'

        self.ui.TitleName.setText(self.windowTitle() + ' ' + version_str)
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())
        self.ui.deviceInfoBtn.clicked.connect(AqUiWorker.show_device_info_window)
        self.ui.paramListBtn.clicked.connect(AqUiWorker.show_device_param_list)
        self.ui.watchListBtn.clicked.connect(AqUiWorker.show_watch_list_window)
        self.ui.setSlaveIdBtn.clicked.connect(AqUiWorker.show_set_slave_id_window)

        self.ui.setDefaultMenuBtn.clicked.connect(Core.session.set_default_cur_active_device)
        self.ui.rebootDeviceBtn.clicked.connect(Core.session.restart_current_active_device)

        self.ui.readParamMenuBtn.clicked.connect(Core.session.read_params_cur_active_device)
        self.ui.writeParamMenuBtn.clicked.connect(Core.session.write_params_cur_active_device)

        Core.session.cur_active_dev_changed.connect(self.floating_menu_customize)

        # TODO: тимчасове, потім видалити
        self.ui.headerMenuFrame.hide()

    def floating_menu_customize(self):
        device = Core.session.cur_active_device
        if device.func('rtc'):
            self.ui.setRtcBtn.setEnabled(True)
        else:
            self.ui.setRtcBtn.setEnabled(False)

        if device.func('password'):
            self.ui.setPasswordBtn.setEnabled(True)
        else:
            self.ui.setPasswordBtn.setEnabled(False)

        if device.func('calibration'):
            self.ui.calibDeviceBtn.setEnabled(True)
        else:
            self.ui.calibDeviceBtn.setEnabled(False)

        if device.func('set_slave_id'):
            self.ui.setSlaveIdBtn.setEnabled(True)
        else:
            self.ui.setSlaveIdBtn.setEnabled(False)

        if device.func('log'):
            self.ui.saveLogBtn.setEnabled(True)
            self.ui.configLogBtn.setEnabled(True)
        else:
            self.ui.saveLogBtn.setEnabled(False)
            self.ui.configLogBtn.setEnabled(False)

        if device.func('fw_update'):
            self.ui.firmwareUpdBtn.setEnabled(True)
        else:
            self.ui.firmwareUpdBtn.setEnabled(False)

        if device.func('restart'):
            self.ui.rebootDeviceBtn.setEnabled(True)
        else:
            self.ui.rebootDeviceBtn.setEnabled(False)

    def close(self):
        super().close()
        Core.de_init()
        QCoreApplication.quit()
