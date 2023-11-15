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
    def __init__(self, event_manager, connect: AqModbusConnect, network_settings):
        super().__init__(event_manager, connect)
        self._connect = connect

    def init_device(self) -> bool:
        self._info['name'] = self.__read_string('name')
        self._info['version'] = self.__read_string('version')
        self._info['serial_num'] = self.__read_string('serial_num')
        self._info['password'] = None

        self._device_tree = None
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

    # def __read_string(self, name):
    #     try:
    #         # Выполняем запрос
    #         response = self._connect.read_param(self._system_string[name][2],
    #                                             self._system_string[name][0],
    #                                             self._system_string[name][1])
    #     except Exception as e:
    #         print(f"Error occurred: {str(e)}")
    #         self._status = 'connect_err'
    #         return None
    #
    #     # Конвертируем значения регистров в строку
    #     hex_string = ''.join(format(value, '04X') for value in response.registers)
    #     # Конвертируем строку в массив байт
    #     byte_array = bytes.fromhex(hex_string)
    #     byte_array = swap_bytes_at_registers(byte_array, self._system_string[name][1])
    #     # Расшифровуем в строку
    #     text = byte_array.decode('ANSI')
    #     result_str = remove_empty_bytes(text)
    #
    #     return result_str

    # TODO: wait until we will have good items and refactor this
    def read_parameter(self, item):
        """Read parameter from device"""
        self._stack_to_read.append(item)
        # param_attributes = item.get_param_attributes()
        #
        # param_type = param_attributes.get('type', '')
        # param_size = param_attributes.get('param_size', '')
        # modbus_reg = param_attributes.get('modbus_reg', '')
        #
        # if param_type != '' and param_size != '' and modbus_reg != '':
        #     if param_type == 'enum':
        #         if param_size > 16:
        #             reg_count = 2
        #             byte_size = 4
        #         else:
        #             reg_count = 1
        #             byte_size = 1
        #     else:
        #         byte_size = param_size
        #         if byte_size < 2:
        #             reg_count = 1
        #         else:
        #             reg_count = byte_size // 2
        #     # Формируем запрос
        #     self._stack_to_read.append({'method': self._connect.read_param, 'func': 3, 'start': modbus_reg,
        #                                 'count': reg_count, 'callback': item.data_from_network})

    # TODO: refactor this huge function
    def write_parameter(self, item):
        if item.get_status() == 'changed':
            # param_attributes = item.get_param_attributes()
            #
            # modbus_reg = param_attributes.get('modbus_reg', '')
            # write_func = param_attributes.get('write_func', '')
            # data = item.data_for_network()
            #
            # self._stack_to_write.append({'method': self._connect.write_param, 'func': 16, 'start': modbus_reg,
            #                              'data': data, 'callback': item.confirm_writing})
            self._stack_to_write.append(item)

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
