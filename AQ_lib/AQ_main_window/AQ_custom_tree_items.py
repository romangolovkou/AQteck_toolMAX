from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem

from AQ_params_delegate_editors import AQ_TreeViewComboBox


class AQ_param_item(QStandardItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        param_attibutes = self.data(Qt.UserRole)
        min_limit = param_attibutes.get('min_limit', None)
        if min_limit is not None:
            if new_value < min_limit:
                raise ValueError("value < min_limit, {} < {}".format(new_value, min_limit))

        max_limit = param_attibutes.get('max_limit', None)
        if max_limit is not None:
            if new_value > max_limit:
                raise ValueError("value > max_limit, {} > {}".format(new_value, max_limit))

        self._value = new_value

    def get_param_attributes(self):
        param_attributes = self.data(Qt.UserRole)
        return param_attributes


class AQ_enum_param_item(AQ_param_item):
    def __init__(self, name):
        super().__init__(name)
        self._value = None
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_TreeViewComboBox

    def get_editor(self):
        return self.editor


class AQ_catalog_item(QStandardItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if (new_value < 18):
            raise ValueError("Sorry you age is below eligibility criteria")
        print("setter method called")
        self._value = new_value

class AQ_param_manager_item(QStandardItem):
    def __init__(self, sourse_item, event_manager):
        param_attributes = sourse_item.data(Qt.UserRole)
        super().__init__(param_attributes.get('name', 'err_name'))
        self.event_manager = event_manager
        self.sourse_item = sourse_item

    def get_editor(self):
        return self.sourse_item.get_editor()

    def get_param_attributes(self):
        return self.sourse_item.get_param_attributes()

    def read_param(self):
        device = self.model().get_device()
        return
