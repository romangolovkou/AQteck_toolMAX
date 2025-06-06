import asyncio
from abc import abstractmethod
from collections import deque
from dataclasses import dataclass
from queue import Queue, PriorityQueue

from PySide6.QtCore import QObject, Signal
from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.file_message import ReadFileRecordRequest, WriteFileRecordRequest
from pymodbus.pdu import ModbusResponse, ExceptionResponse

from AQ_EventManager import AQ_EventManager
from AqIsValidIpFunc import is_valid_ip
from AqMessageManager import AqMessageManager
from AqTranslateManager import AqTranslateManager


class AqConnect(QObject):
    progress_updated = Signal(int, str)

    def __init__(self, notify):
        super().__init__()
        self.status = 'no status'
        self.notify = notify
        self.requestGroupProceedDoneCallback = None
        self.RequestGroupQueue = deque()
        self.message_manager = AqMessageManager.get_global_message_manager()

    @abstractmethod
    async def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def read_param(self, item):
        pass

    def write_param(self, item):
        pass

    async def proceedOneRequestGroup(self):
        if len(self.RequestGroupQueue) > 0:
            request_dict = self.RequestGroupQueue.popleft()
            request_stack = request_dict['request_stack']
            req_settings = request_dict['settings']
        else:
            print("WTF????")
            self.set_ready_flag()
            return
        method = None if len(request_stack) == 0 else request_stack[0]['method'].__name__
        connect_result = await self.open()
        if connect_result is True:
            for i in range(len(request_stack)):
                request = request_stack.pop()
                try:
                    await self.proceed_request(request)
                except Exception as e:
                    self.proceed_failed_request(request)
        else:
            for i in range(len(request_stack)):
                request = request_stack.pop()
                self.proceed_failed_request(request)
            self.RequestGroupQueue.clear()
            if req_settings.get('msg_feedback_address', False):
                self.message_manager.send_message('main', "Error", AqTranslateManager.tr('Can`t connect to device.') + " " +
                                                  AqTranslateManager.tr('Please check network settings and try again.'))
        self.close()
        self.requestGroupProceedDoneCallback(message_feedback_address=req_settings.get('msg_feedback_address', False),
                                             method=method)

        self.set_ready_flag()

    async def proceed_request(self, request):
        function = request.get('method', None)

        if function is not None:
            await function(request.get('item', None))
        else:
            raise Exception('AqConnectError: unknown "method"')

    def proceed_failed_request(self, request):
        item = request.get('item', None)
        function = request.get('method', None)
        if function.__name__ == 'read_param' or function.__name__ == 'read_file':
            item.data_from_network(None, True, 'modbus_error')
        elif function.__name__ == 'write_param' or function.__name__ == 'write_file':
            item.confirm_writing(False, 'modbus_error')


    def create_param_request(self, method, stack, message_feedback_address=False):
        request_stack = list()
        req_settings_dict = dict()
        request_dict = dict()
        for i in range(len(stack)):
            request = dict()
            if method == 'read':
                request['method'] = self.read_param
            elif method == 'write':
                request['method'] = self.write_param
            elif method == 'read_file':
                request['method'] = self.read_file
            elif method == 'write_file':
                request['method'] = self.write_file
            else:
                raise Exception('AqConnectError: unknown stack name')

            request['item'] = stack[i]

            # Формируем запрос
            request_stack.append(request)

        if message_feedback_address:
            req_settings_dict['msg_feedback_address'] = message_feedback_address

        request_dict['settings'] = req_settings_dict
        request_dict['request_stack'] = request_stack

        if method == 'write' or method == 'write_file':
            self.RequestGroupQueue.appendleft(request_dict)
        else:
            self.RequestGroupQueue.append(request_dict)

        self.set_ready_flag()

    def set_ready_flag(self):
        if len(self.RequestGroupQueue) > 0 and not self.mutex.locked():
            self.notify(self)

    def clear_existing_requests(self):
        # Очищаем очередь
        self.RequestGroupQueue.clear()

    @abstractmethod
    def address_string(self):
        pass

    def setRequestGroupProceedDoneCallback(self, callback):
        self.requestGroupProceedDoneCallback = callback

    @property
    def hasRequests(self):
        if len(self.RequestGroupQueue) > 0:
            return True
        else:
            return False


class AqIpConnectSettings:
    def __init__(self, _ip):
        super().__init__()

        if is_valid_ip(_ip):
            self.ip = _ip
        else:
            raise ValueError("Invalid ip " + str(_ip))

        self.mutex = None


    @property
    def addr(self):
        return 'IP: '+ str(self.ip)


class AqOfflineConnectSettings:
    def __init__(self):
        super().__init__()

    @property
    def addr(self):
        return 'Offline'


class AqComConnectSettings:
    available_baudrate = [4800, 9600, 19200, 38400, 57600, 115200]
    available_parity = ["None", "Even", "Odd"]
    available_stopbits = [1, 2]
    def __init__(self, _port, _baudrate, _parity, _stopbits):
        super().__init__()
        # TODO: Зачем нам хранить одно и тоже в разных переменных???
        self.port = _port
        self._interface = _port
        self.mutex = None

        if _baudrate in self.available_baudrate:
            self.baudrate = _baudrate
        else:
            raise ValueError("Invalid baudrate " + str(_baudrate))
        if _parity in self.available_parity:
            self.parity = _parity
        else:
            raise ValueError("Invalid parity " + str(_parity))
        if _stopbits in self.available_stopbits:
            self.stopbits = _stopbits
        else:
            raise ValueError("Invalid stopbits " + str(_parity))


    @property
    def addr(self):
        return str(self.port)


@dataclass
class RequestGroup:
    connect: AqConnect
    requestStack: list


class AqModbusConnect(AqConnect):

    def __init__(self, connect_settings, slave_id, notify):
        super().__init__(notify)
        self.connect_settings = connect_settings
        self.file_request_stack = []
        self.timeout = 10.0
        self.mutex = connect_settings.mutex
        self.event_manager = AQ_EventManager.get_global_event_manager()
        if isinstance(self.connect_settings, AqComConnectSettings):
            self.client = AsyncModbusSerialClient(method='rtu',
                                                    port=self.connect_settings.port,
                                                    baudrate=self.connect_settings.baudrate,
                                                    parity=self.connect_settings.parity[:1],
                                                    stopbits=self.connect_settings.stopbits,
                                                    timeout=self.timeout,
                                                    retries=0)
            self.slave_id = slave_id
        elif isinstance(self.connect_settings, AqIpConnectSettings):
            self.client = AsyncModbusTcpClient(self.connect_settings.ip)
            self.slave_id = 1
        else:
            Exception('Помилка. Невідомі налаштування коннекту')

    # def set_new_client_settings(self, ip=None, port=None, baudrate=None, parity=None,
    #                             stopbits=None, timeout=None, retries=None, slave_id=None):
    #     try:
    #         if ip is None:
    #             self.connect_settings = AqComConnectSettings(_port=port if port is not None else self.connect_settings.port,
    #                                                         _baudrate=baudrate if baudrate is not None else self.connect_settings.baudrate,
    #                                                         _parity=parity if parity is not None else self.connect_settings.parity,
    #                                                         _stopbits=stopbits if stopbits is not None else self.connect_settings.stopbits)
    #
    #             self.timeout = timeout if timeout is not None else self.timeout
    #
    #             self.client = AsyncModbusSerialClient(method='rtu',
    #                                                     port=self.connect_settings.port,
    #                                                     baudrate=self.connect_settings.baudrate,
    #                                                     parity=self.connect_settings.parity[:1],
    #                                                     stopbits=self.connect_settings.stopbits,
    #                                                     timeout=self.timeout,
    #                                                     retries=retries if retries is not None else 0)
    #
    #             self.slave_id = slave_id if slave_id is not None else self.slave_id
    #
    #         else:
    #             self.connect_settings = AqIpConnectSettings(_ip=ip)
    #             self.client = AsyncModbusTcpClient(self.connect_settings.ip)
    #             self.slave_id = 1
    #
    #     except Exception as e:
    #         Exception('Помилка. Невідомі налаштування коннекту')

    def address_string(self):
        if isinstance(self.connect_settings, AqIpConnectSettings):
            return self.connect_settings.addr
        else:
            return str(self.slave_id) + ' (' + self.connect_settings.addr + ')'

    async def open(self):
        await self.mutex.acquire()
        result = await self.client.connect()
        self.status = 'connect_ok' if result else 'connect_err'
        return result

    def close(self):
        self.client.close()
        if self.mutex.locked():
            self.mutex.release()
            self.set_ready_flag()

    async def read_param(self, item):
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
            try:
                if func == 3:
                    result = await self.client.read_holding_registers(modbus_reg, count, self.slave_id)
                elif func == 2:
                    result = await self.client.read_discrete_inputs(modbus_reg, 1, self.slave_id)
                elif func == 1:
                    result = await self.client.read_coils(modbus_reg, 1, self.slave_id)
                else:
                    item.data_from_network(None, True, 'modbus_error')
                    raise Exception('AqConnectError: in {} attributes "func" is not supported'.format(
                        item.__name__))
            except Exception:
                self.status = 'connect_err'
                item.data_from_network(None, True, 'modbus_error')
                return

            if isinstance(result, ModbusIOException):
                # return 'modbus_error'
                item.data_from_network(None, True, 'modbus_error')
            elif isinstance(result, ExceptionResponse):
                self.status = 'connect_err'
                item.data_from_network(None, True, 'modbus_error')
                return
            else:
                item.data_from_network(result)

    async def write_param(self, item):
        if item is not None:
            param_attributes = item.get_param_attributes()

            modbus_reg = param_attributes.get('modbus_reg', '')
            func = param_attributes.get('write_func', '')
            data = item.data_for_network()
            try:
                result = None
                if func == 16:
                    result = await self.client.write_registers(modbus_reg, data, self.slave_id)
                elif func == 5:
                    # Запись одного дискретного выхода (бита)
                    result = await self.client.write_coil(modbus_reg, data, self.slave_id)
                elif func == 6:

                    if item.param_size < 2:
                        data = data[0]
                    else:
                        low_byte = data[0]
                        high_byte = data[1]
                        # Восстановление 16-битного числа
                        data = (high_byte << 8) | low_byte
                    # TODO: перенести костыль в функцию в расслыку широковещательного запроса
                    # if modbus_reg == 100:
                    #     # Для регістру 64 (слейв адреса пристрою) посилаємо широкомовний запит (Broadcast)
                    #     result = await self.client.write_register(modbus_reg, data, 0)
                    #     if not isinstance(result, ModbusIOException):
                    #         self.slave_id = data
                    # else:
                    # Запись одного регистра
                    result = await self.client.write_register(modbus_reg, data, self.slave_id)

                if isinstance(result, ModbusIOException):
                    item.confirm_writing(False, 'modbus_error')
                else:
                    item.confirm_writing(True)

            except Exception as e:
                print(f"Error occurred: {str(e)}")
                raise

    async def read_file(self, item):
        if item is not None:
            max_record_size = 124
            param_attributes = item.get_param_attributes()

            file_num = param_attributes.get('file_num', '')
            start_record_num = param_attributes.get('start_record_num', '')
            left_to_read = param_attributes.get('file_size', '')
            summary_data = bytearray()
            while left_to_read > 0:
                # read_size = max_record_size if left_to_read > max_record_size else left_to_read
                read_size = max_record_size
                result = None
                request = ReadFileRecordRequest(self.slave_id)
                request.file_number = file_num
                request.record_number = start_record_num
                request.record_length = read_size

                try:
                    if left_to_read < 14000:
                        x = 20 + 4
                    result = await self.client.read_file_record(self.slave_id, [request])
                    start_record_num += read_size
                    left_to_read -= read_size
                except Exception as e:
                    print(f"Error occurred: {str(e)}")
                    item.data_from_network(None, True, 'modbus_error')
                    return

                try:
                    summary_data += result.records[0].record_data
                except Exception as e:
                    left_to_read = 0

            item.data_from_network(summary_data)


    def read_file_record(self, file_number, record_number, record_length):
        # Создание экземпляра структуры ReadFileRecordRequest
        request = ReadFileRecordRequest(self.slave_id)
        # Установка значений полей структуры
        request.file_number = file_number
        request.record_number = record_number
        request.record_length = record_length
        result = self.client.read_file_record(self.slave_id, [request])

        return result

    async def write_file(self, item):
        if item is not None:
            # 120 записів (не байт)
            max_record_size = 120
            # 10000 записів (не байт)
            max_file_size = 10000
            _file_shift = 0
            param_attributes = item.get_param_attributes()

            file_num = param_attributes.get('file_num', '')
            start_record_num = param_attributes.get('start_record_num', '')
            left_to_write = param_attributes.get('file_size', '')
            record_data = item.data_for_network()
            if left_to_write is None:
                left_to_write = len(record_data)//2 + len(record_data) % 2

            total_size = left_to_write
            last_record_number = left_to_write

            while left_to_write > 0:
                write_size = max_record_size if left_to_write > max_record_size else left_to_write
                result = None
                request = WriteFileRecordRequest(self.slave_id)
                if start_record_num >= max_file_size:
                    _file_shift += 1
                    start_record_num = 0

                if (write_size + start_record_num) > max_file_size:
                    write_size = max_file_size - start_record_num

                request.file_number = file_num + _file_shift
                request.record_number = start_record_num
                request.record_length = write_size
                request.record_data = record_data[((_file_shift*max_file_size) + start_record_num)*2:
                                                  (((_file_shift*max_file_size) + start_record_num)*2) + write_size*2]

                try:
                    result = await self.client.write_file_record(self.slave_id, [request])
                    start_record_num += write_size
                    left_to_write -= write_size

                    # Отправляем сигнал с обновлением прогресса
                    progress = int(((total_size - left_to_write) / total_size) * 100)
                    self.progress_updated.emit(progress, 'write_file')

                except Exception as e:
                    print(f"Error occurred: {str(e)}")
                    item.confirm_writing(False, 'modbus_error')
                    return 'error'

                #TEST FW BREAK RESPONCE
                if isinstance(result, ModbusIOException):
                    # return 'modbus_error'
                    item.confirm_writing(False, 'modbus_error')
                elif isinstance(result, ExceptionResponse):
                    self.status = 'connect_err'
                    item.confirm_writing(False, 'modbus_error')
                    return
#                else:
#                    item.confirm_writing(True)

            # WARNING TODO:!!!!  !!!!!!!!
            # Тимчасова вставка для перевірки роботи файлу ребут,
            # незрозумілий пустий файл потрібно передати у кінці
            #
            # Update: Порожній файл передається в кінці запису будь якого файлу!
            request.record_number = start_record_num #last_record_number #param_attributes.get('file_size', '')
            request.record_length = 0
            request.record_data = b'' #b'\x00\x00'
            try:
                result = await self.client.write_file_record(self.slave_id, [request])

            except Exception as e:
                print(f"Error occurred: {str(e)}")
                item.confirm_writing(False, 'modbus_error')
                return
            # WARNING TODO:!!!!  !!!!!!!!

            if isinstance(result, ModbusIOException):
                item.confirm_writing(False, 'modbus_error')
            else:
                item.confirm_writing(True)


    def write_file_record(self, file_number, record_number, record_length, record_data):
        # Создание экземпляра структуры WriteFileRecordRequest
        request = WriteFileRecordRequest(self.slave_id)
        # Установка значений полей структуры
        request.file_number = file_number
        request.record_number = record_number
        request.record_length = record_length
        request.record_data = record_data
        result = self.client.write_file_record(self.slave_id, [request])

        return result


class AqOfflineConnect(AqConnect):
    def __init__(self, core_cv):
        super().__init__(core_cv)
        # self.core_cv = core_cv
        self.param_request_stack = []
        self.file_request_stack = []

    def address_string(self):
        return 'Offline'

    async def open(self):
        # return self.client.connect()
        return True

    def close(self):
        # self.client.close()
        return True

    def createFileRequest(self, func, file_num, record_num, record_len, data):
        self.file_request_stack.append({'func': func, 'file_num': file_num,
                                        'record_num': record_num, 'record_len': record_len, 'data': data})
        with self.core_cv:
            self.core_cv.notify()

    async def read_param(self, item):
        if item is not None:
            if item.value_in_device is None:
                item.set_default_value()

            item.value = item.value_in_device
            item.synchronized = True

    async def write_param(self, item):
        if item is not None:
            item.confirm_writing(True)

    def read_file_record(self, file_number, record_number, record_length):
        # Создание экземпляра структуры ReadFileRecordRequest
        request = ReadFileRecordRequest(self.slave_id)
        # Установка значений полей структуры
        request.file_number = file_number
        request.record_number = record_number
        request.record_length = record_length
        result = self.client.read_file_record(self.slave_id, [request])

        return result

    def set_ready_flag(self):
        if len(self.RequestGroupQueue) > 0:
            self.notify(self)
