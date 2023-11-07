import threading
from abc import ABC, abstractmethod

from pymodbus.client import serial
import serial.tools.list_ports

from AQ_Connect import AQ_modbusRTU_connect, AQ_modbusTCP_connect
from AQ_CustomTreeItems import AQ_ParamItem
from AQ_EventManager import AQ_EventManager
from AQ_IsValidIpFunc import is_valid_ip
from AQ_TreeViewItemModel import AQ_TreeItemModel
from DeviceModels import AqDeviceInfoModel, AqDeviceConfig


class AqBaseDevice(ABC):
    def __init__(self, event_manager, connect, network_settings):
        self._event_manager = event_manager
        self._local_event_manager = None
        self._device_tree = None
        self._params_list = list()
        self._changed_param_stack = []
        self._update_param_stack = []
        self.connect = connect
        self._request_count = list()
        self._core_cv = threading.Condition()

        self._info = {
            'name':             None,
            'version':          None,
            'serial_num':       None,
            'connection':       None,
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

        # TODO: refactor this
        self.network_settings = network_settings
        self._event_manager.emit_event('create_new_connect', self)
        self.connect.open()

        if self.connect is not None and self.connect.open():
            self.init_device()
        else:
            return False

        # end refactor zone

        if self._device_tree is not None and isinstance(self._device_tree, AQ_TreeItemModel):
            self._device_tree.set_device(self)

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
        if items is None:
            self.read_all_parameters()
        elif isinstance(items, AQ_ParamItem):
            self.__read_item(items)
        elif isinstance(items, list):
            for i in range(len(items)):
                self.read_parameter(items[i])

        if len(self._update_param_stack) > 0:
            self._event_manager.emit_event('current_device_data_updated', self, self._update_param_stack)
            self._update_param_stack.clear()

    def read_all_parameters(self):
        root = self._device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.__read_item(child_item)

        self._update_param_stack.clear()
        self._event_manager.emit_event('current_device_data_updated', self)
        return

    @abstractmethod
    def read_parameter(self, item):
        """Read parameter from device"""
        return NotImplementedError

    @abstractmethod
    def write_parameter(self, item):
        """Write parameter to device"""
        return NotImplementedError

    def write_all_parameters(self):
        root = self._device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.write_parameter(child_item)

        self._event_manager.emit_event('current_device_data_written', self)

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

    # TODO: Refactor this
    def __create_client(self, address_tuple):
        interface = address_tuple[0]
        address = address_tuple[1]
        if interface == "Ethernet":
            if is_valid_ip(address):
                self._info['connection'] = 'IP'
                self._info['address'] = str(address)
                client = AQ_modbusTCP_connect(address)
                return client
        else:
            # Получаем список доступных COM-портов
            com_ports = serial.tools.list_ports.comports()
            for port in com_ports:
                if port.description == interface:
                    selected_port = port.device
                    boudrate = address_tuple[3]
                    parity = address_tuple[4][:1]
                    stopbits = address_tuple[5]
                    self._info['connection'] = str(selected_port)
                    self._info['address'] = str(address)
                    client = AQ_modbusRTU_connect(selected_port, boudrate, parity, stopbits, address)
                    return client

        return None
    # end refactor zone

    def __add_changed_param(self, item):
        self._changed_param_stack.append(item)

    def __add_param_to_update_stack(self, item):
        self._update_param_stack.append(item)

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

    def __param_convert_tree_to_list(self):
        root = self._device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.__convert_tree_branch_to_list(child_item)

    def __create_local_event_manager(self):
        self._local_event_manager = AQ_EventManager()

        for item in self._params_list:
            item.set_local_event_manager(self._local_event_manager)

        self._local_event_manager.register_event_handler('param_changed', self.__add_changed_param)
        self._local_event_manager.register_event_handler('param_need_update', self.__add_param_to_update_stack)
