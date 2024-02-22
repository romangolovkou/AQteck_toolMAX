from PySide6.QtWidgets import QLineEdit

from AqWindowTemplate import AqDialogTemplate


class AqSetPasswordWindow(AqDialogTemplate):

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.maximizeBtnEnable = False

        self._password = None

        self.name = 'Set password'
        self.prepare_ui()

    def prepare_ui(self):
        self.ui.passwordFrame.prepare_ui()
        self.ui.passwordFrame.uiChanged.connect(self.resize_by_ui_changed)

    def load_password(self, new_pass):
        self.ui.passwordFrame.load_password(new_pass)

    def resize_by_ui_changed(self):
        new_height = self.ui.headerFrame.sizeHint().height() + \
            self.ui.centerFrame.sizeHint().height() + \
            self.ui.footerFrame.sizeHint().height() + self.ui_title.toolboxFrame.height() + 20
        self.setMinimumHeight(new_height)
        self.resize_MainWindow('%', '%', '%', new_height)
