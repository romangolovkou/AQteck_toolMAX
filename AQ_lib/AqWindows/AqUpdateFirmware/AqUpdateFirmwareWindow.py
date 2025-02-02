from AQ_EventManager import AQ_EventManager
from AqWindowTemplate import AqDialogTemplate


class AqUpdateFirmwareWidget(AqDialogTemplate):

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.minimizeBtnEnable = False
        self.maximizeBtnEnable = False

        self.name = 'Firmware update'
        self.event_manager = AQ_EventManager.get_global_event_manager()

    # def set_calib_device(self, device):
    #     self.event_manager.emit_event('set_calib_device', device)


