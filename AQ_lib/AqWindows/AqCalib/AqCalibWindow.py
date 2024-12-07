from functools import partial

from PySide6.QtCore import Signal

from AQ_EventManager import AQ_EventManager
from AqCalibCreator import AqCalibCreator
from AqCalibrator import AqCalibrator
from AqMessageManager import AqMessageManager
from AqTranslateManager import AqTranslateManager
from AqWindowTemplate import AqDialogTemplate


class AqCalibWidget(AqDialogTemplate):

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.minimizeBtnEnable = False
        self.maximizeBtnEnable = False

        self.name = 'Calibration'
        self.event_manager = AQ_EventManager.get_global_event_manager()

    def set_calib_device(self, device):
        self.event_manager.emit_event('set_calib_device', device)


