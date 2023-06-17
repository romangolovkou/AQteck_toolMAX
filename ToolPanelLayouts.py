from ToolPanelButtons import AddDeviceButton, VLine_separator
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QRect, QSize

class SetGroup_LayH(QHBoxLayout):
    def __init__(self, parent=None, *buttons):
        super().__init__(parent)
        self.setContentsMargins(2, 0, 2, 0)
        self.setSpacing(0)
        for button in buttons:
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            self.addWidget(button)

class SetGroup_LayV(QVBoxLayout):
    def __init__(self, parent=None, *buttons):
        super().__init__(parent)
        self.setContentsMargins(2, 0, 2, 0)
        self.setSpacing(0)
        count = len(buttons)
        for button in buttons:
            if count > 2:
                button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            else:
                button.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.addWidget(button)


def replaceToolPanelWidget(self, layout):
    recommended_width = self.tool_panel_frame.minimumSizeHint().width()
    #порядок перчисления элементов в макете по индексу
    order = [4, 10, 2, 0, 6, 8, 12]

    if self.width() < (recommended_width - 50):
        # Перебор всех добавленных в макет других макетов
        mask_shift = 0
        for i in order:
            cur_group_layout = layout.itemAt(i)
            if isinstance(cur_group_layout, QHBoxLayout):
                index = layout.indexOf(cur_group_layout)
                layout.removeItem(cur_group_layout)
                widgets = []
                for i in range(cur_group_layout.count()):
                    item = cur_group_layout.itemAt(i)
                    widget = item.widget()
                    if widget is not None:
                        widgets.append(widget)

                cur_group_layout = SetGroup_LayV(self.tool_panel_frame, *widgets)
                self.tool_panel_layout_mask |= 1 << mask_shift
                mask_shift = mask_shift + 1
                layout.insertLayout(index, cur_group_layout, 0)
            if (self.tool_panel_frame.minimumSizeHint().width() < self.width()):
                break
    elif self.width() >= (recommended_width + 50):
        # Перебор всех добавленных в макет других макетов
        mask_shift = 0
        for i in reversed(order):
            cur_group_layout = self.tool_panel_layout.itemAt(i)
            if isinstance(cur_group_layout, QVBoxLayout):
                index = layout.indexOf(cur_group_layout)
                layout.removeItem(cur_group_layout)
                widgets = []
                for i in range(cur_group_layout.count()):
                    item = cur_group_layout.itemAt(i)
                    widget = item.widget()
                    if widget is not None:
                        widgets.append(widget)

                cur_group_layout = SetGroup_LayH(self.tool_panel_frame, *widgets)
                self.tool_panel_layout_mask &= ~(1 << mask_shift)
                mask_shift = mask_shift + 1
                layout.insertLayout(index, cur_group_layout, 0)
            if (self.tool_panel_frame.minimumSizeHint().width() > (self.width() -75)):
                break