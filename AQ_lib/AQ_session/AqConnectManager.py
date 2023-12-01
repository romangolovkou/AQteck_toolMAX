import asyncio
import threading
import time
from random import random

from pymodbus.client import serial
import serial.tools.list_ports

from AQ_IsValidIpFunc import is_valid_ip
from AqConnect import AqOfflineConnect, AqModbusConnect, AqConnect
from AqConnect import AqIpConnectSettings, AqComConnectSettings


class AqConnectManager(object):

    event_manager = None
    core_cv = None
    core_thread = None
    connect_list = []
    request_stack = []

    @classmethod
    def init(cls, event_manager):
        cls.event_manager = event_manager
        cls.core_cv = threading.Condition()
        cls.core_thread = threading.Thread(target=cls.run)
        cls.core_thread.start()

    @classmethod
    def run(cls):
        asyncio.run(cls.proceed())

    @classmethod
    async def proceed(cls):
        with AqConnectManager.core_cv:
            while True:
                cls.core_cv.wait()
                for i in range(len(cls.connect_list)):
                    while len(cls.connect_list[i].param_request_stack) > 0:
                        await cls.proceedParamRequest(cls.connect_list[i])
                    while len(cls.connect_list[i].file_request_stack) > 0:
                        await cls.proceedFileRequest(cls.connect_list[i].param_request_stack.pop())

    @classmethod
    def create_connect(cls, network_settings) -> AqConnect:
        connect = None
        if network_settings.get('interface') == 'Offline':
            connect = AqOfflineConnect(cls.core_cv)
            cls.connect_list.append(connect)
        else:
            connect_settings = cls.get_connect_settings(network_settings)
            if connect_settings is not None:
                try:
                    connect = AqModbusConnect(connect_settings, network_settings.get('address', 1), cls.core_cv)
                    if connect.open():
                        connect.close()
                        cls.connect_list.append(connect)
                    else:
                        connect = 'connect_error'
                except Exception as e:
                    print(str(e))
        return connect

    @staticmethod
    def get_connect_settings(network_settings):
        if network_settings.get('ip', False):
            ip = network_settings.get('ip', None)
            if ip is not None and is_valid_ip(ip):
                return AqIpConnectSettings(_ip=ip)
        elif network_settings.get('boudrate', False):
            interface = network_settings.get('interface', None)
            # Получаем список доступных COM-портов
            com_ports = serial.tools.list_ports.comports()
            for port in com_ports:
                if port.description == interface:
                    selected_port = port.device

            boudrate = network_settings.get('boudrate', None)
            parity = network_settings.get('parity', None)
            stopbits = network_settings.get('stopbits', None)

            if selected_port is not None and \
                    boudrate is not None and \
                    parity is not None and \
                    stopbits is not None:
                return AqComConnectSettings(_port=selected_port,
                                            _baudrate=boudrate,
                                            _parity=parity,
                                            _stopbits=stopbits)

        return None

    @staticmethod
    async def proceedParamRequest(connect):
        for i in range(len(connect.param_request_stack)):
            request = connect.param_request_stack.pop()
            connect.proceed_request(request)

    @staticmethod
    async def proceedFileRequest(req_data):
        data_storage = req_data['data']
        time.sleep(random.uniform(0.1, 2.0))
        data_storage = random.randint(50, 100)










