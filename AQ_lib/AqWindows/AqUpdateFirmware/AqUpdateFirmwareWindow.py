from PySide2.QtCore import Signal

from AQ_EventManager import AQ_EventManager
from AqTranslateManager import AqTranslateManager
from AqWatchListCore import AqWatchListCore
from AqWindowTemplate import AqDialogTemplate


class AqUpdateFirmwareWidget(AqDialogTemplate):

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.minimizeBtnEnable = False
        self.maximizeBtnEnable = False
        AqWatchListCore.set_pause_flag(True)

        self.name = AqTranslateManager.tr('Firmware update')
        self.event_manager = AQ_EventManager.get_global_event_manager()
        self.event_manager.register_event_handler('FW_update_close_btn_block', self.close_btn_block)

    def set_update_device(self, device):
        self.event_manager.emit_event('set_update_device', device)

    def close_btn_block(self, value):
        self.ui_title.closeBtn.setEnabled(not value)

    def close(self):
        self.event_manager.unregister_event_handler('FW_update_close_btn_block', self.close_btn_block)
        AqWatchListCore.set_pause_flag(False)
        super().close()
