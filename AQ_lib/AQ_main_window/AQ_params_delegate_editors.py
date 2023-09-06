from PyQt5.QtWidgets import QComboBox


class AQ_TreeViewComboBox(QComboBox):
    def __init__(self, param_attributes, parent=None):
        super().__init__()
        self.parent = parent
        self.view().setStyleSheet("color: #D0D0D0;")
        self.setStyleSheet("QComboBox { border: 0px solid #D0D0D0; color: #D0D0D0; }")
        enum_strings = param_attributes.get('enum_strings', '')
        for i in range(len(enum_strings)):
            enum_str = enum_strings[i]
            self.addItem(enum_str)
        self.currentIndexChanged.connect(self.parent.commit_editor_data)
