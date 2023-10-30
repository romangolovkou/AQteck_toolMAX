import abc

from AQ_CustomTreeItems import AQ_ParamItem
from AQ_EventManager import AQ_EventManager

class AQ_Device_Info_Model:

    def __init__(self):
        super().__init__()
        self.general_info = []
        self.operating_params_info = []

    def add_general_info(self, info_str, info_value):
        self.general_info.append({'info_str': info_str, 'info_value': info_value})

    def clear(self):
        self.general_info.clear()
        self.operating_params_info.clear()

class AQ_Device_Config:
    def __init__(self):
        super().__init__()
        self.device_name = ""
        self.saved_param_list = []

class AQ_BaseDevice(abc.ABC):
    def __init__(self, event_manager, connect):
        self._event_manager = event_manager
        self._local_event_manager = AQ_EventManager()
        self._device_tree = None
        self._params_list = []
        self._changed_param_stack = []
        self._update_param_stack = []

        self._info = {
            'name': None,
            'version': None,
            'serial_num': 'No S/N'
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

        self.__init_device()
        self.__set_functions_data()

        self.__verify()


    #Public functions
    @property
    def status(self):
        return self._status

    def func(self, name: str):
        return self._functions[name]

    @property
    def info(self, param: str):
        return self._info[param]

    def read_parameters(self, items=None):
        if items is None:
            self.read_all_parameters()
        elif isinstance(items, AQ_ParamItem):
            self.read_item(items)
        elif isinstance(items, list):
            for i in range(len(items)):
                self.read_parameter(items[i])

        if len(self.update_param_stack) > 0:
            self.event_manager.emit_event('current_device_data_updated', self, self.update_param_stack)
            self.update_param_stack.clear()

    def read_all_parameters(self):
        root = self.device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.read_item(child_item)

        self.update_param_stack.clear()
        self.event_manager.emit_event('current_device_data_updated', self)
        return

    @abc.abstractmethod
    def write_parameter(self, item):
        """Write parameter to device"""

    def write_all_parameters(self):
        root = self.device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.write_parameter(child_item)

        self.event_manager.emit_event('current_device_data_written', self)

    def restart(self):
        """
            Return NotImplemented by default.
            Redefine function at child class if it needed
        """
        return NotImplemented

    def fwUpdate(self, fwdata):
        """
            Return NotImplemented by default.
            Redefine function at child class if it needed
        """
        return NotImplemented

    def setRtc(self, rtc_data):
        """
            Return NotImplemented by default.
            Redefine function at child class if it needed
        """
        return NotImplemented

    def setPassword(self, rtc_data):
        """
            Return NotImplemented by default.
            Redefine function at child class if it needed
        """
        return NotImplemented

    def save_config(self):
        config = AQ_Device_Config()
        config.device_name = self.info('name')

        self.__make_config_data(config)

        return config

    #Private function
    def __add_changed_param(self, item):
        self.changed_param_stack.append(item)

    def __add_param_to_update_stack(self, item):
        self.update_param_stack.append(item)

    def __convert_tree_branch_to_list(self, item):
        param_attributes = item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                self.__convert_tree_branch_to_list(child_item)
        else:
            self.params_list.append(item)

    @abc.abstractmethod
    def __init_device(self) -> bool:
        """
            Init your device
            Fill self.info dict
            Example:
                self.info['name'] = 'MV210-101'
                self.info['version'] = '1.1.3'
                self.info['serial_num'] = '1333....'
            :return: True - init ok, False - init error
        """

    def __verify(self) -> bool:
        if not hasattr(self._info, 'name') or
            not hasattr(self._info, 'version') or
            not hasattr(self._info, 'serial')
            print('Failed to create ', self.__name__, 'object. '
                'No required attributes at self._info field')
            return False

        return True

    # @abc.abstractmethod
    # def __set_info(self, name, version, serial_num):
    #     """
    #         Fill self.info dict
    #         Example:
    #             self.info['name'] = 'MV210-101'
    #             self.info['version'] = '1.1.3'
    #             self.info['serial_num'] = '1333....'
    #         Left field empty if parameter doesn`t exist
    #     """

    @abc.abstractmethod
    def __set_functions_data(self):
        """
            Fill _functions dictionary for supported function in child class
            Example:
            self._functions = {
                'read_write': True,
                'password' = True,
                'restart' = True
            }
        """

    @abc.abstractmethod
    def __make_config_data(self, config_obj: AQ_Device_Config):
        """
            Fill saved_param_list with needed to save data
            Example:   config.saved_param_list.append(
                {'UID': param_attributes.get('UID', 0),
                 'modbus_reg': param_attributes.get('modbus_reg', 0),
                 'value': devParam.value})
        """

    def __read_item(self, item):
        param_attributes = item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            row_count = item.rowCount()
            for row in range(row_count):
                child_item = item.child(row)
                self.__read_item(child_item)
        else:
            self.read_parameter(item)

    @abc.abstractmethod
    def __read_parameter(self, item):
        """Read parameter from device"""

    def __param_convert_tree_to_list(self):
        root = self.device_tree.invisibleRootItem()
        for row in range(root.rowCount()):
            child_item = root.child(row)
            self.__convert_tree_branch_to_list(child_item)


