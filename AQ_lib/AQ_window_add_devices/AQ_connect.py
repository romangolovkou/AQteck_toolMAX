from abc import abstractmethod

from PyQt5.QtCore import QObject
from pymodbus.client import ModbusTcpClient, ModbusSerialClient


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
