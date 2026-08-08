from PySide6.QtCore import Signal

from AqParamsDelegateEditors import AqEnumTreeComboBox, AqEnumROnlyTreeLineEdit


class AqModbusGenericEnumTreeComboBox(AqEnumTreeComboBox):
    edit_done_signal = Signal(object)

    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)

    def updateIndex(self, index):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        index = index
        string = self.itemText(index)
        key = self.get_key_by_value(self.enum_str_dict, string)
        self.save_new_value(key)
        self.edit_done_signal.emit(self.manager_item_handler.get_sourse_item())

    def set_value(self, value):
        if not self.hasFocus():
            string = self.enum_str_dict.get(value, '')
            self.setCurrentText(string)


class AqModbusGenericEnumROnlyTreeLineEdit(AqEnumROnlyTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)

    def set_value(self, value):
        self.setText(self.enum_str_dict.get(value, ''))
