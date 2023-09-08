from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem

from AQ_params_delegate_editors import AQ_TreeViewComboBox, AQ_UintTreeLineEdit, AQ_IntTreeLineEdit, \
    AQ_FloatTreeLineEdit, AQ_IpTreeLineEdit


class AQ_ParamItem(QStandardItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None
        self.editor = None

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

    def get_editor(self):
        return self.editor


class AQ_CatalogItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None


class AQ_EnumParamItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_TreeViewComboBox


class AQ_UnsignedParamItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor_uint = AQ_UintTreeLineEdit
        self.editor_ip = AQ_IpTreeLineEdit

    def get_editor(self):
        param_attributes = self.data(Qt.UserRole)
        if param_attributes is not None:
            if param_attributes.get('visual_type', '') == 'ip_format':
                return self.editor_ip

        return self.editor_uint


class AQ_SignedParamItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_IntTreeLineEdit


class AQ_FloatParamItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_FloatTreeLineEdit


class AQ_DateTimeParamItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_UintTreeLineEdit


class AQ_param_manager_item(QStandardItem):
    def __init__(self, sourse_item):
        param_attributes = sourse_item.data(Qt.UserRole)
        super().__init__(param_attributes.get('name', 'err_name'))
        self.sourse_item = sourse_item
        self.editor_object = None

    def get_editor(self):
        return self.sourse_item.get_editor()

    def get_param_attributes(self):
        return self.sourse_item.get_param_attributes()

    def get_sourse_item(self):
        return self.sourse_item

    def get_value(self):
        return self.sourse_item.value

    def save_editor_object(self, editor):
        self.editor_object = editor

    def show_new_value(self, value):
        if self.editor_object is not None:
            self.editor_object.set_value(value)
