from functools import partial

from PySide6.QtCore import QCoreApplication, Signal
from PySide6.QtGui import QKeySequence, QShortcut

import AqUiWorker
from AqSettingsFunc import AqSettingsManager
from AqTranslateManager import AqTranslateManager
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
        AqTranslateManager.subscribe(self.retranslate)

        loadJsonStyle(self, self.ui)

        self.event_manager = AQ_EventManager.get_global_event_manager()
        try:
            with open(version_path, 'r') as file:
                self.version_str = file.read()
        except:
            self.version_str = 'unknown'

        self.ui.TitleName.setText(self.windowTitle())
        # self.ui.versionLabel.setText(QCoreApplication.translate("Custom context", u"Version", None))
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())
        self.ui.langComboBox.currentTextChanged.connect(self.lang_change)
        AqSettingsManager.load_last_combobox_state(self.ui.langComboBox)
        self.ui.deviceInfoBtn.clicked.connect(AqUiWorker.show_device_info_window)
        self.ui.paramListBtn.clicked.connect(AqUiWorker.show_device_param_list)
        self.ui.watchListBtn.clicked.connect(AqUiWorker.show_watch_list_window)
        self.ui.setSlaveIdBtn.clicked.connect(AqUiWorker.show_set_slave_id_window)
        self.ui.setRtcBtn.clicked.connect(AqUiWorker.show_set_rtc)
        self.ui.setPasswordBtn.clicked.connect(AqUiWorker.show_set_password)
        self.ui.gatewayBtn.clicked.connect(AqUiWorker.show_gateway)
        self.ui.calibDeviceBtn.clicked.connect(AqUiWorker.show_calib_window)
        self.ui.firmwareUpdBtn.clicked.connect(AqUiWorker.show_update_fw_window)
        self.ui.saveLogBtn.clicked.connect(AqUiWorker.show_archive_window)

        self.ui.setDefaultMenuBtn.clicked.connect(self.setFocus)
        self.ui.setDefaultMenuBtn.clicked.connect(Core.session.set_default_cur_active_device)
        self.ui.rebootDeviceBtn.clicked.connect(Core.session.restart_current_active_device)

        self.ui.readParamMenuBtn.clicked.connect(self.setFocus)
        self.ui.readParamMenuBtn.clicked.connect(Core.session.read_params_cur_active_device)
        self.ui.writeParamMenuBtn.clicked.connect(Core.session.write_params_cur_active_device)

        Core.session.cur_active_dev_changed.connect(self.floating_menu_customize)

        # TODO: тимчасове, потім видалити
        self.ui.headerMenuFrame.hide()
        self.ui.configLogBtn.hide()

        self.message_signal.connect(partial(Core.message_manager.show_message, self))
        Core.message_manager.subscribe('main', self.message_signal.emit)

        self.retranslate()

        # Відключення кнопок утіліт до відображення першого девайсу

        #Hot keys
        self.shortcut_calib_develop = QShortcut(QKeySequence("F8"), self)
        self.shortcut_calib_develop.activated.connect(lambda: AqUiWorker.show_calib_window(True))

    def retranslate(self):
        self.ui.retranslateUi(self)
        # tr_string = QCoreApplication.translate("Custom context", u"Version", None)
        tr_string = AqTranslateManager.tr('Version')
        self.ui.versionLabel.setText(tr_string + ' ' + self.version_str)

    def lang_change(self, lang):
        AqSettingsManager.save_combobox_current_state(self.ui.langComboBox)
        AqTranslateManager.set_current_lang(lang)

    def floating_menu_customize(self):
        device = Core.session.cur_active_device
        if device.func('rtc'):
            self.ui.setRtcBtn.setEnabled(True)
            self.ui.setRtcBtn.setToolTip(None)
        else:
            self.ui.setRtcBtn.setEnabled(False)
            self.ui.setRtcBtn.setToolTip(AqTranslateManager.tr('Not available for this device'))

        if device.func('password'):
            self.ui.setPasswordBtn.setEnabled(True)
            self.ui.setPasswordBtn.setToolTip(None)
        else:
            self.ui.setPasswordBtn.setEnabled(False)
            self.ui.setPasswordBtn.setToolTip(AqTranslateManager.tr('Not available for this device'))

        if device.func('gateway'):
            self.ui.gatewayBtn.setEnabled(True)
            self.ui.gatewayBtn.setToolTip(None)
        else:
            self.ui.gatewayBtn.setEnabled(False)
            self.ui.gatewayBtn.setToolTip(AqTranslateManager.tr('Not available for this device'))

        if device.func('calibration'):
            self.ui.calibDeviceBtn.setEnabled(True)
            self.ui.calibDeviceBtn.setToolTip(None)
        else:
            self.ui.calibDeviceBtn.setEnabled(False)
            self.ui.calibDeviceBtn.setToolTip(AqTranslateManager.tr('Not available for this device'))

        if device.func('set_slave_id'):
            self.ui.setSlaveIdBtn.setEnabled(True)
            self.ui.setSlaveIdBtn.setToolTip(None)
        else:
            self.ui.setSlaveIdBtn.setEnabled(False)
            self.ui.setSlaveIdBtn.setToolTip(AqTranslateManager.tr('Not available for this device'))

        if device.func('log'):
            self.ui.saveLogBtn.setEnabled(True)
            self.ui.saveLogBtn.setToolTip(None)
            self.ui.configLogBtn.setEnabled(True)
            self.ui.configLogBtn.setToolTip(None)
        else:
            self.ui.saveLogBtn.setEnabled(False)
            self.ui.saveLogBtn.setToolTip(AqTranslateManager.tr('Not available for this device'))
            self.ui.configLogBtn.setEnabled(False)
            self.ui.configLogBtn.setToolTip(AqTranslateManager.tr('Not available for this device'))

        if device.func('fw_update'):
            self.ui.firmwareUpdBtn.setEnabled(True)
            self.ui.firmwareUpdBtn.setToolTip(None)
        else:
            self.ui.firmwareUpdBtn.setEnabled(False)
            self.ui.firmwareUpdBtn.setToolTip(AqTranslateManager.tr('Not available for this device'))

        if device.func('restart'):
            self.ui.rebootDeviceBtn.setEnabled(True)
            self.ui.rebootDeviceBtn.setToolTip(None)
        else:
            self.ui.rebootDeviceBtn.setEnabled(False)
            self.ui.rebootDeviceBtn.setToolTip(AqTranslateManager.tr('Not available for this device'))

    def close(self):
        super().close()
        Core.de_init()
        QCoreApplication.quit()
