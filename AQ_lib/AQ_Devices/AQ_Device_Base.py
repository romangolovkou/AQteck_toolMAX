import abc

from AQ_CustomTreeItems import AQ_ParamItem
from AQ_EventManager import AQ_EventManager

class AQ_Device_Config:
    def __init__(self):
        super().__init__()
        self.device_name = ""
        self.saved_param_list = []

class AQ_Device_Base(abc.ABC):
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.local_event_manager = AQ_EventManager()
        self.device_tree = None
        self.params_list = []
        self.changed_param_stack = []
        self.update_param_stack = []

        self._info = {
            'name': None,
            'version': None,
            'serial_num': None
        }
        self._status = None
        self._functions = {
            'read_write': None,
            'rtc' = None,
            'password' = None,
            'calibration' = None,
            'log' = None,
            'fw_update' = None,
            'restart' = None
        }

    #Public functions

    @property
    def status(self):
        return self._status

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
    def __set_info(self, name, version, serial_num):
        """
            Fill self.info dict
            Example:
                self.info['name'] = 'MV210-101'
                self.info['version'] = '1.1.3'
                self.info['serial_num'] = '1333....'
            Left field empty if parameter doesn`t exist
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


