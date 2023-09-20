from abc import abstractmethod

from PyQt5.QtCore import QObject
from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.file_message import ReadFileRecordRequest, WriteFileRecordRequest


class AQ_connect(QObject):
    def __init__(self):
        super().__init__()
    @abstractmethod
    def open(self):
        pass
    @abstractmethod
    def close(self):
        pass


class AQ_COM_connect(AQ_connect):
    def __init__(self):
        super().__init__()


class AQ_TCP_connect(AQ_connect):
    def __init__(self):
        super().__init__()


class AQ_modbusRTU_connect(AQ_COM_connect):
    def __init__(self, _port, _baudrate, slave_id):
        super().__init__()
        self.slave_id = slave_id
        self.modbus_rtu_client = ModbusSerialClient(method='rtu', port=_port, baudrate=_baudrate)

    def open(self):
        self.modbus_rtu_client.connect()

    def close(self):
        self.modbus_rtu_client.close()

    def read_holding_registers(self, start_address, register_count):
        response = self.modbus_rtu_client.read_holding_registers(start_address, register_count, self.slave_id)
        return response

    def read_file_record(self, file_number, record_number, record_length):
        # Создание экземпляра структуры ReadFileRecordRequest
        request = ReadFileRecordRequest(self.slave_id)
        # Установка значений полей структуры
        request.file_number = file_number
        request.record_number = record_number
        request.record_length = record_length
        result = self.modbus_rtu_client.read_file_record(self.slave_id, [request])

        return result

    def write_registers(self, modbus_reg, registers):
        try:
            self.modbus_rtu_client.write_registers(modbus_reg, registers, self.slave_id)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            raise

    def write_file_record(self, file_number, record_number, record_length, record_data):
        # Создание экземпляра структуры ReadFileRecordRequest
        request = WriteFileRecordRequest(self.slave_id)
        # Установка значений полей структуры
        request.file_number = file_number
        request.record_number = record_number
        request.record_length = record_length
        request.record_data = record_data
        result = self.modbus_rtu_client.write_file_record(self.slave_id, [request])

        return result


class AQ_modbusTCP_connect(AQ_TCP_connect):
    def __init__(self, ip):
        super().__init__()
        self.slave_id = 1
        self.modbus_tcp_client = ModbusTcpClient(ip)

    def open(self):
        self.modbus_tcp_client.connect()

    def close(self):
        self.modbus_tcp_client.close()

    def read_holding_registers(self, start_address, register_count):
        response = self.modbus_tcp_client.read_holding_registers(start_address, register_count, self.slave_id)
        return response

    def read_file_record(self, file_number, record_number, record_length):
        # Создание экземпляра структуры ReadFileRecordRequest
        request = ReadFileRecordRequest(self.slave_id)
        # Установка значений полей структуры
        request.file_number = file_number
        request.record_number = record_number
        request.record_length = record_length
        result = self.modbus_tcp_client.read_file_record(self.slave_id, [request])

        return result

    def write_registers(self, modbus_reg, registers):
        try:
            self.modbus_tcp_client.write_registers(modbus_reg, registers, self.slave_id)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            raise

    def write_file_record(self, file_number, record_number, record_length, record_data):
        # Создание экземпляра структуры ReadFileRecordRequest
        request = WriteFileRecordRequest(self.slave_id)
        # Установка значений полей структуры
        request.file_number = file_number
        request.record_number = record_number
        request.record_length = record_length
        request.record_data = record_data
        result = self.modbus_tcp_client.write_file_record(self.slave_id, [request])

        return result