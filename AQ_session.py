from PyQt5.QtCore import QObject
from AQ_window_AddDevices import AQ_DialogAddDevices


class AQ_CurrentSession(QObject):
    def __init__(self, event_manager, parent):
        super().__init__()
        self.parent = parent
        self.event_manager = event_manager
        self.cur_active_device = None
        self.event_manager.register_handler("open_AddDevices", self.open_AddDevices)

    def open_AddDevices(self):
        AddDevices_window = AQ_DialogAddDevices('Add Devices', self.parent)
        AddDevices_window.exec_()

    def read_cur_active_device(self):
        return

    def write_cur_active_device(self):
        return