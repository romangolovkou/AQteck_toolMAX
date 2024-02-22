from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QLineEdit, QRadioButton


class AqPasswordFrame(QFrame):
    uiChanged = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_ui_elements = None
        self._password = None

        self.currentPassLabel = None
        self.currentPassLineFrame = None
        self.newPassLabel = None
        self.newPassLineFrame = None
        self.rNewPassLabel = None
        self.rNewPassLineFrame = None
        self.resetBtn = None
        self.createBtn = None
        self.changeBtn = None
        self.createRadioBtn = None
        self.resetRadioBtn = None
        self.currentPassLineEdit = None
        self.newPassLineEdit = None
        self.rNewPassLineEdit = None
        self.wrongPassLabel = None
        self.notMatchLabel = None

    def prepare_ui(self):
        self.currentPassLabel = self.findChild(QLabel, 'currentPassLabel')
        self.currentPassLineFrame = self.findChild(QFrame, 'currentPassLineFrame')
        self.newPassLabel = self.findChild(QLabel, 'newPassLabel')
        self.newPassLineFrame = self.findChild(QFrame, 'newPassLineFrame')
        self.rNewPassLabel = self.findChild(QLabel, 'rNewPassLabel')
        self.rNewPassLineFrame = self.findChild(QFrame, 'rNewPassLineFrame')
        self.resetBtn = self.findChild(QPushButton, 'resetBtn')
        self.createBtn = self.findChild(QPushButton, 'createBtn')
        self.changeBtn = self.findChild(QPushButton, 'changeBtn')
        self.createRadioBtn = self.findChild(QRadioButton, 'createRadioBtn')
        self.resetRadioBtn = self.findChild(QRadioButton, 'resetRadioBtn')
        self.currentPassLineEdit = self.findChild(QLineEdit, 'currentPassLineEdit')
        self.newPassLineEdit = self.findChild(QLineEdit, 'newPassLineEdit')
        self.rNewPassLineEdit = self.findChild(QLineEdit, 'rNewPassLineEdit')
        self.wrongPassLabel = self.findChild(QLabel, 'wrongPassLabel')
        self.notMatchLabel = self.findChild(QLabel, 'notMatchLabel')

        self.main_ui_elements = [
                self.currentPassLabel,
                self.currentPassLineFrame,
                self.newPassLabel,
                self.newPassLineFrame,
                self.rNewPassLabel,
                self.rNewPassLineFrame,
                self.resetBtn,
                self.createBtn,
                self.changeBtn,
                self.createRadioBtn,
                self.resetRadioBtn,
                self.currentPassLineEdit,
                self.newPassLineEdit,
                self.rNewPassLineEdit,
                self.wrongPassLabel,
                self.notMatchLabel
            ]

        for i in self.main_ui_elements:
            if i is None:
                raise Exception(self.objectName() + ' Error: lost UI element: ')

        self.wrongPassLabel.hide()
        self.notMatchLabel.hide()
        self.createRadioBtn.clicked.connect(self.change_ui_by_selected_mode)
        self.resetRadioBtn.clicked.connect(self.change_ui_by_selected_mode)
        self.currentPassLineFrame.prepare_ui()
        self.newPassLineFrame.prepare_ui()
        self.rNewPassLineFrame.prepare_ui()

    def load_password(self, new_pass):
        self._password = new_pass
        self.createRadioBtn.setChecked(True)
        if self._password is None or self._password == '':
            self.resetRadioBtn.setEnabled(False)
            self.resetRadioBtn.setToolTip('Nothing to reset, the device is now without a password')
            self.show_create_if()
        else:
            self.resetRadioBtn.setToolTip(None)
            self.show_change_if()

    def change_ui_by_selected_mode(self):
        if self.resetRadioBtn.isChecked():
            self.show_reset_if()
        else:
            if self._password is None or self._password == '':
                self.show_create_if()
            else:
                self.show_change_if()

        self.uiChanged.emit()

        # new_height = self.ui.headerFrame.sizeHint().height() + \
        #     self.ui.centerFrame.sizeHint().height() + \
        #     self.ui.footerFrame.sizeHint().height() + self.ui_title.toolboxFrame.height() + 20
        # self.setMinimumHeight(new_height)
        # self.resize_MainWindow('%', '%', '%', new_height)
        
    def show_reset_if(self):
        self.currentPassLabel.show()
        self.currentPassLineFrame.show()
        self.newPassLabel.hide()
        self.newPassLineFrame.hide()
        self.rNewPassLabel.hide()
        self.rNewPassLineFrame.hide()

        self.resetBtn.show()
        self.createBtn.hide()
        self.changeBtn.hide()

    def show_create_if(self):
        self.currentPassLabel.hide()
        self.currentPassLineFrame.hide()
        self.newPassLabel.show()
        self.newPassLineFrame.show()
        self.rNewPassLabel.show()
        self.rNewPassLineFrame.show()

        self.resetBtn.hide()
        self.createBtn.show()
        self.changeBtn.hide()

    def show_change_if(self):
        self.currentPassLabel.show()
        self.currentPassLineFrame.show()
        self.newPassLabel.show()
        self.newPassLineFrame.show()
        self.rNewPassLabel.show()
        self.rNewPassLineFrame.show()

        self.resetBtn.hide()
        self.createBtn.hide()
        self.changeBtn.show()
        