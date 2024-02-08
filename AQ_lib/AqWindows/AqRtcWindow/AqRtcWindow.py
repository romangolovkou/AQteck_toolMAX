from AqWindowTemplate import AqDialogTemplate


class AqRtcWindow(AqDialogTemplate):
    """
    Widget require ui.generalInfoFrame and ui.operatingInfoFrame for work
    Check names at your generated Ui
    """

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.maximizeBtnEnable = False

        self.name = 'Set Date Time'
        self.prepare_ui()

    def prepare_ui(self):
        self.ui.secWidget.prepare_ui()
