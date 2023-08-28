from PyQt5.QtCore import QObject
from AQ_window_AddDevices import AQ_DialogAddDevices
from AQ_Device import AQ_Device


class AQ_CurrentSession(QObject):
    def __init__(self, event_manager, parent):
        super().__init__()
        self.parent = parent
        self.event_manager = event_manager
        self.cur_active_device = None
        self.event_manager.register_event_handler("open_AddDevices", self.open_AddDevices)
        self.ready_to_add_devices_trees = []
        self.ready_to_add_devices = []
        self.devices_trees = []
        self.devices = []
        self.current_active_dev_index = 0

    def open_AddDevices(self):
        AddDevices_window = AQ_DialogAddDevices(self.event_manager, self.devices, self.parent)
        AddDevices_window.exec_()

    def read_cur_active_device(self):
        return

    def write_cur_active_device(self):
        return