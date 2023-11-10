import asyncio
import threading
import time
from PySide6.QtCore import QThread, Signal, QObject
from pymodbus.client import serial
import serial.tools.list_ports

from AQ_Connect import AQ_modbusTCP_connect, AQ_modbusRTU_connect, AQ_IP_Connect_settings, AQ_COM_Connect_settings, \
    AQ_Modbus_Connect
from AQ_IsValidIpFunc import is_valid_ip


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
        connect_settings = self.get_connect_settings(network_settings)
        if connect_settings is not None:
            try:
                connect = AQ_Modbus_Connect(connect_settings, network_settings.get('address', 1), self.core_cv)
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
                return AQ_IP_Connect_settings(_ip=ip)
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
                return AQ_COM_Connect_settings(_port=selected_port,
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
            # function = request.get('method', None)
            # func = request.get('func', None)
            # start = request.get('start', None)
            # count = request.get('count', None)
            # callback = request.get('callback', None)
            # if func is not None and start is not None\
            #         and count is not None and callback is not None:
            connect.proceed_request(request)

    async def proceedFileRequest(self, req_data):
        data_storage = req_data['data']
        time.sleep(random.uniform(0.1, 2.0))
        data_storage = random.randint(50, 100)

    # def add_request(self, request):
    #     self.request_stack.append(request)
    #     with self.core_cv:
    #         self.core_cv.notify()

    def wrapper_call(self, request):
        request()


# class AQ_Modbus___Connect():
#     def __init__(self):
#         self.param_request_stack = []
#         self.file_request_stack = []
#         self.core_cv = threading.Condition()
#
#     def createParamRequest(self, func, start, count, data):
#         self.param_request_stack.append({'func': func, 'start': start,
#                                          'count': count, 'data': data})
#         with self.core_cv:
#             self.core_cv.notify()
#
#     def createFileRequest(self, func, file_num, record_num, record_len, data):
#         self.file_request_stack.append({'func': func, 'file_num': file_num,
#                                         'record_num': record_num, 'record_len': record_len, 'data': data})
#         with self.core_cv:
#             self.core_cv.notify()





