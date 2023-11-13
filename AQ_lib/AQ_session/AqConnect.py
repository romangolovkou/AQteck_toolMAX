from abc import abstractmethod

from PySide6.QtCore import QObject
from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.file_message import ReadFileRecordRequest, WriteFileRecordRequest
from pymodbus.pdu import ModbusResponse


class AqConnect(QObject):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def create_param_request(self, method, stack):
        pass

    def read_param(self, item):
        pass

    def write_param(self, item):
        pass

    @abstractmethod
    def address_string(self):
        pass


class AqIpConnectSettings:
    def __init__(self, _ip):
        super().__init__()
        self.ip = _ip

    @property
    def addr(self):
        return 'IP: '+ str(self.ip)


class AqComConnectSettings:
    def __init__(self, _port, _baudrate, _parity, _stopbits):
        super().__init__()
        self.port = _port
        self.baudrate = _baudrate
        self.parity = _parity
        self.stopbits = _stopbits
        self._interface = _port

    @property
    def addr(self):
        return str(self.port)


class AqModbusConnect(AqConnect):

    def __init__(self, connect_settings, slave_id, core_cv):
        super().__init__()
        self.connect_settings = connect_settings
        self.core_cv = core_cv
        self.param_request_stack = []
        self.file_request_stack = []
        self.timeout = 1.0
        if type(self.connect_settings).__name__ == 'AqComConnectSettings':
            self.client = ModbusSerialClient(method='rtu',
                                                    port=self.connect_settings.port,
                                                    baudrate=self.connect_settings.baudrate,
                                                    parity=self.connect_settings.parity[:1],
                                                    stopbits=self.connect_settings.stopbits,
                                                    timeout=self.timeout)
            self.slave_id = slave_id
        elif type(self.connect_settings).__name__ == 'AqIpConnectSettings':
            self.client = ModbusTcpClient(self.connect_settings.ip)
            self.slave_id = 1
        else:
            Exception('Помилка. Невідомі налаштування коннекту')

    def address_string(self):
        if type(self.connect_settings).__name__ == 'AqIpConnectSettings':
            return self.connect_settings.addr
        else:
            return str(self.slave_id) + ' (' + self.connect_settings.addr + ')'

    def open(self):
        return self.client.connect()

    def close(self):
        self.client.close()

    def create_param_request(self, method, stack):
        request_stack = list()
        for i in range(len(stack)):
            request = dict()
            if method == 'read':
                request['method'] = self.read_param
            elif method == 'write':
                request['method'] = self.write_param
            else:
                raise Exception('AqConnectError: unknown stack name')

            request['item'] = stack[i]

            # Формируем запрос
            request_stack.append(request)

        self.param_request_stack = request_stack
        with self.core_cv:
            self.core_cv.notify()
        # self.param_request_stack = request_stack
        # with self.core_cv:
        #     self.core_cv.notify()

    def createFileRequest(self, func, file_num, record_num, record_len, data):
        self.file_request_stack.append({'func': func, 'file_num': file_num,
                                        'record_num': record_num, 'record_len': record_len, 'data': data})
        with self.core_cv:
            self.core_cv.notify()

    def proceed_request(self, request):
        # function = request.get('method', None)
        #
        # if function.__name__ == 'read_param':
        #     func = request.get('func', None)
        #     start = request.get('start', None)
        #     count = request.get('count', None)
        #     callback = request.get('callback', None)
        #     if func is not None and start is not None \
        #             and count is not None and callback is not None:
        #         function(func, start, count, callback)
        # elif function.__name__ == 'write_param':
        #     func = request.get('func', None)
        #     start = request.get('start', None)
        #     data = request.get('data', None)
        #     callback = request.get('callback', None)
        #     if func is not None and start is not None \
        #             and data is not None:
        #         function(func, start, data, callback)
        function = request.get('method', None)

        if function is not None:
            # if function.__name__ == 'read_param':
            function(request.get('item', None))
        # elif function.__name__ == 'write_param':
        #     function(request.get('item', None))
        else:
            raise Exception('AqConnectError: unknown "method"')

    def read_param(self, item):
        if item is not None:
            param_attributes = item.get_param_attributes()

            param_size = param_attributes.get('param_size', '')
            modbus_reg = param_attributes.get('modbus_reg', '')
            func = param_attributes.get('read_func', '')

            if func != '' and param_size != '' and modbus_reg != '':
                byte_size = param_size
                if byte_size < 2:
                    count = 1
                else:
                    count = byte_size // 2
            else:
                raise Exception('AqConnectError: in {} attributes "func"\
                                             or "param_size" or "modbus_reg" not exist'.format(item.__name__))

            if func == 3:
                result = self.client.read_holding_registers(modbus_reg, count, self.slave_id)
            elif func == 2:
                result = self.client.read_discrete_inputs(modbus_reg, 1, self.slave_id)
            elif func == 1:
                result = self.client.read_coils(modbus_reg, 1, self.slave_id)
            else:
                return 'modbus_error'

            if isinstance(result, ModbusIOException):
                # return 'modbus_error'
                item.data_from_network(None, True, 'modbus_error')
            else:
                item.data_from_network(result)

    def write_param(self, item):
        if item is not None:
            param_attributes = item.get_param_attributes()

            modbus_reg = param_attributes.get('modbus_reg', '')
            func = param_attributes.get('write_func', '')
            data = item.data_for_network()
            try:
                result = None
                if func == 16:
                    result = self.client.write_registers(modbus_reg, data, self.slave_id)
                elif func == 5:
                    # Запись одного дискретного выхода (бита)
                    result = self.client.write_coil(modbus_reg, data, self.slave_id)
                elif func == 6:
                    # TODO: перенести костыль в функцию в расслыку широковещательного запроса
                    if modbus_reg == 100:
                        # Для регістру 64 (слейв адреса пристрою) посилаємо широкомовний запит (Broadcast)
                        result = self.client.write_register(modbus_reg, data, 0)
                        if not isinstance(result, ModbusIOException):
                            self.slave_id = data
                    else:
                        # Запись одного регистра
                        result = self.client.write_register(modbus_reg, data, self.slave_id)

                if isinstance(result, ModbusIOException):
                    item.confirm_writing(False, 'modbus_error')
                else:
                    item.confirm_writing(True)

            except Exception as e:
                print(f"Error occurred: {str(e)}")
                raise

    def read_file_record(self, file_number, record_number, record_length):
        # Создание экземпляра структуры ReadFileRecordRequest
        request = ReadFileRecordRequest(self.slave_id)
        # Установка значений полей структуры
        request.file_number = file_number
        request.record_number = record_number
        request.record_length = record_length
        result = self.client.read_file_record(self.slave_id, [request])

        return result
#
# class AQ_COM_connect(AQ_connect):
#     def __init__(self):
#         super().__init__()
#
#
# class AQ_TCP_connect(AQ_connect):
#     def __init__(self):
#         super().__init__()
#
#
# class AQ_modbusRTU_connect(AQ_COM_connect):
#     def __init__(self, connect_manager, _port, _baudrate, _parity, _stopbits, slave_id):
#         super().__init__()
#         self.slave_id = slave_id
#         self.start_address = None
#         self.register_count = None
#         self.func = None
#         self.connect_manager = connect_manager
#         self.timeout = 1.0
#         self.modbus_rtu_client = ModbusSerialClient(method='rtu', port=_port, baudrate=_baudrate, parity=_parity,
#                                                     stopbits=_stopbits, timeout=self.timeout)
#
#     def open(self):
#         return self.modbus_rtu_client.connect()
#
#     def close(self):
#         self.modbus_rtu_client.close()
#
#     # def request(self, callback,  start_address, register_count, func):
#     #     self.start_address = start_address
#     #     self.register_count = register_count
#     #     self.func = func
#     #     self.callback = callback
#     #     if func == 3 or func == 2 or func == 1:
#     #         self.connect_manager.add_request(self.read_param)
#
#     def read_param(self):
#         if self.func == 3:
#             response = self.modbus_rtu_client.read_holding_registers(self.start_address, self.register_count, self.slave_id)
#             if isinstance(response, ModbusIOException):
#                 response = 'modbus_error'
#
#             # return response
#             self.callback(response)
#         elif self.func == 2:
#             result = self.modbus_rtu_client.read_discrete_inputs(self.start_address, 1, self.slave_id)
#             if isinstance(result, ModbusIOException):
#                 return 'modbus_error'
#             # return result.bits
#             self.callback(result.bits)
#         elif self.func == 1:
#             result = self.modbus_rtu_client.read_coils(self.start_address, 1, self.slave_id)
#             if isinstance(result, ModbusIOException):
#                 return 'modbus_error'
#             # return result.bits
#             self.callback(result.bits)
#
#
#     def read_file_record(self, file_number, record_number, record_length):
#         # Создание экземпляра структуры ReadFileRecordRequest
#         request = ReadFileRecordRequest(self.slave_id)
#         # Установка значений полей структуры
#         request.file_number = file_number
#         request.record_number = record_number
#         request.record_length = record_length
#         result = self.modbus_rtu_client.read_file_record(self.slave_id, [request])
#
#         return result
#
#     def write_param(self, modbus_reg, registers, write_func):
#         try:
#             result = None
#             if write_func == 16:
#                 result = self.modbus_rtu_client.write_registers(modbus_reg, registers, self.slave_id)
#             elif write_func == 5:
#                 # Запись одного дискретного выхода (бита)
#                 result = self.modbus_rtu_client.write_coil(modbus_reg, registers, self.slave_id)
#             elif write_func == 6:
#                 if modbus_reg == 100:
#                     # Для регістру 64 (слейв адреса пристрою) посилаємо широкомовний запит (Broadcast)
#                     result = self.modbus_rtu_client.write_register(modbus_reg, registers, 0)
#                     if not isinstance(result, ModbusIOException):
#                         self.slave_id = registers
#                 else:
#                     # Запись одного регистра
#                     result = self.modbus_rtu_client.write_register(modbus_reg, registers, self.slave_id)
#
#             if isinstance(result, ModbusIOException):
#                 result = 'modbus_error'
#
#             return result
#         except Exception as e:
#             print(f"Error occurred: {str(e)}")
#             raise
#
#
#     def write_file_record(self, file_number, record_number, record_length, record_data):
#         # Создание экземпляра структуры WriteFileRecordRequest
#         request = WriteFileRecordRequest(self.slave_id)
#         # Установка значений полей структуры
#         request.file_number = file_number
#         request.record_number = record_number
#         request.record_length = record_length
#         request.record_data = record_data
#         result = self.modbus_rtu_client.write_file_record(self.slave_id, [request])
#
#         return result
#
#
# class AQ_modbusTCP_connect(AQ_TCP_connect):
#     def __init__(self, ip):
#         super().__init__()
#         self.slave_id = 1
#         self.modbus_tcp_client = ModbusTcpClient(ip)
#
#     def open(self):
#         self.modbus_tcp_client.connect()
#
#     def close(self):
#         self.modbus_tcp_client.close()
#
#     def read_holding_registers(self, start_address, register_count):
#         response = self.modbus_tcp_client.read_holding_registers(start_address, register_count, self.slave_id)
#         return response
#
#     def read_file_record(self, file_number, record_number, record_length):
#         # Создание экземпляра структуры ReadFileRecordRequest
#         request = ReadFileRecordRequest(self.slave_id)
#         # Установка значений полей структуры
#         request.file_number = file_number
#         request.record_number = record_number
#         request.record_length = record_length
#         result = self.modbus_tcp_client.read_file_record(self.slave_id, [request])
#
#         return result
#
#     def write_registers(self, modbus_reg, registers):
#         try:
#             result = self.modbus_tcp_client.write_registers(modbus_reg, registers, self.slave_id)
#             if isinstance(result, ModbusIOException):
#                 result = 'modbus_error'
#
#             return result
#         except Exception as e:
#             print(f"Error occurred: {str(e)}")
#             raise
#
#     def write_file_record(self, file_number, record_number, record_length, record_data):
#         # Создание экземпляра структуры WriteFileRecordRequest
#         request = WriteFileRecordRequest(self.slave_id)
#         # Установка значений полей структуры
#         request.file_number = file_number
#         request.record_number = record_number
#         request.record_length = record_length
#         request.record_data = record_data
#         result = self.modbus_tcp_client.write_file_record(self.slave_id, [request])
#
#         return result
#
#
# class AQ_ModbusConnect():
#     def __init__(self):
#         self.param_request_stack = []
#         self.file_request_stack = []
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