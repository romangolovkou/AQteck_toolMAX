from PySide2.QtWidgets import QHBoxLayout, QFrame
from AQ_ToolbarGroup import AQ_device_action_group, AQ_param_action_group, AQ_utils_group, AQ_archieve_group, \
                             AQ_firmware_group, AQ_other_group

class AQ_ToolbarLayout(QHBoxLayout):
    def __init__(self, parent, event_manager):
        super().__init__(parent)
        self.parent = parent
        self.setContentsMargins(4, 0, 0, 0)
        self.setSpacing(0)

        self.groups = []
        self.separators = []

    # Додаємо бажані группи кнопок за порядком розміщення
    # Группа 1
        self.device_action_group = AQ_device_action_group(event_manager, self.parent)
        self.groups.append(self.device_action_group)
    # Группа 2
        self.param_action_group = AQ_param_action_group(event_manager, self.parent)
        self.groups.append(self.param_action_group)
    # Группа 3
        self.utils_group = AQ_utils_group(event_manager, self.parent)
        self.groups.append(self.utils_group)
    # Группа 4
    #     self.archieve_group = AQ_archieve_group(event_manager, self.parent)
    #     self.groups.append(self.archieve_group)
    # Группа 4
    #     self.firmware_group = AQ_firmware_group(event_manager, self.parent)
    #     self.groups.append(self.firmware_group)
    # Группа 4
        self.other_group = AQ_other_group(event_manager, self.parent)
        self.groups.append(self.other_group)

    # Створюємо додані группи
        self.create_toolbar_groups()

    def create_toolbar_groups(self):
        for i in range(len(self.groups)):
            self.separators.append(VLine_separator(self.parent.height(), self.parent))
            self.addWidget(self.groups[i], 0)
            self.addWidget(self.separators[i], 0)

        self.addStretch(1)


class VLine_separator(QFrame):
    def __init__(self, height, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.VLine)
        self.setFixedSize(1, height - 10)
        self.setStyleSheet("background-color: #5caa62;\n")