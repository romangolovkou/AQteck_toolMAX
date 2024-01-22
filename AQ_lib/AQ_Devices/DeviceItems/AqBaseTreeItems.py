from datetime import datetime
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem

from AqParamsDelegateEditors import AqEnumTreeComboBox, AqUintTreeLineEdit, AqIntTreeLineEdit, \
    AqFloatTreeLineEdit, AqStringTreeLineEdit, AqDateTimeLineEdit, AqEnumROnlyTreeLineEdit, \
    AqSignedToFloatTreeLineEdit, AqFloatEnumROnlyTreeLineEdit, AqFloatEnumTreeComboBox, AqBitLineEdit, AqIpTreeLineEdit


class AqParamItem(QStandardItem):
    def __init__(self, param_attributes):
        name = param_attributes.get('name', None)
        R_Only = param_attributes.get('R_Only', None)
        W_Only = param_attributes.get('W_Only', None)
        if name is None or R_Only is None or W_Only is None:
            raise Exception('AqParamItemError: "name" is not exist')
        super().__init__(name)
        self._value = None
        self.value_in_device = None
        self.editor = None
        self.synchro_flag = False
        self.param_status = None
        self.local_event_manager = None
        self.setData(param_attributes, Qt.UserRole)

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
            new_value = self.unpack(new_value)
            self.validate(new_value)
            self._value = new_value
            self.synchronized = True

    def data_for_network(self):
        return self.pack()

    def pack(self):
        return self._value

    def unpack(self, data):
        return data

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

    def set_default_value(self):
        param_attributes = self.data(Qt.UserRole)
        default_value = param_attributes.get('def_value', None)
        if default_value is None:
            default_value = self._get_standart_def_value()

        min_limit = param_attributes.get('min_limit', None)
        if min_limit is not None:
            if default_value < min_limit:
                default_value = min_limit
        max_limit = param_attributes.get('max_limit', None)
        if max_limit is not None:
            if default_value > max_limit:
                default_value = max_limit

        self.value = default_value

    def _get_standart_def_value(self) -> Any:
        return 0

    def get_param_attributes(self):
        param_attributes = self.data(Qt.UserRole)
        return param_attributes

    def get_editor(self):
        return self.editor

    def get_status(self):
        return self.param_status

    def set_local_event_manager(self, local_event_manager):
        self.local_event_manager = local_event_manager


class AqModbusItem(AqParamItem):
    def __init__(self, param_attributes):

        modbus_reg = param_attributes.get('modbus_reg', None)
        param_size = param_attributes.get('param_size', None)
        if param_size is None or modbus_reg is None:
            raise Exception('ModbusItemError: "modbus_reg" or "param_size" not exist')
        # TODO: Переделать c размера в байхтах на колличество регистров
        read_func = param_attributes.get('read_func', None)
        if read_func is None:
            raise Exception('ModbusItemError: "read_func" is not exist')

        if not (param_attributes.get('R_Only', None) == 1 and
                param_attributes.get('W_Only', None) == 0):
            write_func = param_attributes.get('write_func', None)
            if write_func is None:
                raise Exception('"write_func" is not exist')

        param_attributes['protocol'] = 'modbus'

        super().__init__(param_attributes)

        self.setData(param_attributes, Qt.UserRole)


class AqModbusFileItem(AqParamItem):
    def __init__(self, param_attributes):

        file_num = param_attributes.get('file_num', None)
        start_record_num = param_attributes.get('start_record_num', None)
        file_size = param_attributes.get('file_size', None)
        if file_num is None or start_record_num is None or file_size is None:
            raise Exception('ModbusItemError: "file_num", "start_record_num" or "file_size" not exist')

        param_attributes['protocol'] = 'modbus'

        super().__init__(param_attributes)

        self.setData(param_attributes, Qt.UserRole)


class AqCatalogItem(AqParamItem):
    def __init__(self, param_attributes):
        is_catalog = param_attributes.get('is_catalog', None)
        if is_catalog is None:
            raise Exception('AQ_CatalogItemError: "is_catalog" is not exist')
        param_attributes['R_Only'] = 0
        param_attributes['W_Only'] = 0
        super().__init__(param_attributes)


class AqEnumParamItem(AqParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None or param_attributes.get('enum_strings', None) is None:
            raise Exception('AQ_EnumParamItemError: "param_size" or "enum_strings" is not exist')

        # Перетворюємо розмір з бітів на байти
        byte_count = self.param_size // 8
        if self.param_size % 8 != 0:
            byte_count += 1
        self.param_size = 2 if byte_count < 3 else 4
        param_attributes['param_size'] = self.param_size

        if param_attributes.get('min_limit', None) is None:
            param_attributes['min_limit'] = None
        if param_attributes.get('max_limit', None) is None:
            param_attributes['max_limit'] = None
        if param_attributes.get('def_value', None) is None:
            param_attributes['def_value'] = ''
        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor_RW = AqEnumTreeComboBox
        self.editor_R_Only = AqEnumROnlyTreeLineEdit

    def get_editor(self):
        param_attributes = self.data(Qt.UserRole)
        if param_attributes is not None:
            if (param_attributes.get('R_Only', 0) == 1 and param_attributes.get('W_Only', 0) == 0):
                return self.editor_R_Only

        return self.editor_RW


class AqUnsignedParamItem(AqParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None:
            raise Exception('AQ_UnsignedParamItemError: "param_size" is not exist')

        if param_attributes.get('min_limit', None) is None:
            param_attributes['min_limit'] = 0
        if param_attributes.get('max_limit', None) is None:
            param_attributes['max_limit'] = self.get_standart_max_limit(self.param_size)
        if param_attributes.get('def_value', None) is None:
            param_attributes['def_value'] = param_attributes.get('min_limit', 0)
        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AqUintTreeLineEdit


    def get_standart_max_limit(self, param_size):
        if param_size == 1:
            return int('255')
        elif param_size == 2:
            return int('65535')
        elif param_size == 4:
            return int('4294967295')
        elif param_size == 8:
            return int('18446744073709551615')


class AqSignedParamItem(AqParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None:
            raise Exception('AQ_SignedParamItemError: "param_size" is not exist')

        if param_attributes.get('min_limit', None) is None:
            param_attributes['min_limit'] = self.get_standart_min_limit(self.param_size)
        if param_attributes.get('max_limit', None) is None:
            param_attributes['max_limit'] = self.get_standart_max_limit(self.param_size)
        if param_attributes.get('def_value', None) is None:
            param_attributes['def_value'] = 0
        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AqIntTreeLineEdit

    def get_standart_min_limit(self, param_size):
        if param_size == 1:
            return int('-127')
        elif param_size == 2:
            return int('-32768')
        elif param_size == 4:
            return int('-2147483648')
        elif param_size == 8:
            return int('-9223372036854775808')

    def get_standart_max_limit(self, param_size):
        if param_size == 1:
            return int('128')
        elif param_size == 2:
            return int('32767')
        elif param_size == 4:
            return int('2147483647')
        elif param_size == 8:
            return int('9223372036854775807')


class AqFloatParamItem(AqParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None:
            raise Exception('AQ_FloatParamItemError: "param_size" is not exist')

        if param_attributes.get('min_limit', None) is None:
            param_attributes['min_limit'] = self.get_standart_min_limit(self.param_size)
        if param_attributes.get('max_limit', None) is None:
            param_attributes['max_limit'] = self.get_standart_max_limit(self.param_size)
        if param_attributes.get('def_value', None) is None:
            param_attributes['def_value'] = 0.0
        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AqFloatTreeLineEdit

    def get_standart_min_limit(self, param_size):
        if param_size == 4:
            return float('-3.402283E+38')
        elif param_size == 8:
            return float('-1.7976931348623E+308')

    def get_standart_max_limit(self, param_size):
        if param_size == 4:
            return float('3.402283E+38')
        elif param_size == 8:
            return float('1.7976931348623E+308')


class AqStringParamItem(AqParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None:
            raise Exception('AQ_StringParamItemError: "param_size" is not exist')

        if param_attributes.get('min_limit', None) is None:
            param_attributes['min_limit'] = None
        if param_attributes.get('max_limit', None) is None:
            param_attributes['max_limit'] = None
        if param_attributes.get('def_value', None) is None:
            param_attributes['def_value'] = ''
        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AqStringTreeLineEdit


class AqDateTimeParamItem(AqParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None:
            raise Exception('AQ_DateTimeParamItemError: "param_size" is not exist')

        if param_attributes.get('min_limit', None) is None:
            param_attributes['min_limit'] = self.get_standart_min_limit()
        if param_attributes.get('max_limit', None) is None:
            param_attributes['max_limit'] = self.get_standart_max_limit()
        if param_attributes.get('def_value', None) is None:
            param_attributes['def_value'] = 0
        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AqDateTimeLineEdit

    def get_standart_min_limit(self):
        return 0  #'01.01.2000 0:00:00' дата від якої у нас йде відлік часу у секундах


    def get_standart_max_limit(self):
        max_limit_date = datetime.strptime('07.02.2136 6:28:15', '%d.%m.%Y %H:%M:%S')
        # Начальный момент времени (2000-01-01 00:00:00)
        min_limit_date = datetime(2000, 1, 1)
        max_limit_seconds = (max_limit_date - min_limit_date).total_seconds()
        return max_limit_seconds


class AqIpParamItem(AqParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None:
            raise Exception('AqIpParamItemError: "param_size" is not exist')

        if param_attributes.get('min_limit', None) is None:
            param_attributes['min_limit'] = None
        if param_attributes.get('max_limit', None) is None:
            param_attributes['max_limit'] = None
        if param_attributes.get('def_value', None) is None:
            param_attributes['def_value'] = ''
        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AqIpTreeLineEdit


class AqMACParamItem(AqParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None:
            raise Exception('AqMACParamItemError: "param_size" is not exist')

        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AqUintTreeLineEdit


class AqBitParamItem(AqParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None:
            raise Exception('AQ_BitParamItemError: "param_size" is not exist')

        param_attributes['min_limit'] = 0
        param_attributes['max_limit'] = 1
        if param_attributes.get('def_value', None) is None:
            param_attributes['def_value'] = 0
        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor_RW = AqBitLineEdit
        self.editor_R_Only = AqUintTreeLineEdit

    def get_editor(self):
        param_attributes = self.data(Qt.UserRole)
        if param_attributes is not None:
            if (param_attributes.get('R_Only', 0) == 1 and param_attributes.get('W_Only', 0) == 0):
                return self.editor_R_Only

        return self.editor_RW


class AqSignedToFloatParamItem(AqParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None or param_attributes.get('multiply', None) is None:
            raise Exception('AQ_SignedToFloatParamItemError: "param_size" or "multiply" is not exist')

        if param_attributes.get('min_limit', None) is None:
            param_attributes['min_limit'] = None
        if param_attributes.get('max_limit', None) is None:
            param_attributes['max_limit'] = None
        if param_attributes.get('def_value', None) is None:
            param_attributes['def_value'] = 0
        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AqSignedToFloatTreeLineEdit


class AqUnsignedToFloatParamItem(AqParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None or param_attributes.get('multiply', None) is None:
            raise Exception('AQ_UnsignedToFloatParamItemError: "param_size" or "multiply" is not exist')

        if param_attributes.get('min_limit', None) is None:
            param_attributes['min_limit'] = None
        if param_attributes.get('max_limit', None) is None:
            param_attributes['max_limit'] = None
        if param_attributes.get('def_value', None) is None:
            param_attributes['def_value'] = 0
        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor = AqSignedToFloatTreeLineEdit


class AqFloatEnumParamItem(AqEnumParamItem):
    def __init__(self, param_attributes):
        self.param_size = param_attributes.get('param_size', None)
        if self.param_size is None or param_attributes.get('enum_strings', None) is None:
            raise Exception('AQ_FloatEnumParamItemError: "param_size" or "enum_strings" is not exist')

        if param_attributes.get('min_limit', None) is None:
            param_attributes['min_limit'] = None
        if param_attributes.get('max_limit', None) is None:
            param_attributes['max_limit'] = None
        if param_attributes.get('def_value', None) is None:
            param_attributes['def_value'] = 0
        super().__init__(param_attributes)
        # editor це не об'єкт, а посилання на класс, сам об'єкт повинен бути створений у делегаті
        self.editor_RW = AqFloatEnumTreeComboBox
        self.editor_R_Only = AqFloatEnumROnlyTreeLineEdit


class AqParamManagerItem(QStandardItem):
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
