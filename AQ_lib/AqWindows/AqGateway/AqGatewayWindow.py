from AqWindowTemplate import AqDialogTemplate


class AqGatewayWindow(AqDialogTemplate):

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.maximizeBtnEnable = False

        self.name = 'Gateway'
        self.prepare_ui()

    def prepare_ui(self):
        pass
