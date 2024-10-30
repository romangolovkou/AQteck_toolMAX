from AQ_EventManager import AQ_EventManager
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

        # Підготовка необхідних полів UI
        # self.prepare_ui_objects()

