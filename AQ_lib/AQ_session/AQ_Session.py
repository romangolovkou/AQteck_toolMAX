from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QGuiApplication, QFont
from PySide6.QtWidgets import QWidget, QFrame, QLabel
from pymodbus.client import serial
import serial.tools.list_ports

from AQ_AddDevicesWindow import AQ_DialogAddDevices
from AQ_Connect import AQ_modbusRTU_connect
from AQ_ParamListWindow import AQ_DialogParamList
from AQ_DeviceInfoWindow import AQ_DialogDeviceInfo
from AQ_SetSlaveIdWindow import AQ_DialogSetSlaveId
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
        self.event_manager.register_event_handler("open_SetSlaveId", self.open_SetSlaveId)
        self.event_manager.register_event_handler("add_new_devices", self.add_new_devices)
        self.event_manager.register_event_handler("set_active_device", self.set_cur_active_device)
        self.event_manager.register_event_handler("read_params_cur_active_device", self.read_params_cur_active_device)
        self.event_manager.register_event_handler("write_params_cur_active_device", self.write_params_cur_active_device)
        self.event_manager.register_event_handler("delete_cur_active_device", self.delete_cur_active_device)
        self.event_manager.register_event_handler("delete_device", self.delete_device)
        self.event_manager.register_event_handler('no_devices', self.clear_cur_active_device)
        self.event_manager.register_event_handler('restart_cur_active_device', self.restart_current_active_device)
        self.event_manager.register_event_handler('add_parameter_to_watch_list', self.add_param_to_watch_list)
        self.event_manager.register_event_handler('set_slave_id', self.set_slave_id)


    def open_AddDevices(self):
        AddDevices_window = AQ_DialogAddDevices(self.event_manager, self.parent)
        AddDevices_window.exec()

    def open_ParameterList(self):
        if self.cur_active_device is not None:
            ParameterList_window = AQ_DialogParamList(self.cur_active_device, self.event_manager, self.parent)
            ParameterList_window.exec()

    def open_DeviceInfo(self):
        if self.cur_active_device is not None:
            device_info_window = AQ_DialogDeviceInfo(self.cur_active_device, self.event_manager, self.parent)
            device_info_window.exec()

    def open_WatchList(self):
        self.watch_list_window = AQ_DialogWatchList(self.event_manager, self.parent)
        self.watch_list_window.show()

    def open_SetSlaveId(self):
        self.set_slave_id_window = AQ_DialogSetSlaveId(self.event_manager, self.parent)
        self.set_slave_id_window.show()

    def add_new_devices(self, new_devices_list):
        for i in range(len(new_devices_list)):
            self.devices.append(new_devices_list[i])
            self.set_local_event_manager_in_parameters(self.devices[-1])
            self.devices[-1].read_parameters()

        self.event_manager.emit_event('new_devices_added', new_devices_list)

    def set_local_event_manager_in_parameters(self, device):
        device_data = device.get_device_data()
        device_tree = device_data.get('device_tree', None)
        if device_tree is not None:
            root = device_tree.invisibleRootItem()
            self.traverse_items_set_local_event_manager(root, device.local_event_manager)

    def traverse_items_set_local_event_manager(self, item, local_event_manager):
        for row in range(item.rowCount()):
            child_item = item.child(row)
            if child_item is not None:
                parameter_attributes = child_item.data(Qt.UserRole)
                if parameter_attributes is not None:
                    if parameter_attributes.get('is_catalog', 0) == 1:
                        self.traverse_items_set_local_event_manager(child_item, local_event_manager)
                    else:
                        child_item.set_local_event_manager(local_event_manager)

    def set_cur_active_device(self, device):
        if device is not None:
            self.cur_active_device = device

    def clear_cur_active_device(self):
        self.cur_active_device = None

    def read_params_cur_active_device(self):
        self.wait_label = AQ_wait_label_widget('Please wait...', self.parent)
        self.wait_label.show()

        if self.cur_active_device is not None:
            self.cur_active_device.read_parameters()

        self.wait_label.hide()
        self.wait_label.deleteLater()

    def write_params_cur_active_device(self):
        if self.cur_active_device is not None:
            self.cur_active_device.write_all_parameters()

    def delete_cur_active_device(self):
        if self.cur_active_device is not None:
            self.event_manager.emit_event('delete_device', self.cur_active_device)

    def delete_device(self, device):
        if device is not None:
            device.client.close()
            index_to_remove = self.devices.index(device)
            removed_element = self.devices.pop(index_to_remove)
            if len(self.devices) == 0:
                self.event_manager.emit_event('no_devices')

    def restart_device(self, device):
        device.restart_device()

    def restart_current_active_device(self):
        if self.cur_active_device is not None:
            self.restart_device(self.cur_active_device)

    def add_param_to_watch_list(self, item, model):
        if not hasattr(self, 'watch_list_window'):
            self.open_WatchList()
        elif self.watch_list_window is None:
            self.open_WatchList()

        self.event_manager.emit_event('add_item_to_watch_list', item, model)

    def set_slave_id(self, network_settings):
        network_settings = network_settings[0]

        if network_settings[2] == 'МВ110-24_1ТД.csv':
            pass
        else:
            interface = network_settings[0]
            # Получаем список доступных COM-портов
            com_ports = serial.tools.list_ports.comports()
            for port in com_ports:
                if port.description == interface:
                    selected_port = port.device
                    boudrate = network_settings[3]
                    parity = network_settings[4][:1]
                    stopbits = network_settings[5]
                    client = AQ_modbusRTU_connect(selected_port, boudrate, parity, stopbits, 0)

            start_address = 100
            register_count = 1
            write_func = 6
            new_slave_id = network_settings[1]
            # Выполняем запрос
            result = client.write_param(start_address, new_slave_id, write_func)
            if result != 'modbus_error':
                self.event_manager.emit_event('set_slave_id_connect_ok')
            else:
                self.event_manager.emit_event('set_slave_id_connect_error')


class AQ_wait_label_widget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 230, 80)
        # Получаем геометрию основного экрана
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry.width() // 2 - self.frame.width() // 2,
                         screen_geometry.height() // 2 - self.frame.height() // 2,
                         self.frame.width(), self.frame.height())
        self.frame.setStyleSheet("border: 2px solid #fe2d2d; border-radius: 5px; background-color: #1e1f22")
        self.text_label = QLabel(text, self)
        self.text_label.setFont(QFont("Segoe UI", 12))
        self.text_label.move(10, 5)
        self.text_label.setStyleSheet("border: none; color: #E0E0E0; background-color: transparent")
        self.show()
