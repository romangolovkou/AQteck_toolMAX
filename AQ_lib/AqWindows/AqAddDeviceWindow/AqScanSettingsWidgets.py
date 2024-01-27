from PySide6.QtWidgets import QFrame, QCheckBox, QLabel, QLineEdit


class AqScanCheckBoxFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.child_buttons = None
        self.warning_label = QLabel('Check something!', self.parent())
        self.warning_label.setStyleSheet("color: #fe2d2d; \n")
        self.warning_label.setFixedSize(100, 20)
        self.warning_label.hide()

    def prepare_ui(self):
        self.child_buttons = self.findChildren(QCheckBox)

        for child_btn in self.child_buttons:
            child_btn.clicked.connect(self.check_buttons_selected)

    def check_buttons_selected(self):
        have_checked = False
        for child_btn in self.child_buttons:
            if child_btn.isChecked():
                have_checked = True

        if have_checked is False:
            self.show_warning()
        else:
            self.hide_warning()

    def show_warning(self):
        rect = self.geometry()
        pos = self.mapTo(self, rect.topRight())
        self.warning_label.move(pos.x() - 105, pos.y())
        self.warning_label.show()

    def hide_warning(self):
        self.warning_label.hide()

class AqScanSlaveIDFrame(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.startLineEdit = None
        self.endLineEdit = None
        self.slaveIdWarningMsgLabel = None
        self.warning_label = QLabel('End address cannot be less than start address!', self)
        self.warning_label.setStyleSheet("color: #fe2d2d; \n")
        self.warning_label.setFixedSize(250, 20)
        self.warning_label.move(10, 55)
        self.warning_label.hide()

    def prepare_ui(self):
        self.startLineEdit = self.findChildren(QLineEdit, 'startLineEdit')[0]
        self.endLineEdit = self.findChildren(QLineEdit, 'endLineEdit')[0]

        self.startLineEdit.textChanged.connect(self.line_edit_changed)
        self.endLineEdit.textChanged.connect(self.line_edit_changed)

    def line_edit_changed(self):
        start = self.startLineEdit.text()
        end = self.endLineEdit.text()
        if start != '' and end != '':
            if int(start) > int(end):
                self.show_warning()
            else:
                self.hide_warning()

    def show_warning(self):
        self.warning_label.show()

    def hide_warning(self):
        self.warning_label.hide()
