import threading
from abc import ABC, abstractmethod

from PySide6.QtCore import Qt, QModelIndex

from AqConnect import AqConnect
from AqBaseTreeItems import AqParamItem
from AQ_EventManager import AQ_EventManager
from AqTreeViewItemModel import AqTreeItemModel
from AqDeviceConfig import AqDeviceConfig
from AqDeviceInfoModel import AqDeviceInfoModel
from AqDeviceParamListModel import AqDeviceParamListModel


class AqBaseDevice(ABC):
    def __init__(self, event_manager, connect: AqConnect):
        self._event_manager = event_manager
        self._local_event_manager = None
        self._device_tree = None
        self._connect = connect
        self._params_list = list()
        self._update_param_stack = list()
        self._stack_to_read = list()
        self._stack_to_write = list()
        self._message_require_stack = list()
        self._core_cv = threading.Condition()
        self.__create_local_event_manager()
        self._connect.setRequestGroupProceedDoneCallback(self.update_param_callback)

        self._info = {
            'name':             '',
            'version':          '',
            'serial_num':       None,
            'address':          ''
        }

        self._functions = {
            'read_write': None,
            'rtc': None,
            'password': True,
            'calibration': None,
            'log': None,
            'fw_update': None,
            'restart': None
        }

        self._status = None
        self._is_inited = False

        if self._connect is not None:
            self._info['address'] = self._connect.address_string()
        else:
            raise Exception('AqBaseDeviceError: can`t open connect')

        if not self.init_device():
            raise Exception('AqBaseDeviceError: can`t initialize device')

        if self._device_tree is not None and isinstance(self._device_tree, AqTreeItemModel):
            self._device_tree.set_device(self)
        else:
            if self._status != 'need_pass' and self._status != 'decrypt_err'\
                    and self._status != 'parsing_err':
                raise Exception('AqBaseDeviceError: device_tree isn`t exists')

        if self._status != 'need_pass' and self._status != 'decrypt_err'\
                and self._status != 'parsing_err':
            self._param_convert_tree_to_list()

        # self.__verify()

    @property
    def status(self):
        return self._status

    @property
    def device_tree(self):
        return self._device_tree

    @property
    def device_info_model(self):
        return self.get_device_info_model()

    @property
    def is_inited(self):
        return self._is_inited

    @property
    def name(self):
        return self._info['name']

    def func(self, name: str):
        return self._functions[name]

    def info(self, param):
        return self._info[param]

    # def init_parameters(self):
    #     self._event_manager.register_event_handler('current_device_data_updated', self.read_complete)
    #     # TODO: check for offline connectivity
    #     for i in self._params_list:
    #         self.read_parameters(i)
    #         with self._core_cv:
    #             self._core_cv.wait()
    #             # TODO: Установить значение по умолчанию или 0
    #
    #     self._event_manager.unregister_event_handler('current_device_data_updated', self.read_complete)
    #     return True
    #
    # def read_complete(self, device, item):
    #     if device == self:
    #         with self._core_cv:
    #             self._core_cv.notify()

    def de_init(self):
        self._connect.close()
        self._clear_existing_requests()
        self._event_manager.unregister_event_handler('current_device_data_updated', self.init_complete)

    def _clear_existing_requests(self):
        self._connect.clear_existing_requests()

    def init_parameters(self):
        self._event_manager.register_event_handler('current_device_data_updated', self.init_complete, True)
        self.read_parameters(self._params_list)

    def init_complete(self, *args):
        if args[0] == self:
            self._is_inited = True

    def read_parameters(self, items=None, message_feedback_flag=False):
        if items is None:
            root = self._device_tree.invisibleRootItem()
            for row in range(root.rowCount()):
                child_item = root.child(row)
                self.__read_item(child_item)
        else:
            if isinstance(items, AqParamItem):
                items = [items]
            for i in range(len(items)):
                self.__read_item(items[i])

        if len(self._stack_to_read) > 0:
            print('AqBaseDevice: Device: '
                  + self.info('name') + ' addr: '
                  + self.info('address')
                  + ' maked request. Request size = '
                  + str(len(self._stack_to_read)))
            self._connect.create_param_request('read', self._stack_to_read)
            if message_feedback_flag:
                self._message_require_stack.append({'method': 'read', 'stack': self._stack_to_read.copy()})
            self._stack_to_read.clear()

    def write_parameters(self, items=None):
        if items is None:
            root = self.device_tree.invisibleRootItem()
            for row in range(root.rowCount()):
                child_item = root.child(row)
                self.__write_item(child_item)
        else:
            if isinstance(items, AqParamItem):
                items = [items]
            for i in range(len(items)):
                self.__write_item(items[i])

        if len(self._stack_to_write) > 0:
            self._connect.create_param_request('write', self._stack_to_write)
            self._stack_to_write.clear()

    def read_parameter(self, item):
        """Read parameter from device"""
        self._stack_to_read.append(item)

    def write_parameter(self, item):
        if item.get_status() == 'changed':
            self._stack_to_write.append(item)

    def set_default_values(self):
        for item in self._params_list:
            param_attributes = item.data(Qt.UserRole)
            if param_attributes is not None:
                if not (param_attributes.get('R_Only', 0) == 1 and param_attributes.get('W_Only', 0) == 0):
                    item.set_default_value(False)
                    self.__add_param_to_update_stack(item)

        self.update_param_callback()


    def reboot(self):
        """
            Return NotImplemented by default.
            Redefine function at child class if it needed
        """
        return NotImplemented

    def fw_update(self, fwdata):
        """
            Return NotImplemented by default.
            Redefine function at child class if it needed
        """
        return NotImplemented

    def set_rtc(self, rtc_data):
        """
            Return NotImplemented by default.
            Redefine function at child class if it needed
        """
        return NotImplemented

    def set_password(self, password):
        """
            Return NotImplemented by default.
            Redefine function at child class if it needed
        """
        return NotImplemented

    def get_device_info_model(self):
        dev_model = AqDeviceInfoModel()
        dev_model.add_general_info("Device name", self._info['name'])
        dev_model.add_general_info("Version", self._info['version'])
        return dev_model

    def get_device_param_list_model(self):
        dev_model = AqDeviceParamListModel()
        dev_model.name = self.info('name')
        dev_model.serial = self.info('serial_num') if self.info('serial_num') is not None else "no serial number"
        dev_model.param_list = self._params_list
        return dev_model

    @abstractmethod
    def get_configuration(self) -> AqDeviceConfig:
        """
        Save your parameters into AqDeviceConfig structure with
        rules for your device
        Example:   config.saved_param_list.append(
                {'UID': param_attributes.get('UID', 0),
                 'modbus_reg': param_attributes.get('modbus_reg', 0),
                 'value': devParam.value})
        :return: data to save into file
        """
        return NotImplementedError

    @abstractmethod
    def set_configuration(self, config: AqDeviceConfig):
        """
        Apply configuration data with rules for your device
        This function is revert to get_configuration
        :param config: - config data created by get_configuration func
        :return: True/False
        """
        return NotImplementedError

    # Private function
    def __add_param_to_update_stack(self, item):
        if item not in self._update_param_stack:
            self._update_param_stack.append(item)

    def update_param_callback(self):
        from AppCore import Core
        self._event_manager.emit_event('current_device_data_updated', self, self._update_param_stack)
        if len(self._message_require_stack) > 0:
            for msg_require in self._message_require_stack:
                if self._update_param_stack[::-1] == msg_require['stack']:
                    msg_status = 'ok'
                    for param in self._update_param_stack:
                        if param.get_status() != 'ok':
                            msg_status = 'error'
                            break

                    if msg_status == 'ok':
                        Core.message_manager.send_main_message("Success", f'{self.name}  Read successful')
                    else:
                        Core.message_manager.send_main_message("Error", f'{self.name}  Read failed. One or more params can`t read')

                    self._message_require_stack.remove(msg_require)
        with self._core_cv:
            self._core_cv.notify()
        self._update_param_stack.clear()

    def __convert_tree_branch_to_list(self, item):
        param_attributes = item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                self.__convert_tree_branch_to_list(child_item)
        else:
            self._params_list.append(item)
            item.set_local_event_manager(self._local_event_manager)

    @abstractmethod
    def init_device(self) -> bool:
        """
            Init your device
            Fill self.info dict
            Example:
                self.info['name'] = 'MV210-101'
                self.info['version'] = '1.1.3'
                self.info['serial_num'] = '1333....'

            Fill self._functions dictionary for supported function in child class
            Example:
            self._functions = {
                'read_write': True,
                'password' = True,
                'restart' = True
            }
            :return: True - init ok, False - init error
        """
        pass

    def __verify(self) -> bool:
        if all(hasattr(self._info, attr) for attr in ["name", "version", "serial"]):
            print('Failed to create ', self.__name__, 'object.')
            print('No required attributes at self._info field')
            return False

        return True

    def __read_item(self, item):
        param_attributes = item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                self.__read_item(child_item)
        else:
            self.read_parameter(item)

    def __write_item(self, item):
        param_attributes = item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                self.__write_item(child_item)
        else:
            self.write_parameter(item)

    def _param_convert_tree_to_list(self):
        root = self._device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.__convert_tree_branch_to_list(child_item)

    def __create_local_event_manager(self):
        self._local_event_manager = AQ_EventManager()

        self._local_event_manager.register_event_handler('add_param_to_update_stack', self.__add_param_to_update_stack)
