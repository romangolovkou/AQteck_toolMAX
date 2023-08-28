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


class AQ_modbusRTU_connect(AQ_COM_connect, ModbusSerialClient):
    def __init__(self):
        super().__init__()


class AQ_modbusTCP_connect(AQ_TCP_connect, ModbusTcpClient):
    def __init__(self):
        super().__init__()