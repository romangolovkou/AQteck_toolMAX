from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel

from AQ_left_widget_panel import AQ_left_widget_panel_frame
from AQ_main_field_frame import AQ_main_field_frame
from AQ_titlebar_frame import AQ_title_bar_frame
from AQ_toolbar_frame import AQ_tool_panel_frame
from Resize_widgets import resizeWidthR_Qwidget, resizeWidthL_Qwidget, resizeHeigthLow_Qwidget, resizeHeigthTop_Qwidget, \
    resizeDiag_BotRigth_Qwidget, resizeDiag_BotLeft_Qwidget, resizeDiag_TopLeft_Qwidget, resizeDiag_TopRigth_Qwidget
from custom_window_templates import AQ_simplified_main_frame


class AQ_main_window_frame(AQ_simplified_main_frame):
    def __init__(self, event_manager, main_name, icon, parent=None):
        super().__init__(parent)

        self.event_manager = event_manager
        # TitleBarFrame
        self.title_bar_frame = AQ_title_bar_frame(self.event_manager, 60, main_name, icon, self)
        # ToolPanelFrame
        self.tool_panel_frame = AQ_tool_panel_frame(self.title_bar_frame.height(), self.event_manager, self)
        # MainFieldFrame
        self.main_field_frame = AQ_main_field_frame(self.event_manager, self.title_bar_frame.height() \
                                                    + self.tool_panel_frame.height(), self)

        # # Создаем виджеты для изменения размеров окна
        self.resizeLineWidth = 4
        self.resizeWidthR_widget = resizeWidthR_Qwidget(self.event_manager, self)
        self.resizeWidthL_widget = resizeWidthL_Qwidget(self.event_manager, self)
        self.resizeHeigthLow_widget = resizeHeigthLow_Qwidget(self.event_manager, self)
        self.resizeHeigthTop_widget = resizeHeigthTop_Qwidget(self.event_manager, self)
        self.resizeDiag_BotRigth_widget = resizeDiag_BotRigth_Qwidget(self.event_manager, self)
        self.resizeDiag_BotLeft_widget = resizeDiag_BotLeft_Qwidget(self.event_manager, self)
        self.resizeDiag_TopLeft_widget = resizeDiag_TopLeft_Qwidget(self.event_manager, self)
        self.resizeDiag_TopRigth_widget = resizeDiag_TopRigth_Qwidget(self.event_manager, self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.title_bar_frame.resize(self.width(), self.title_bar_frame.height())
        self.tool_panel_frame.resize(self.width(), self.tool_panel_frame.height())
        self.main_field_frame.resize(self.width(), self.height() -
                                     (self.title_bar_frame.height() + self.tool_panel_frame.height() + 2))

        self.resizeWidthR_widget.setGeometry(self.width() - self.resizeLineWidth,
                                             self.resizeLineWidth, self.resizeLineWidth,
                                             self.height() - (self.resizeLineWidth * 2))
        self.resizeWidthL_widget.setGeometry(0, self.resizeLineWidth, self.resizeLineWidth,
                                             self.height() - (self.resizeLineWidth * 2))
        self.resizeHeigthLow_widget.setGeometry(self.resizeLineWidth, self.height() - self.resizeLineWidth,
                                                self.width() - (self.resizeLineWidth * 2),
                                                self.resizeLineWidth)
        self.resizeHeigthTop_widget.setGeometry(self.resizeLineWidth, 0,
                                                self.width() - (self.resizeLineWidth * 2),
                                                self.resizeLineWidth)
        self.resizeDiag_BotRigth_widget.move(self.width() - self.resizeLineWidth,
                                             self.height() - self.resizeLineWidth)
        self.resizeDiag_TopLeft_widget.move(0, 0)
        self.resizeDiag_TopRigth_widget.move(self.width() - self.resizeLineWidth, 0)
        self.resizeDiag_BotLeft_widget.move(0, self.height() - self.resizeLineWidth)

        event.accept()

