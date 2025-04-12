from PySide2.QtWidgets import QFrame, QPushButton, QLineEdit


class AqPasswordLineEditFrame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.showPassBtn = None
        self.passLineEdit = None

    def prepare_ui(self):
        self.showPassBtn = self.findChild(QPushButton)
        self.passLineEdit = self.findChild(QLineEdit)
        self.passLineEdit.setEchoMode(QLineEdit.Password)
        self.showPassBtn.toggled.connect(self.toggle_password_visibility)

    def toggle_password_visibility(self, checked):
        if checked:
            self.passLineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.passLineEdit.setEchoMode(QLineEdit.Password)

    def text(self):
        return self.passLineEdit.text()
