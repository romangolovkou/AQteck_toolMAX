from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject
from PySide6.QtGui import QGuiApplication, QFont
from PySide6.QtWidgets import QWidget, QFrame, QLabel
from pymodbus.client import serial, ModbusSerialClient
import serial.tools.list_ports
from pymodbus.exceptions import ModbusIOException

import AqUiWorker
from AqBaseDevice import AqBaseDevice
from AQ_SetSlaveIdWindow import AQ_DialogSetSlaveId
import pickle
import io

from AqConnectManager import AqConnectManager
from AqDeviceFabrica import DeviceCreator


class AQ_CurrentSession(QObject):
    def __init__(self, event_manager, parent):
        super().__init__()
        self.parent = parent
        self.event_manager = event_manager
        self.cur_active_device = None
        self.devices = []
        self.event_manager.register_event_handler("open_ParameterList", self.open_ParameterList)
        self.event_manager.register_event_handler("open_DeviceInfo", self.open_DeviceInfo)
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
        self.event_manager.register_event_handler('save_device_configuration', self.save_device_config)
        self.event_manager.register_event_handler('load_device_configuration', self.load_device_config)

    def open_ParameterList(self):
        if self.cur_active_device is not None:
            AqUiWorker.show_device_param_list(None)
        else:
            AqUiWorker.show_device_param_list(None)

    def open_DeviceInfo(self):
        if self.cur_active_device is not None:
            AqUiWorker.show_device_info_window(self.cur_active_device.device_info_model)
        else:
            AqUiWorker.show_device_info_window(None)

    def open_SetSlaveId(self):
        self.set_slave_id_window = AQ_DialogSetSlaveId(self.event_manager, self.parent)
        self.set_slave_id_window.show()

    def add_new_devices(self, new_devices_list):
        self.devices.extend(new_devices_list)

        self.event_manager.emit_event('new_devices_added', new_devices_list)

    def set_cur_active_device(self, device):
        if device is not None:
            self.cur_active_device = device

    def clear_cur_active_device(self):
        self.cur_active_device = None

    def read_params_cur_active_device(self):
        if self.cur_active_device is not None:
            self.cur_active_device.read_parameters()

    def write_params_cur_active_device(self):
        if self.cur_active_device is not None:
            self.cur_active_device.write_parameters()

    def delete_cur_active_device(self):
        if self.cur_active_device is not None:
            self.event_manager.emit_event('delete_device', self.cur_active_device)

    def delete_device(self, device):
        if device is not None:
            # TODO: delete device object and do deinit inside
            device._connect.close()
            index_to_remove = self.devices.index(device)
            removed_element = self.devices.pop(index_to_remove)
            if len(self.devices) == 0:
                self.event_manager.emit_event('no_devices')


    def restart_device(self, device):
        device.restart()

    def restart_current_active_device(self):
        if self.cur_active_device is not None:
            self.restart_device(self.cur_active_device)

    def add_param_to_watch_list(self, item, model):
        if not hasattr(self, 'watch_list_window'):
            self.open_WatchList()
        elif self.watch_list_window is None:
            self.open_WatchList()

        self.event_manager.emit_event('add_item_to_watch_list', item, model)

    def save_device_config(self, device: AqBaseDevice):
        fname = None

        f = io.BytesIO()
        p = pickle.Pickler(f)

        config = device.get_configuration()
        p.dump(config)

        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setLabelText(QFileDialog.DialogLabel.LookIn, "Save as...")
        dialog.setNameFilter(QCoreApplication.translate("SaveFileDialog", u"AQteck device configuration (*.adc)", None))
        if dialog.exec_():
            fname = dialog.selectedFiles()

        if fname is not None:
            if fname[0] != None:
                with open(fname[0], 'wb') as file:
                    file.write(f.getvalue())
                    file.close()

            print('I wrote some shit')

    def load_device_config(self, device: AqBaseDevice):
        loadConf = None
        fname = None

        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setNameFilter(QCoreApplication.translate("SaveFileDialog", u"AQteck device configuration (*.adc)", None))
        if dialog.exec_():
            fname = dialog.selectedFiles()

        if fname is not None:
            print('Filename ', fname)
            # File has been choosed
            if fname[0] != '':
                try:
                    with open (fname[0], 'rb') as cfgFile:
                        fileData = io.BytesIO(cfgFile.read())
                        loadConf = pickle.loads(fileData.getvalue())
                except Exception as e:
                    print(f"Error occurred: {str(e)}")
                    loadConf = None
                    self.event_manager.emit_event('parsing_cfg_error')


            if loadConf != None:
                device.set_configuration(loadConf)
                print('Loaded')
            else:
                print('Load failed')

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
                    # client = AQ_modbusRTU_connect(selected_port, boudrate, parity, stopbits, 0)
                    timeout = 1.0
                    client = ModbusSerialClient(method='rtu',
                                                 port=selected_port,
                                                 baudrate=boudrate,
                                                 parity=parity,
                                                 stopbits=stopbits,
                                                 timeout=timeout)

            if network_settings[2] == 'МВ110-24_8АС.csv' or network_settings[2] == 'МВ110-24_8А.csv':
                start_address = 30
            else:
                start_address = 100

            register_count = 1
            write_func = 6
            new_slave_id = network_settings[1]
            # Выполняем запрос
            client.connect()
            result = client.write_register(start_address, new_slave_id)
            client.close()
            if not isinstance(result, ModbusIOException):
                self.event_manager.emit_event('set_slave_id_connect_ok')
            else:
                self.event_manager.emit_event('set_slave_id_connect_error')
