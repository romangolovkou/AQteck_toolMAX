from AqBaseDevice import AqBaseDevice
from AqConnect import AqModbusConnect
from AqDeviceConfig import AqDeviceConfig
from AqModbusTips import swap_bytes_at_registers, remove_empty_bytes


class AqGenericModbusDevice(AqBaseDevice):
    # Format: 'param_name': {start_reg, count, func}
    _system_string = {
        #     TODO: Fill from device_description class
    }
    _system_param = {}

    # Add to init all what we need
    def __init__(self, event_manager, connect: AqModbusConnect, configuration):
        self._configuration = configuration
        super().__init__(event_manager, connect)
        self._connect = connect

    def init_device(self) -> bool:
        self._info['name'] = self._configuration.dev_descr_dict.get('Name')

        self._device_tree = self._configuration.params_tree
        if self._device_tree == 'parsing_err' or \
                self._device_tree is None:
            self._status = 'error'
            return False

        # TODO: describe rules to chache which functions are supported
        # into AutoDetectionDevice
        # later should be json file inside device with definitions
        self._functions['read_write'] = False,
        self._functions['rtc'] = False
        self._functions['password'] = False
        self._functions['calibration'] = False
        self._functions['log'] = False
        self._functions['fw_update'] = False
        self._functions['restart'] = False

        self._status = 'ok'
        return True

    def get_configuration(self) -> AqDeviceConfig:
        config = AqDeviceConfig()
        config.device_name = self.info('name')

        for devParam in self._params_list:
            param_attributes = devParam.get_param_attributes()
            config.saved_param_list.append({'modbus_reg': param_attributes.get('modbus_reg', 0),
                                            'value': devParam.value})

        return config

    def set_configuration(self, config: AqDeviceConfig):
        if self.info('name') != config.device_name:
            return NotImplementedError
            # TODO: need generate custom exception or generate event to display error message

        for cfgParam in config.saved_param_list:
            for devParam in self._params_list:
                param_attributes = devParam.get_param_attributes()
                modbusReg = param_attributes.get('modbus_reg', 0)
                if cfgParam['modbus_reg'] == modbusReg:
                    devParam.value = cfgParam['value']
        # TODO: optimize this algorithm

        # self._event_manager.emit_event('current_device_data_updated', self, self._update_param_stack)
        self._event_manager.emit_event('current_device_data_updated', self)
