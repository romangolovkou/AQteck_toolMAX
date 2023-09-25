from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from AQ_AddDevicesWindow import AQ_DialogAddDevices
from AQ_Device import AQ_Device
from AQ_ParamListWindow import AQ_DialogParamList
from AQ_DeviceInfoWindow import AQ_DialogDeviceInfo
from AQ_WatchListWindow import AQ_DialogWatchList


class AQ_CurrentSession(QObject):
    def __init__(self, event_manager, parent):
        super().__init__()
        self.parent = parent
        self.event_manager = event_manager
        self.cur_active_device = None
        self.devices = []
        self.event_manager.register_event_handler("open_AddDevices", self.open_AddDevices)
        self.event_manager.register_event_handler("open_ParameterList", self.open_ParameterList)
        self.event_manager.register_event_handler("open_DeviceInfo", self.open_DeviceInfo)
        self.event_manager.register_event_handler("open_WatchList", self.open_WatchList)
        self.event_manager.register_event_handler("add_new_devices", self.add_new_devices)
        self.event_manager.register_event_handler("set_active_device", self.set_cur_active_device)
        self.event_manager.register_event_handler("read_params_cur_active_device", self.read_params_cur_active_device)
        self.event_manager.register_event_handler("write_params_cur_active_device", self.write_params_cur_active_device)
        self.event_manager.register_event_handler("delete_cur_active_device", self.delete_cur_active_device)
        self.event_manager.register_event_handler("delete_device", self.delete_device)
        self.event_manager.register_event_handler('no_devices', self.clear_cur_active_device)
        self.event_manager.register_event_handler('restart_cur_active_device', self.restart_current_active_device)


    def open_AddDevices(self):
        AddDevices_window = AQ_DialogAddDevices(self.event_manager, self.parent)
        AddDevices_window.exec_()

    def open_ParameterList(self):
        if self.cur_active_device is not None:
            ParameterList_window = AQ_DialogParamList(self.cur_active_device, self.event_manager, self.parent)
            ParameterList_window.exec_()

    def open_DeviceInfo(self):
        if self.cur_active_device is not None:
            device_info_window = AQ_DialogDeviceInfo(self.cur_active_device, self.event_manager, self.parent)
            device_info_window.exec_()

    def open_WatchList(self):
        watch_list_window = AQ_DialogWatchList(self.event_manager, self.parent)
        watch_list_window.show()

    def add_new_devices(self, new_devices_list):
        for i in range(len(new_devices_list)):
            self.devices.append(new_devices_list[i])
            self.devices[-1].read_all_parameters()

        self.event_manager.emit_event('new_devices_added', new_devices_list)

    def set_cur_active_device(self, device):
        if device is not None:
            self.cur_active_device = device

    def clear_cur_active_device(self):
        self.cur_active_device = None

    def read_params_cur_active_device(self):
        if self.cur_active_device is not None:
            self.cur_active_device.read_all_parameters()

    def write_params_cur_active_device(self):
        if self.cur_active_device is not None:
            self.cur_active_device.write_all_parameters()

    def delete_cur_active_device(self):
        if self.cur_active_device is not None:
            self.event_manager.emit_event('delete_device', self.cur_active_device)

    def delete_device(self, device):
        if device is not None:
            index_to_remove = self.devices.index(device)
            removed_element = self.devices.pop(index_to_remove)
            if len(self.devices) == 0:
                self.event_manager.emit_event('no_devices')

    def restart_device(self, device):
        device.restart_device()

    def restart_current_active_device(self):
        if self.cur_active_device is not None:
            self.restart_device(self.cur_active_device)
