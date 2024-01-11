import os
import threading

import serial.tools.list_ports

from AqIsValidIpFunc import is_valid_ip
from AqAutoDetectionDevice import AqAutoDetectionDevice
from AqConnect import AqComConnectSettings, AqOfflineConnectSettings, AqIpConnectSettings
from AqConnectManager import AqConnectManager
from AqGenericModbusLibrary import read_configuration_file
# імпорти нижче не видаляти, потрібні для globals()
from AqGenericModbusDevice import AqGenericModbusDevice
PATH = '110_device_conf/'


class DeviceCreator(object):
    event_manager = None
    com_ports =None
    @classmethod
    def init(cls, _event_manager):
        cls.event_manager = _event_manager

    @classmethod
    def get_protocol_list(cls):
        protocol_list = list()
        protocol_list.append('Modbus')
        protocol_list.append('AqAutoDetectionProtocol')

        return protocol_list

    @classmethod
    def get_interface_list(cls):
        interface_list = list()
        interface_list.append('Offline')
        interface_list.append('Ethernet')
        cls.com_ports = serial.tools.list_ports.comports()
        # Заполняем выпадающий список COM-портами
        for port in cls.com_ports:
            interface_list.append(port.description)

        return interface_list

    @classmethod
    def get_device_list_by_protocol(cls, protocol):
        devices = list()
        if protocol == 'Modbus':
            # Получаем список файлов в указанной директории
            devices = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]

        return devices


    @classmethod
    def from_param_dict(cls, param_dict):
        device = None

        connect_settings = cls.__param_dict_to_connect_settings(param_dict)
        if connect_settings is not None:
            device_id = 1
            if param_dict.get('address', False):
                device_id = param_dict.get('address', None)
            connect = AqConnectManager.create_connect(connect_settings, device_id)
            if connect is not None:
                device = cls.__param_dict_to_device_object(param_dict, connect)

        return device

    @classmethod
    def __param_dict_to_device_object(cls, param_dict, connect):
        device = None

        device_type = param_dict.get('device_type')
        if device_type == 'AqAutoDetectionDevice':
            try:
                device = AqAutoDetectionDevice(cls.event_manager, connect)
            except Exception as e:
                print(f"{str(e)}")
                device = None
        elif device_type == 'AqFileDescriptionDevice':
            dev_name = param_dict.get('device', None)
            configuration = read_configuration_file(dev_name)
            class_name = configuration.dev_descr_dict.get('Type')
            try:
                device = globals()[str(class_name)](cls.event_manager, connect, configuration)
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                raise Exception(e)
        else:
            print(cls.__name__ + 'Error: no device type specified')

        return device

    # TODO: need print error, when didn`t find some argument
    @classmethod
    def __param_dict_to_connect_settings(cls, param_dict):
        # First check is offline connection as simplest
        if param_dict.get('interface_type') == 'Offline':
            return AqOfflineConnectSettings()
        # Then check if some Ethernet/WiFi
        elif param_dict.get('interface_type', False) == 'ip':
            ip = param_dict.get('ip', None)
            if ip is not None and is_valid_ip(ip):
                return AqIpConnectSettings(_ip=ip)
            else:
                return None
        # Then if is there some COM settings
        elif param_dict.get('interface_type', False) == 'com':
            interface = param_dict.get('interface', None)
            # Получаем список доступных COM-портов
            com_ports = serial.tools.list_ports.comports()
            for port in com_ports:
                if port.description == interface:
                    selected_port = port.device

            boudrate = param_dict.get('boudrate', None)
            parity = param_dict.get('parity', None)
            stopbits = param_dict.get('stopbits', None)

            if selected_port is not None and \
                    boudrate is not None and \
                    parity is not None and \
                    stopbits is not None:
                return AqComConnectSettings(_port=selected_port,
                                            _baudrate=boudrate,
                                            _parity=parity,
                                            _stopbits=stopbits)
        else:
            return None

    @classmethod
    def add_device(cls, devices: list):
        for device in devices:
            device.init_parameters()

        cls.event_manager.emit_event('add_new_devices', devices)
