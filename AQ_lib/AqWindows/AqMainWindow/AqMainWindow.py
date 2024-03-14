from functools import partial

from PySide6.QtCore import QCoreApplication, Signal

import AqUiWorker
from Custom_Widgets import QMainWindow, loadJsonStyle
from Custom_Widgets.QCustomModals import QCustomModals
from AQ_EventManager import AQ_EventManager
from AppCore import Core
from ui_form import Ui_MainWindow

version_path = "version.txt"


class AqMainWindow(QMainWindow):
    message_signal = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self, self.ui)

        self.event_manager = AQ_EventManager.get_global_event_manager()
        try:
            with open(version_path, 'r') as file:
                version_str = file.read()
        except:
            version_str = 'unknown version'

        self.ui.TitleName.setText(self.windowTitle())
        self.ui.versionLabel.setText('Version ' + version_str)
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())
        self.ui.deviceInfoBtn.clicked.connect(AqUiWorker.show_device_info_window)
        self.ui.paramListBtn.clicked.connect(AqUiWorker.show_device_param_list)
        self.ui.watchListBtn.clicked.connect(AqUiWorker.show_watch_list_window)
        self.ui.setSlaveIdBtn.clicked.connect(AqUiWorker.show_set_slave_id_window)
        self.ui.setRtcBtn.clicked.connect(AqUiWorker.show_set_rtc)
        self.ui.setPasswordBtn.clicked.connect(AqUiWorker.show_set_password)

        self.ui.setDefaultMenuBtn.clicked.connect(Core.session.set_default_cur_active_device)
        self.ui.rebootDeviceBtn.clicked.connect(Core.session.restart_current_active_device)

        self.ui.readParamMenuBtn.clicked.connect(Core.session.read_params_cur_active_device)
        self.ui.writeParamMenuBtn.clicked.connect(Core.session.write_params_cur_active_device)

        Core.session.cur_active_dev_changed.connect(self.floating_menu_customize)

        # TODO: тимчасове, потім видалити
        self.ui.headerMenuFrame.hide()
        self.ui.firmwareUpdBtn.clicked.connect(self.test_modal)

        self.message_signal.connect(partial(Core.message_manager.show_message, self))
        Core.message_manager.subscribe(self.message_signal.emit)



    def test_modal(self):
        myModal = QCustomModals.InformationModal(
            title="Updating dashboard",
            parent=self,
            position='bottom-center',
            closeIcon="Icons/Close.png",
            modalIcon="UI/icons/AQico_silver.png",
            description="Refreshing dashboard information",
            isClosable=True,
            duration=3000
        )
        myModal.show()

    def floating_menu_customize(self):
        device = Core.session.cur_active_device
        if device.func('rtc'):
            self.ui.setRtcBtn.setEnabled(True)
            self.ui.setRtcBtn.setToolTip(None)
        else:
            self.ui.setRtcBtn.setEnabled(False)
            self.ui.setRtcBtn.setToolTip('Not available for this device')

        if device.func('password'):
            self.ui.setPasswordBtn.setEnabled(True)
            self.ui.setPasswordBtn.setToolTip(None)
        else:
            self.ui.setPasswordBtn.setEnabled(False)
            self.ui.setPasswordBtn.setToolTip('Not available for this device')

        if device.func('calibration'):
            self.ui.calibDeviceBtn.setEnabled(True)
            self.ui.calibDeviceBtn.setToolTip(None)
        else:
            self.ui.calibDeviceBtn.setEnabled(False)
            self.ui.calibDeviceBtn.setToolTip('Not available for this device')

        if device.func('set_slave_id'):
            self.ui.setSlaveIdBtn.setEnabled(True)
            self.ui.setSlaveIdBtn.setToolTip(None)
        else:
            self.ui.setSlaveIdBtn.setEnabled(False)
            self.ui.setSlaveIdBtn.setToolTip('Not available for this device')

        if device.func('log'):
            self.ui.saveLogBtn.setEnabled(True)
            self.ui.saveLogBtn.setToolTip(None)
            self.ui.configLogBtn.setEnabled(True)
            self.ui.configLogBtn.setToolTip(None)
        else:
            self.ui.saveLogBtn.setEnabled(False)
            self.ui.saveLogBtn.setToolTip('Not available for this device')
            self.ui.configLogBtn.setEnabled(False)
            self.ui.configLogBtn.setToolTip('Not available for this device')

        if device.func('fw_update'):
            self.ui.firmwareUpdBtn.setEnabled(True)
            self.ui.firmwareUpdBtn.setToolTip(None)
        else:
            self.ui.firmwareUpdBtn.setEnabled(False)
            self.ui.firmwareUpdBtn.setToolTip('Not available for this device')

        if device.func('restart'):
            self.ui.rebootDeviceBtn.setEnabled(True)
            self.ui.rebootDeviceBtn.setToolTip(None)
        else:
            self.ui.rebootDeviceBtn.setEnabled(False)
            self.ui.rebootDeviceBtn.setToolTip('Not available for this device')

    def close(self):
        super().close()
        Core.de_init()
        QCoreApplication.quit()
