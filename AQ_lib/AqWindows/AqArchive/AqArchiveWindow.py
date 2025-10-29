from functools import partial

from PySide6.QtCore import Signal, Qt

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

        self.ui.logSetSettingsBtn.clicked.connect(self.write_logging_settings)

        self.device = None
        self.log_settings = None

        self._params_dict_from_tree = {}
        self._ui_edit_lines_dict = {}
        self._settings_values = {}

    def set_logging_device(self, device):
        # self.event_manager.emit_event('set_logging_device', device)
        self.device = device
        self.log_settings = self.device.get_log_settings()
        if self.log_settings is not None:
            self.ui.logIntervalLineEdit.setText(str(self.log_settings['log_interval']))
            self._ui_edit_lines_dict['log_interval'] = self.ui.logIntervalLineEdit
            self.ui.logNumberFilesLineEdit.setText(str(self.log_settings['log_num_files']))
            self._ui_edit_lines_dict['log_num_files'] = self.ui.logNumberFilesLineEdit
            self.ui.logFileSizeLineEdit.setText(str(self.log_settings['log_file_size']))
            self._ui_edit_lines_dict['log_file_size'] = self.ui.logFileSizeLineEdit

        self.ui.devNameLabel.setText(self.device.name)
        self.ui.devSnLabel.setText('S/N' + self.device.info('serial_num'))

        for key in self.log_settings.keys():
            item = self.device.system_params_dict[key]
            param_attributes = item.data(Qt.UserRole)
            self._params_dict_from_tree[key] = self.device.get_item_by_modbus_reg(param_attributes['modbus_reg'])
            param_attributes = self._params_dict_from_tree[key].data(Qt.UserRole)
            self._ui_edit_lines_dict[key].min_limit = param_attributes['min_limit']
            self._ui_edit_lines_dict[key].max_limit = param_attributes['max_limit']

    def write_logging_settings(self):
        try:
            interval = int(self.ui.logIntervalLineEdit.text())
            num_files = int(self.ui.logNumberFilesLineEdit.text())
            file_size = int(self.ui.logFileSizeLineEdit.text())
        except:
            self._message_manager.send_message('LogDevice', "Error", AqTranslateManager.tr('Values must be an UINT'))
            return None

        if isinstance(interval, int) and isinstance(num_files, int) and isinstance(file_size, int):
            settings_dict = {'log_interval': interval, 'log_num_files': num_files, 'log_file_size': file_size}
        else:
            self._message_manager.send_message('LogDevice', "Error", AqTranslateManager.tr('Values must be an UINT'))
            return None

        items_to_write = list()
        for key in settings_dict.keys():
            if settings_dict[key] < self._ui_edit_lines_dict[key].min_limit or \
                    settings_dict[key] > self._ui_edit_lines_dict[key].max_limit:
                self._message_manager.send_message('LogDevice', "Error",
                                                   AqTranslateManager.tr('Value') + ' ' +
                                                   key[4:] + ' ' +
                                                   AqTranslateManager.tr('less or more than permissible'))
                return None

            item = self._params_dict_from_tree[key]
            item.value = settings_dict[key]
            item.param_status = 'changed'
            items_to_write.append(item)

        self.device.write_parameters(items_to_write, message_feedback_address='LogDevice')

    def close(self):
        # self.event_manager.unregister_event_handler('DeviceLog', self.close_btn_block)
        AqWatchListCore.set_pause_flag(False)
        super().close()
