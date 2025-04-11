from functools import partial

from PySide6.QtCore import Signal

from AQ_EventManager import AQ_EventManager
from AqMessageManager import AqMessageManager
from AqTranslateManager import AqTranslateManager
from AqWatchListCore import AqWatchListCore
from AqWindowTemplate import AqDialogTemplate


class AqArchiveWidget(AqDialogTemplate):
    message_signal = Signal(str, str)

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.minimizeBtnEnable = False
        self.maximizeBtnEnable = False
        AqWatchListCore.set_pause_flag(True)

        self.name = AqTranslateManager.tr('Log')
        self.event_manager = AQ_EventManager.get_global_event_manager()
        # self.event_manager.register_event_handler('DeviceLog', self.close_btn_block)

        self._message_manager = AqMessageManager.get_global_message_manager()

        self.message_signal.connect(partial(self._message_manager.show_message, self))
        self._message_manager.subscribe('LogDevice', self.message_signal.emit)

        self.ui.logSetSettingsBtn.clicked.connect()

        self.device = None
        self.log_settings = None

    def set_logging_device(self, device):
        # self.event_manager.emit_event('set_logging_device', device)
        self.device = device
        self.log_settings = self.device.get_log_settings()
        if self.log_settings is not None:
            self.ui.logIntervalLineEdit.setValue(self.log_settings['log_interval'])
            self.ui.logNumberFilesLineEdit.setValue(self.log_settings['log_num_files'])
            self.ui.logFileSizeLineEdit.setValue(self.log_settings['log_file_size'])

    def write_logging_settings(self):
        interval = self.ui.logIntervalLineEdit.text()
        num_files = self.ui.logNumberFilesLineEdit.text()
        file_size = self.ui.logFileSizeLineEdit.text()

        if isinstance(interval, int) and isinstance(num_files, int) and isinstance(file_size, int):
            settings_dict = {'log_interval': interval, 'log_num_files': num_files, 'log_file_size': file_size}
        else:
            return None

    # def close_btn_block(self, value):
    #     self.ui_title.closeBtn.setEnabled(not value)

    def close(self):
        # self.event_manager.unregister_event_handler('DeviceLog', self.close_btn_block)
        AqWatchListCore.set_pause_flag(False)
        super().close()
