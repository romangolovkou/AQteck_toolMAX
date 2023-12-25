from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog
from ui_AqWindowTemplate import Ui_AqWindowTemplate

class AqWindowTemplate(QWidget):
    def __init__(self, widget: QWidget, parent=None):
        super().__init__(parent)
        self._window_name = ''
        self.ui = Ui_AqWindowTemplate()
        self.ui.setupUi(self)
        self.ui.mainWidget = widget
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        getattr(self.ui, "closeBtn").clicked.connect(lambda: self.close())

    @property
    def name(self):
        return self._window_name

    @name.setter
    def name(self, name):
        self._window_name = name
        self.ui.headertext = name


class AqDialogTemplate(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._window_name = ''
        self.ui_title = Ui_AqWindowTemplate()
        self.ui_title.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        getattr(self.ui_title, "closeBtn").clicked.connect(lambda: self.close())

    @property
    def name(self):
        return self._window_name

    @name.setter
    def name(self, name):
        self._window_name = name
        self.ui_title.headertext.setText(name)

    @property
    def content_widget(self):
        return self.ui_title.mainWidget
