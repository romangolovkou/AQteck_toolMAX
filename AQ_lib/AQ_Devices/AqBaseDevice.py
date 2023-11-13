import threading
from abc import ABC, abstractmethod

from pymodbus.client import serial
import serial.tools.list_ports

from AqConnect import AqConnect
from AQ_CustomTreeItems import AqParamItem
from AQ_EventManager import AQ_EventManager
from AQ_IsValidIpFunc import is_valid_ip
from AQ_TreeViewItemModel import AQ_TreeItemModel
from DeviceModels import AqDeviceInfoModel, AqDeviceConfig


class AqBaseDevice(ABC):
    def __init__(self, event_manager, connect: AqConnect):
        self._event_manager = event_manager
        self._local_event_manager = None
        self._device_tree = None
        self._connect = connect
        self._params_list = list()
        self._update_param_stack = []
        self._request_count = list()
        self._stack_to_read = list()
        self._stack_to_write = list()
        self._core_cv = threading.Condition()

        self._info = {
            'name':             None,
            'version':          None,
            'serial_num':       None,
            'address':          None
        }
        self._status = None
        self._functions = {
            'read_write': None,
            'rtc': None,
            'password': True,
            'calibration': None,
            'log': None,
            'fw_update': None,
            'restart': None
        }

        if self._connect is not None and self._connect.open():
            self._info['address'] = self._connect.address_string()
        else:
            raise Exception('AqBaseDeviceError: can`t open connect')

        if not self.init_device():
            raise Exception('AqBaseDeviceError: can`t initialize device')

        if self._device_tree is not None and isinstance(self._device_tree, AQ_TreeItemModel):
            self._device_tree.set_device(self)
        else:
            raise Exception('AqBaseDeviceError: device_tree isn`t exists')

        self.__param_convert_tree_to_list()
        self.__create_local_event_manager()
        # self.__verify()

    @property
    def status(self):
        return self._status

    @property
    def device_tree(self):
        return self._device_tree

    def func(self, name: str):
        return self._functions[name]

    def info(self, param):
        return self._info[param]

    def init_parameters(self):
        self._event_manager.register_event_handler('current_device_data_updated', self.read_complete)
        # TODO: check for offline connectivity
        for i in self._params_list:
            self.read_parameters(i)
            with self._core_cv:
                self._core_cv.wait()
                # TODO: Установить значение по умолчанию или 0

        self._event_manager.unregister_event_handler('current_device_data_updated', self.read_complete)
        return True

    def read_complete(self, device, item):
        if device == self:
            with self._core_cv:
                self._core_cv.notify()

    def read_parameters(self, items=None):
        if len(self._request_count) == 0:
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

            self._request_count.append(len(self._stack_to_read))
            self._connect.create_param_request('read', self._stack_to_read)

    def write_parameters(self, items=None):
        if len(self._request_count) == 0:
            if items is None:
                root = self.device_tree.invisibleRootItem()
                for row in range(root.rowCount()):
                    child_item = root.child(row)
                    self.__write_item(child_item)
            else:
                if isinstance(items, AqParamItem):
                    items = list(items)
                for i in range(len(items)):
                    self.__write_item(items[i])

            self._request_count.append(len(self._stack_to_write))
            self._connect.create_param_request('write', self._stack_to_write)

    @abstractmethod
    def read_parameter(self, item):
        """Read parameter from device"""
        return NotImplementedError

    @abstractmethod
    def write_parameter(self, item):
        """Read parameter from device"""
        return NotImplementedError

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
            if len(self._update_param_stack) == self._request_count[0]:
                self._request_count.pop(0)
                self._event_manager.emit_event('current_device_data_updated', self, self._update_param_stack)
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

    def __param_convert_tree_to_list(self):
        root = self._device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.__convert_tree_branch_to_list(child_item)

    def __create_local_event_manager(self):
        self._local_event_manager = AQ_EventManager()

        for item in self._params_list:
            item.set_local_event_manager(self._local_event_manager)

        self._local_event_manager.register_event_handler('add_param_to_update_stack', self.__add_param_to_update_stack)
