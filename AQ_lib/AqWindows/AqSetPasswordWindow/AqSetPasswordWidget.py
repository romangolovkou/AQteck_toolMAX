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

    #     self.ui.createRadioBtn.clicked.connect(self.change_ui_by_selected_mode)
    #     self.ui.resetRadioBtn.clicked.connect(self.change_ui_by_selected_mode)
    #     self.ui.currentPassLineEdit.setEchoMode(QLineEdit.Password)
    #     self.ui.newPassLineEdit.setEchoMode(QLineEdit.Password)
    #     self.ui.rNewPassLineEdit.setEchoMode(QLineEdit.Password)
    #     self.ui.showCurPassBtn.toggled.connect(self.toggle_password_visibility)
    #     self.ui.showNewPassBtn.toggled.connect(self.toggle_password_visibility)
    #     self.ui.showRNewPassBtn.toggled.connect(self.toggle_password_visibility)

    def load_password(self, new_pass):
        self.ui.passwordFrame.load_password(new_pass)
        # self._password = new_pass
        # # self.ui.passwordFrame.password = new_pass
        # self.ui.createRadioBtn.setChecked(True)
        # if self._password is None or self._password == '':
        #     self.ui.resetRadioBtn.setEnabled(False)
        #     self.ui.resetRadioBtn.setToolTip('Nothing to reset, the device is now without a password')
        #     self.show_create_if()
        # else:
        #     self.ui.resetRadioBtn.setToolTip(None)
        #     self.show_change_if()

    # def change_ui_by_selected_mode(self):
    #     if self.ui.resetRadioBtn.isChecked():
    #         self.show_reset_if()
    #     else:
    #         if self._password is None or self._password == '':
    #             self.show_create_if()
    #         else:
    #             self.show_change_if()
    #
    def resize_by_ui_changed(self):
        new_height = self.ui.headerFrame.sizeHint().height() + \
            self.ui.centerFrame.sizeHint().height() + \
            self.ui.footerFrame.sizeHint().height() + self.ui_title.toolboxFrame.height() + 20
        self.setMinimumHeight(new_height)
        self.resize_MainWindow('%', '%', '%', new_height)

    # def show_reset_if(self):
    #     self.ui.currentPassLabel.show()
    #     self.ui.currentPassFrame.show()
    #     self.ui.newPassLabel.hide()
    #     self.ui.rNewPassLabel.hide()
    #     self.ui.newPassFrame.hide()
    #     self.ui.rNewPassFrame.hide()
    #
    #     self.ui.resetBtn.show()
    #     self.ui.createBtn.hide()
    #     self.ui.changeBtn.hide()
    #
    # def show_create_if(self):
    #     self.ui.currentPassLabel.hide()
    #     self.ui.currentPassFrame.hide()
    #     self.ui.newPassLabel.show()
    #     self.ui.rNewPassLabel.show()
    #     self.ui.newPassFrame.show()
    #     self.ui.rNewPassFrame.show()
    #
    #     self.ui.resetBtn.hide()
    #     self.ui.createBtn.show()
    #     self.ui.changeBtn.hide()
    #
    # def show_change_if(self):
    #     self.ui.currentPassLabel.show()
    #     self.ui.currentPassFrame.show()
    #     self.ui.newPassLabel.show()
    #     self.ui.rNewPassLabel.show()
    #     self.ui.newPassFrame.show()
    #     self.ui.rNewPassFrame.show()
    #
    #     self.ui.resetBtn.hide()
    #     self.ui.createBtn.hide()
    #     self.ui.changeBtn.show()

    # def toggle_password_visibility(self, checked):
    #     if checked:
    #         self.sender().setEchoMode(QLineEdit.Normal)
    #     else:
    #         self.sender().setEchoMode(QLineEdit.Password)
