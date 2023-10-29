import threading
import time
from PySide6.QtCore import QThread, Signal, QObject
from pymodbus.client import serial
import serial.tools.list_ports

from AQ_Connect import AQ_modbusTCP_connect, AQ_modbusRTU_connect
from AQ_IsValidIpFunc import is_valid_ip


class AQ_ConnectManager(QObject):
    def __init__(self, event_manager, parent):
        super().__init__(parent)
        self.event_manager = event_manager
        self.request_stack = []

        self.event_manager.register_event_handler('create_new_connect', self.create_connect)

        self.core_cv = threading.Condition()

        self.core_thread = threading.Thread(target=self.run)
        self.core_thread.start()

    def create_connect(self, device):
        address_tuple = device.address_tuple
        interface = address_tuple[0]
        address = address_tuple[1]
        if interface == "Ethernet":
            if is_valid_ip(address):
                device.connect = AQ_modbusTCP_connect(address)
                # return client
        else:
            # Получаем список доступных COM-портов
            com_ports = serial.tools.list_ports.comports()
            for port in com_ports:
                if port.description == interface:
                    selected_port = port.device
                    boudrate = address_tuple[3]
                    parity = address_tuple[4][:1]
                    stopbits = address_tuple[5]
                    device.connect = AQ_modbusRTU_connect(self, selected_port, boudrate, parity, stopbits, address)
                    # return client

        # return None

    def run(self):
        with self.core_cv:
            while True:
                self.core_cv.wait()
                if len(self.request_stack) > 0:
                    self.wrapper_call(self.request_stack[0])
                    self.request_stack.pop(0)
        pass

    def add_request(self, request):
        self.request_stack.append(request)
        with self.core_cv:
            self.core_cv.notify()

    def wrapper_call(self, request):
        request()
