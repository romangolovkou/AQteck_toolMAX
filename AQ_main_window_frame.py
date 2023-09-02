from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel

from AQ_left_widget_panel import AQ_left_widget_panel_frame
from AQ_main_field_frame import AQ_main_field_frame
from AQ_toolbar_frame import AQ_tool_panel_frame
from Resize_widgets import resizeWidthR_Qwidget, resizeWidthL_Qwidget, resizeHeigthLow_Qwidget, resizeHeigthTop_Qwidget, \
    resizeDiag_BotRigth_Qwidget, resizeDiag_BotLeft_Qwidget, resizeDiag_TopLeft_Qwidget, resizeDiag_TopRigth_Qwidget
from custom_window_templates import main_frame_AQFrame, title_bar_frame_AQFrame, main_field_frame_AQFrame


class AQ_main_window_frame(main_frame_AQFrame):
    def __init__(self, event_manager, main_name, icon, parent=None):
        super().__init__(parent)
        self.resizeLineWidth = 4
        self.event_manager = event_manager
        # TitleBarFrame
        self.title_bar_frame = title_bar_frame_AQFrame(self.event_manager, 60, main_name, icon, self)
        # ToolPanelFrame
        self.tool_panel_frame = AQ_tool_panel_frame(self.title_bar_frame.height(), self.event_manager, self)
        # MainFieldFrame
        self.main_field_frame = AQ_main_field_frame(self.event_manager, self.title_bar_frame.height() \
                                                    + self.tool_panel_frame.height(), self)

        # # Создаем заставочную картинку для главного поля
        # self.main_background_pic = QLabel(self.main_field_frame)
        # self.main_background_pic.setPixmap(self.background_pic)
        # self.main_background_pic.setScaledContents(True)
        # self.main_background_pic.setGeometry(0, 0, 450, 326)
        #
        # # Створюємо бокову панель зліва з віджетами доданих девайсів
        # self.left_panel = AQ_left_widget_panel_frame(self.event_manager, self.main_field_frame)
        # self.left_panel.setGeometry(0, 0, 248, self.main_field_frame.height())

        # # Создаем виджеты для изменения размеров окна
        self.resizeWidthR_widget = resizeWidthR_Qwidget(self)
        self.resizeWidthL_widget = resizeWidthL_Qwidget(self)
        self.resizeHeigthLow_widget = resizeHeigthLow_Qwidget(self)
        self.resizeHeigthTop_widget = resizeHeigthTop_Qwidget(self)
        self.resizeDiag_BotRigth_widget = resizeDiag_BotRigth_Qwidget(self)
        self.resizeDiag_BotLeft_widget = resizeDiag_BotLeft_Qwidget(self)
        self.resizeDiag_TopLeft_widget = resizeDiag_TopLeft_Qwidget(self)
        self.resizeDiag_TopRigth_widget = resizeDiag_TopRigth_Qwidget(self)

