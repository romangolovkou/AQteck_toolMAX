import asyncio
import threading
import time
from PySide6.QtCore import QThread, Signal, QObject
from pymodbus.client import serial
import serial.tools.list_ports

from AqConnect import AqIpConnectSettings, AqComConnectSettings, AqModbusConnect, AqOfflineConnect
from AqIsValidIpFunc import is_valid_ip


class AQ_ConnectManager(QObject):
    def __init__(self, event_manager, parent):
        super().__init__(parent)
        self.event_manager = event_manager
        self.request_stack = []
        self.connect_list = []

        self.event_manager.register_event_handler('create_new_connect', self.create_connect)

        self.core_cv = threading.Condition()

        self.core_thread = threading.Thread(target=self.run)
        self.core_thread.start()

    def create_connect(self, network_settings, callback_dict):
        if network_settings.get('interface') == 'Offline':
            connect = AqOfflineConnect(self.core_cv)
            callback_dict['connect'] = connect
            self.connect_list.append(connect)
        else:
            connect_settings = self.get_connect_settings(network_settings)
            if connect_settings is not None:
                try:
                    connect = AqModbusConnect(connect_settings, network_settings.get('address', 1), self.core_cv)
                    if connect.open():
                        connect.close()
                        self.connect_list.append(connect)
                        callback_dict['connect'] = connect
                    else:
                        callback_dict['connect'] = 'connect_error'
                except Exception as e:
                    print(str(e))

    def get_connect_settings(self, network_settings):
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

    def run(self):
        asyncio.run(self.proceed())

    async def proceed(self):
        with self.core_cv:
            while True:
                self.core_cv.wait()
                for i in range(len(self.connect_list)):
                    while len(self.connect_list[i].param_request_stack) > 0:
                        await self.proceedParamRequest(self.connect_list[i])
                    while len(self.connect_list[i].file_request_stack) > 0:
                        await self.proceedFileRequest(self.connect_list[i].param_request_stack.pop())

    async def proceedParamRequest(self, connect):
        for i in range(len(connect.param_request_stack)):
            request = connect.param_request_stack.pop()
            connect.proceed_request(request)

    async def proceedFileRequest(self, req_data):
        data_storage = req_data['data']
        time.sleep(random.uniform(0.1, 2.0))
        data_storage = random.randint(50, 100)
