from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QDialog, QPushButton, QComboBox, QLineEdit, QProgressBar
from PyQt5.QtCore import Qt, QTimer, QRect, QSize
from AQ_ToolbarLayaout import AQ_ToolbarLayout


class AQ_ToolPanelFrame(QFrame):
    def __init__(self, shift_y, event_manager, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(0, shift_y + 2, parent.width(), 90))
        self.setStyleSheet("background-color: #2b2d30;\n"
                           "border-top-left-radius: 0px;\n"
                           "border-top-right-radius: 0px;\n"
                           "border-bottom-left-radius: 0px;\n"
                           "border-bottom-right-radius: 0px;")
        self.setObjectName("tool_panel_frame")
        self.tool_panel_layout = AQ_ToolbarLayout(self, event_manager)

    def resizeEvent(self, event):
        if hasattr(self, 'tool_panel_layout'):
            self.rotate_next_widget(self.tool_panel_layout)

    def rotate_next_widget(self, layout):
        recommended_width = layout.sizeHint().width()
        cur_width = self.width()
        if self.width() < (recommended_width - 5):
            for i in range(layout.count()):
                widest_widget = self.find_widest_Hwidget(layout)
                if widest_widget is not None:
                    widest_widget.change_oriental()
                    self.updateGeometry()
                    layout.invalidate()
                if self.width() > self.check_sum_widgets_hint(layout):
                    break
        elif self.width() >= (recommended_width + 50):
            for i in range(layout.count()):
                most_slim_widget = self.find_most_slim_Vwidget(layout)
                if most_slim_widget is not None:
                    most_slim_widget.change_oriental()
                    self.updateGeometry()
                    layout.invalidate()
                if self.check_sum_widgets_hint(layout) > self.width() - 50:
                    break

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

    def check_sum_widgets_hint(self, layout):
        sum_width = 0

        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if hasattr(widget, 'get_cur_oriental'): # Тут використовується як ознака що це віджет, а не сепаратор VLine
                sum_width += item.widget().sizeHint().width()

        return sum_width