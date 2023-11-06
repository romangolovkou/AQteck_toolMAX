from PySide6.QtCore import Qt, QModelIndex, QObject, Signal
from PySide6.QtGui import QStandardItem

from AQ_ParamsDelegateEditors import AQ_EnumTreeComboBox, AQ_UintTreeLineEdit, AQ_IntTreeLineEdit, \
    AQ_FloatTreeLineEdit, AQ_IpTreeLineEdit, AQ_StringTreeLineEdit, AQ_DateTimeLineEdit, AQ_EnumROnlyTreeLineEdit, \
    AQ_SignedToFloatTreeLineEdit, AQ_FloatEnumROnlyTreeLineEdit, AQ_FloatEnumTreeComboBox


class BaseItem:
    def __init__(self):
        super().__init__()
        self._value = None
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, data):
        print('I was setted with ', data)
        self._value = data


class ModbusItem(BaseItem):
    def __init__(self, packer=None):
        super().__init__()
        self.my_protocol = "Modbus"
        self._packer = packer

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, data):
        if self._packer:
            _value = self._packer.unpack()
        else:
            _value = data

        print('I was setted with ', data,)


class AQ_ParamItem(QStandardItem):
    def __init__(self, name, packer=None):
        super().__init__(name)
        self.packer = packer
        self._value = None
        self.value_in_device = None
        self.editor = None
        self.synchro_flag = False
        self.param_status = None
        self.local_event_manager = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value is not None:
            if self.validate(new_value) is True:
                if self.value_in_device is None:
                    self.value_in_device = new_value
                else:
                    if self.value_in_device == new_value:
                        self.param_status = 'ok'
                    else:
                        self.param_status = 'changed'
                        self.synchronized = False
                        # self.local_event_manager.emit_event('add_param_to_changed_stack', self)
                self._value = new_value
        else:
            self.param_status = 'error'

    @property
    def synchronized(self):
        return self.synchro_flag

    @synchronized.setter
    def synchronized(self, flag):
        if flag is True:
            # if self.value_in_device != self.value:
            self.value_in_device = self.value
            if self.param_status == 'changed':
                self.param_status = 'ok'
            if self.local_event_manager is not None:
                self.local_event_manager.emit_event('add_param_to_update_stack', self)

        self.synchro_flag = flag

    def confirm_writing(self, result: bool, message=None):
        """
        The function must be called for each writing operation.
        :param result: True - success writing, False - writing fail.
        :param message: If need - error message.
        :return:
        """
        self.synchronized = result
        if not result:
            self.set_error_flag(message)

    def set_error_flag(self, message=None):
        self.param_status = 'error'
        self.error_message = message
        if self.local_event_manager is not None:
            self.local_event_manager.emit_event('add_param_to_update_stack', self)

    def data_from_network(self, new_value, is_error=False, message=None):
        if is_error:
            self.set_error_flag(message)
        else:
            if self.packer:
                new_value = self.packer.unpack(self, new_value)
            self.validate(new_value)
            self._value = new_value
            self.synchronized = True

    def data_for_network(self):
        if self.packer:
            value = self.packer.pack(self, self._value)
        else:
            value = self._value

        return value

    def validate(self, new_value):
        param_attributes = self.data(Qt.UserRole)
        min_limit = param_attributes.get('min_limit', None)
        if min_limit is not None:
            if new_value < min_limit:
                self.param_status = 'error'
                print("value < min_limit, {} < {}".format(new_value, min_limit))
                return False

        max_limit = param_attributes.get('max_limit', None)
        if max_limit is not None:
            if new_value > max_limit:
                self.param_status = 'error'
                print("value > max_limit, {} > {}".format(new_value, max_limit))
                return False

        self.param_status = 'ok'
        return True

    # def synchro_last_value_and_value(self):
    #     self.value_in_device = self._value
    #     self.param_status = 'ok'

    def get_param_attributes(self):
        param_attributes = self.data(Qt.UserRole)
        return param_attributes

    def get_editor(self):
        return self.editor

    def get_status(self):
        return self.param_status

    def set_local_event_manager(self, local_event_manager):
        self.local_event_manager = local_event_manager


class AQ_CatalogItem(AQ_ParamItem):
    def __init__(self, name):
        super().__init__(name)


class AQ_EnumParamItem(AQ_ParamItem):
    def __init__(self, name, packer):
        super().__init__(name, packer)
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
    def __init__(self, name, packer):
        super().__init__(name, packer)
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
    def __init__(self, name, packer):
        super().__init__(name, packer)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_IntTreeLineEdit


class AQ_FloatParamItem(AQ_ParamItem):
    def __init__(self, name, packer):
        super().__init__(name, packer)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_FloatTreeLineEdit


class AQ_StringParamItem(AQ_ParamItem):
    def __init__(self, name, packer):
        super().__init__(name, packer)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_StringTreeLineEdit


class AQ_DateTimeParamItem(AQ_ParamItem):
    def __init__(self, name, packer):
        super().__init__(name, packer)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_DateTimeLineEdit


class AQ_SignedToFloatParamItem(AQ_ParamItem):
    def __init__(self, name, packer):
        super().__init__(name, packer)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_SignedToFloatTreeLineEdit


class AQ_UnsignedToFloatParamItem(AQ_ParamItem):
    def __init__(self, name, packer):
        super().__init__(name, packer)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AQ_SignedToFloatTreeLineEdit


class AQ_FloatEnumParamItem(AQ_EnumParamItem):
    def __init__(self, name, packer):
        super().__init__(name, packer)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor_RW = AQ_FloatEnumTreeComboBox
        self.editor_R_Only = AQ_FloatEnumROnlyTreeLineEdit


class AQ_ParamManagerItem(QStandardItem):
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
