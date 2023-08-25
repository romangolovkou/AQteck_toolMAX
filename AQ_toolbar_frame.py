from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QDialog, QPushButton, QComboBox, QLineEdit, QProgressBar
from PyQt5.QtCore import Qt, QTimer, QRect, QSize


class AQ_tool_panel_frame(QFrame):
    def __init__(self, shift_y, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(0, shift_y + 2, parent.width(), 90))
        self.setStyleSheet("background-color: #2b2d30;\n"
                           "border-top-left-radius: 0px;\n"
                           "border-top-right-radius: 0px;\n"
                           "border-bottom-left-radius: 0px;\n"
                           "border-bottom-right-radius: 0px;")
        self.setObjectName("tool_panel_frame")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'tool_panel_layout'):
            self.rotate_next_widget(self.tool_panel_layout)

    def rotate_next_widget(self, layout):
        recommended_width = self.sizeHint().width()
        cur_width = self.width()
        for i in range(layout.count()):
            if self.width() < (recommended_width - 50):
                    widest_widget = self.find_widest_Hwidget(layout)
                    if widest_widget is not None:
                        widest_widget.change_oriental()
            elif self.width() >= (recommended_width + 50):
                    most_slim_widget = self.find_most_slim_Vwidget(layout)
                    if most_slim_widget is not None:
                        most_slim_widget.change_oriental()

    def find_widest_Hwidget(self, layout):
        max_width = 0
        widest_widget = None

        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if hasattr(widget, 'get_cur_oriental'):
                if widget.get_cur_oriental() == 0:
                    if item.widget() and item.widget().width() > max_width:
                        max_width = item.widget().width()
                        widest_widget = item.widget()

        return widest_widget

    def find_most_slim_Vwidget(self, layout):
        min_width = float('inf')  # Инициализируем минимальную ширину как бесконечность
        most_slim_widget = None

        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if hasattr(widget, 'get_cur_oriental'):
                if widget.get_cur_oriental() == 1:
                    if item.widget() and item.widget().width() < min_width:
                        min_width = item.widget().width()
                        most_slim_widget = item.widget()

        return most_slim_widget