from PyQt5.QtCore import Qt, QModelIndex, QObject, pyqtSignal
from PyQt5.QtGui import QStandardItem

from AQ_ParamsDelegateEditors import AQ_EnumTreeComboBox, AQ_UintTreeLineEdit, AQ_IntTreeLineEdit, \
    AQ_FloatTreeLineEdit, AQ_IpTreeLineEdit, AQ_StringTreeLineEdit, AQ_DateTimeLineEdit, AQ_EnumROnlyTreeLineEdit


class AQ_ParamItem(QStandardItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None
        self.last_value_from_device = None
        self.editor = None
        self.param_status = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value is not None:
            param_attibutes = self.data(Qt.UserRole)
            min_limit = param_attibutes.get('min_limit', None)
            if min_limit is not None:
                if new_value < min_limit:
                    self.param_status = 'error'
                    raise ValueError("value < min_limit, {} < {}".format(new_value, min_limit))

            max_limit = param_attibutes.get('max_limit', None)
            if max_limit is not None:
                if new_value > max_limit:
                    self.param_status = 'error'
                    raise ValueError("value > max_limit, {} > {}".format(new_value, max_limit))

            if self.last_value_from_device is None:
                self.last_value_from_device = new_value
            else:
                if self.last_value_from_device == new_value:
                    self.param_status = 'ok'
                else:
                    self.param_status = 'changed'
            self._value = new_value
        else:
            self.param_status = 'error'

    def set_last_value_from_device(self, new_value):
        self.last_value_from_device = new_value
        try:
            self.value = new_value
            # self.param_status = 'ok'
        except:
            self._value = new_value
            self.param_status = 'error'

    def synchro_last_value_and_value(self):
        self.last_value_from_device = self._value
        self.param_status = 'ok'

    def get_param_attributes(self):
        param_attributes = self.data(Qt.UserRole)
        return param_attributes

    def get_editor(self):
        return self.editor

    def get_status(self):
        return self.param_status


class AQ_CatalogItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)


class AQ_EnumParamItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor_RW = AQ_EnumTreeComboBox
        self.editor_R_Only = AQ_EnumROnlyTreeLineEdit

    def get_editor(self):
        param_attributes = self.data(Qt.UserRole)
        if param_attributes is not None:
            if (param_attributes.get('R_Only', 0) == 1 and param_attributes.get('W_Only', 0) == 0):
                return self.editor_R_Only

        return self.editor_RW


class AQ_UnsignedParamItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)
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
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_IntTreeLineEdit


class AQ_FloatParamItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_FloatTreeLineEdit


class AQ_StringParamItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_StringTreeLineEdit


class AQ_DateTimeParamItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_DateTimeLineEdit


class AQ_param_manager_item(QStandardItem):
    def __init__(self, sourse_item):
        param_attributes = sourse_item.data(Qt.UserRole)
        super().__init__(param_attributes.get('name', 'err_name'))
        self.sourse_item = sourse_item
        self.editor_object = None
        self.param_status = 'ok'
        self.setData(self.param_status, Qt.UserRole + 1)

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

    def show_new_value(self):
        if self.editor_object is not None:
            value = self.get_value()
            self.editor_object.set_value(value)

    def save_new_value(self, value):
        try:
            self.sourse_item.value = value
        except:
            self.param_status = 'error'

        self.update_status()

    def update_status(self):
        self.setData(self.sourse_item.get_status(), Qt.UserRole + 1)
