from PySide6.QtWidgets import QLineEdit

from AqBaseDevice import AqBaseDevice
from AqTranslateManager import AqTranslateManager
from AqWindowTemplate import AqDialogTemplate


class AqSetPasswordWindow(AqDialogTemplate):

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.minimizeBtnEnable = False
        self.maximizeBtnEnable = False

        self._password = None
        self._workingDevice = None

        self.name = AqTranslateManager.tr('Set password')
        self.prepare_ui()

    def prepare_ui(self):
        self.ui.passwordFrame.prepare_ui()
        self.ui.passwordFrame.uiChanged.connect(self.resize_by_ui_changed)
        self.ui.passwordFrame.newPasswordReady.connect(self.write_new_password)
        self.ui.passwordFrame.close_signal.connect(self.close)

    def set_working_device(self, device: AqBaseDevice):
        self._workingDevice = device
        self._password = self._workingDevice.get_password()
        self.ui.passwordFrame.load_password(self._password)

    def resize_by_ui_changed(self):
        new_height = self.ui.headerFrame.sizeHint().height() + \
            self.ui.centerFrame.sizeHint().height() + \
            self.ui.footerFrame.sizeHint().height() + self.ui_title.toolboxFrame.height() + 20
        self.setMinimumHeight(new_height)
        self.resize_MainWindow('%', '%', '%', new_height)

    def write_new_password(self, new_password):
        self._workingDevice.write_password(new_password)
        self.close()
