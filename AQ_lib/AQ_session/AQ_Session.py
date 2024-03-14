from PySide6.QtCore import QCoreApplication, Signal
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject
from PySide6.QtGui import QGuiApplication, QFont
from PySide6.QtWidgets import QWidget, QFrame, QLabel
from pymodbus.client import serial, ModbusSerialClient
import serial.tools.list_ports
from pymodbus.exceptions import ModbusIOException

import AqUiWorker
from AqBaseDevice import AqBaseDevice
import pickle
import io

from AqConnectManager import AqConnectManager
from AqDeviceFabrica import DeviceCreator
from AqWatchListCore import AqWatchListCore


class AQ_CurrentSession(QObject):
    cur_active_dev_changed = Signal()
    def __init__(self, event_manager, parent):
        super().__init__()
        self.parent = parent
        self.event_manager = event_manager
        self.cur_active_device = None
        self.devices = []

        self.event_manager.register_event_handler("add_new_devices", self.add_new_devices)
        self.event_manager.register_event_handler("set_active_device", self.set_cur_active_device)
        self.event_manager.register_event_handler("read_params_cur_active_device", self.read_params_cur_active_device)
        self.event_manager.register_event_handler("write_params_cur_active_device", self.write_params_cur_active_device)
        self.event_manager.register_event_handler("delete_cur_active_device", self.delete_cur_active_device)
        self.event_manager.register_event_handler("delete_device", self.delete_device)
        self.event_manager.register_event_handler('no_devices', self.clear_cur_active_device)
        self.event_manager.register_event_handler('restart_cur_active_device', self.restart_current_active_device)
        self.event_manager.register_event_handler('set_slave_id', self.set_slave_id)
        self.event_manager.register_event_handler('save_device_configuration', self.save_device_config)
        self.event_manager.register_event_handler('load_device_configuration', self.load_device_config)

    def add_new_devices(self, new_devices_list):
        self.devices.extend(new_devices_list)

        self.event_manager.emit_event('new_devices_added', new_devices_list)

    def set_cur_active_device(self, device):
        if device is not None:
            self.cur_active_device = device
            self.cur_active_dev_changed.emit()

    def clear_cur_active_device(self):
        self.cur_active_device = None

    def read_params_cur_active_device(self):
        if self.cur_active_device is not None:
            self.cur_active_device.read_parameters(message_feedback_flag=True)

    def write_params_cur_active_device(self):
        if self.cur_active_device is not None:
            self.cur_active_device.write_parameters()

    def delete_cur_active_device(self):
        if self.cur_active_device is not None:
            self.event_manager.emit_event('delete_device', self.cur_active_device)

    def delete_device(self, device):
        if device is not None:
            # TODO: delete device object and do deinit inside
            AqWatchListCore.removeItemByDevice(device)
            AqConnectManager.deleteConnect(device._connect)
            device.de_init()


            index_to_remove = self.devices.index(device)
            removed_element = self.devices.pop(index_to_remove)
            if len(self.devices) == 0:
                self.event_manager.emit_event('no_devices')

    def restart_device(self, device):
        if device is not None:
            device.reboot()

    def restart_current_active_device(self):
        if self.cur_active_device is not None:
            self.restart_device(self.cur_active_device)

    def set_default_cur_active_device(self):
        if self.cur_active_device is not None:
            self.cur_active_device.set_default_values()

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
        client = None

        if network_settings is not None:
            interface = network_settings.get('interface', None)
            # Получаем список доступных COM-портов
            com_ports = serial.tools.list_ports.comports()
            if interface is not None:
                for port in com_ports:
                    if port.description == interface:
                        selected_port = port.device
                        boudrate = network_settings.get('boudrate', None)
                        parity = network_settings.get('parity', None)[:1]
                        stopbits = network_settings.get('stopbits', None)
                        # client = AQ_modbusRTU_connect(selected_port, boudrate, parity, stopbits, 0)
                        timeout = 1.0
                        if boudrate is not None and\
                            parity is not None and\
                            stopbits is not None:
                            client = ModbusSerialClient(method='rtu',
                                                         port=selected_port,
                                                         baudrate=boudrate,
                                                         parity=parity,
                                                         stopbits=stopbits,
                                                         timeout=timeout)

                device = network_settings.get('device', None)
                if device is not None:
                    if device == 'МВ110-24_8АС.csv' or device == 'МВ110-24_8А.csv':
                        start_address = 30
                    else:
                        start_address = 100

                register_count = 1
                write_func = 6
                new_slave_id = network_settings.get('address', None)
                if new_slave_id is not None:
                    # Выполняем запрос
                    client.connect()
                    result = client.write_register(start_address, new_slave_id)
                    client.close()
                    if not isinstance(result, ModbusIOException):
                        self.event_manager.emit_event('set_slave_id_connect_ok')
                    else:
                        self.event_manager.emit_event('set_slave_id_connect_error')
                else:
                    self.event_manager.emit_event('set_slave_id_connect_error')
            else:
                self.event_manager.emit_event('set_slave_id_connect_error')
        else:
            self.event_manager.emit_event('set_slave_id_connect_error')
