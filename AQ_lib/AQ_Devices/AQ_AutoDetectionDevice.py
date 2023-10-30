import AQ_BaseDevice


class AQ_AutoDetectionDevice(AQ_BaseDevice):

    _system_param_reg = {
        'name':     {0xF000, 16},
        'version':  {}
    }

    #Add to init all what we need
    def __init__(self, event_manager, connect):
        super().__init__(event_manager, connect)

    def __init_device(self):
        self._info['name'] = self.__read_name()
        return True

    def __read_from_device(self, param_name):
        #read from device and return device name
        if param_name == 'name':
            modbus_reg = 0xF000
            modbus_cnt = 16
        elif param_name == 'version'
        return "AutoDetectionDevice"
