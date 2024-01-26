from PySide6.QtWidgets import QFrame, QCheckBox, QLabel


class AqScanCheckBoxFrame(QFrame):
    child_buttons = None
    def __init__(self, parent):
        super().__init__(parent)
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
