from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from AQ_window_AddDevices import AQ_DialogAddDevices
from AQ_Device import AQ_Device


class AQ_CurrentSession(QObject):
    def __init__(self, event_manager, parent):
        super().__init__()
        self.parent = parent
        self.event_manager = event_manager
        self.cur_active_device = None
        self.event_manager.register_event_handler("open_AddDevices", self.open_AddDevices)
        self.event_manager.register_event_handler("add_new_devices", self.add_new_devices)
        self.event_manager.register_event_handler("set_active_device", self.set_cur_active_device)
        self.event_manager.register_event_handler("read_params_cur_active_device", self.read_params_cur_active_device)
        self.devices = []

    def open_AddDevices(self):
        AddDevices_window = AQ_DialogAddDevices(self.event_manager, self.parent)
        AddDevices_window.exec_()

    def add_new_devices(self, new_devices_list):
        for i in range(len(new_devices_list)):
            self.devices.append(new_devices_list[i])

    def set_cur_active_device(self, device):
        self.cur_active_device = device

    def read_params_cur_active_device(self):
        self.cur_active_device.read_all_parameters()

