import os
import threading
import zipfile
from datetime import datetime
import struct
import time

from PySide6.QtCore import Qt

from AqAutoDetectionDevice import AqAutoDetectionDevice
from AqAutoDetectionItems import AqAutoDetectStringParamItem, AqAutoDetectModbusFileItem, AqAutoDetectPasswordFileItem
from AqBaseDevice import AqBaseDevice
from AqBaseTreeItems import AqParamItem
from AqCRC32 import Crc32
from AqDeviceConfig import AqDeviceConfig
from AqConnect import AqModbusConnect
from AqDeviceInfoModel import AqDeviceInfoModel
from AqParser import build_item, build_file_item
from AqTranslateManager import AqTranslateManager
from AqTreeViewItemModel import AqTreeItemModel

from AqAutoDetectionLibrary import get_containers_count, \
    get_containers_offset, get_storage_container, parse_tree
from AqZipFunc import extract_zip_with_cyrillic


class AqAutoDetectionDeviceOffline(AqAutoDetectionDevice):

    # Add to init all what we need
    def __init__(self, event_manager, connect: AqModbusConnect, password=None, param_dict=None):
        self._param_dict = param_dict
        super().__init__(event_manager, connect, password=None)

    def init_device(self) -> bool:

        self.__create_system_params()
        self.__create_system_files()
        try:
            name, version = self._param_dict.get('device', None).split('_', 1)
        except:
            self._status = 'connect_err'
            print('AqAutoDetectionDeviceOffline ERROR: incorrect file name')
            return False

        self._info['name'] = name
        if self._connect.status == 'connect_err':
            self._status = 'connect_err'
            return False
        self._info['version'] = version
        self._info['serial_num'] = None
        self._info['password'] = None
        self._default_prg = self.read_def_prg()

        if self._default_prg == 'decrypt_err':
            self._status = 'decrypt_err'
            return True

        if self._default_prg == 'need_pass':
            self._status = 'need_pass'
            return True

        self._device_tree = self.__parse_default_prg()
        if self._device_tree == 'parsing_err' or \
                self._device_tree is None:
            self._status = 'parsing_err'
            return True

        # TODO: describe rules to chache which functions are supported
        # into AutoDetectionDevice
        # later should be json file inside device with definitions
        self._functions['read_write'] = True,
        if self.__sync_read_param(self.system_params_dict['time_zone']) is None:
            self._functions['rtc'] = False
        else:
            self._functions['rtc'] = False  #True
        self._functions['password'] = False  #True
        self._functions['gateway'] = False  #self.__check_ugm_container()
        self._functions['set_slave_id'] = True
        self._functions['calibration'] = False  #self.__check_calib_json()
        self._functions['log'] = False  #self.__check_archive_container() #now only true, заглушка
        self._functions['fw_update'] = False  #True
        self._functions['restart'] = False  #True

        self._status = 'ok'
        return True

    def read_def_prg(self):
        file_path = 'auto_detect_conf/' + self._info['name'] + '_' + self._info['version'] + '.prg'
        if not os.path.isfile(file_path):
            raise Exception('AqAutoDetectionDeviceOffline ERROR: Can`t find configuration for specified device')
        with open(file_path, 'rb') as file:
            def_prg = file.read()

        return def_prg

    def reinit_device_with_pass(self, password):
        self.set_password(password)

        if not self.init_device():
            raise Exception('AqBaseDeviceError: can`t initialize device')

        if self._device_tree is not None and isinstance(self._device_tree, AqTreeItemModel):
            self._device_tree.set_device(self)
        else:
            if self._status != 'need_pass':
                raise Exception('AqBaseDeviceError: device_tree isn`t exists')

        if self._status != 'need_pass':
            self._param_convert_tree_to_list()

        return self._status

    def __create_system_params(self):
        # Створюємо строкові системні ітеми
        keys_list = list(self._system_string.keys())
        for i in range(len(keys_list)):
            param_attributes = dict()
            param_attributes['name'] = keys_list[i]
            param_attributes['modbus_reg'] = self._system_string[keys_list[i]][0]
            param_attributes['param_size'] = 2 * self._system_string[keys_list[i]][1]
            param_attributes['read_func'] = self._system_string[keys_list[i]][2]
            param_attributes['R_Only'] = 1
            param_attributes['W_Only'] = 0
            self.system_params_dict[keys_list[i]] = AqAutoDetectStringParamItem(param_attributes)
            self.system_params_dict[keys_list[i]].set_local_event_manager(self._local_event_manager)

        keys_list = list(self._system_param.keys())
        for i in range(len(keys_list)):
            param_attributes = dict()
            param_attributes['name'] = keys_list[i]
            param_attributes['modbus_reg'] = self._system_param[keys_list[i]][0]
            param_attributes['param_size'] = 2 * self._system_param[keys_list[i]][1]
            param_attributes['read_func'] = self._system_param[keys_list[i]][2]
            param_attributes['write_func'] = self._system_param[keys_list[i]][3]
            if self._system_param[keys_list[i]][5] is True:
                param_attributes['R_Only'] = 1
            else:
                param_attributes['R_Only'] = 0
            param_attributes['W_Only'] = 0
            self.system_params_dict[keys_list[i]] = build_item(self._system_param[keys_list[i]][4], param_attributes)
            self.system_params_dict[keys_list[i]].set_local_event_manager(self._local_event_manager)

    def __create_system_files(self):
        keys_list = list(self._system_file.keys())
        for i in range(len(keys_list)):
            param_attributes = dict()
            param_attributes['name'] = keys_list[i]
            param_attributes['file_num'] = self._system_file[keys_list[i]][0]
            param_attributes['start_record_num'] = self._system_file[keys_list[i]][1]
            param_attributes['file_size'] = self._system_file[keys_list[i]][2] // 2
            if self._system_file[keys_list[i]][3] is True:
                param_attributes['R_Only'] = 1
            else:
                param_attributes['R_Only'] = 0
            param_attributes['W_Only'] = 0
            self.system_params_dict[keys_list[i]] = build_file_item(self._system_file[keys_list[i]][4],
                                                                    param_attributes, self.get_password,
                                                                    self._system_file[keys_list[i]][5])
            self.system_params_dict[keys_list[i]].set_local_event_manager(self._local_event_manager)

    def __parse_default_prg(self):
        try:
            containers_count = get_containers_count(self._default_prg)
            containers_offset = get_containers_offset(self._default_prg)
            storage_container = get_storage_container(self._default_prg, containers_offset)
            device_tree = parse_tree(storage_container)
            return device_tree
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'parsing_err'


    def __sync_read_param(self, item):
        self.read_parameters(item)
        with self._core_cv:
            self._core_cv.wait()
        return item.value

    def __sync_read_file(self, item):
        self.read_file(item)
        with self._core_cv:
            self._core_cv.wait()
        return item.value

    def __sync_write_param(self, item):
        self.write_parameters(item)
        with self._core_cv:
            self._core_cv.wait()
        return item.get_status()

    def read_file(self, item):
        if item is not None:
            self.read_parameter(item)
        if len(self._stack_to_read) > 0:
            self._connect.create_param_request('read_file', self._stack_to_read)
            self._stack_to_read.clear()

    def write_file(self, item, message_feedback_address=False):
        if item is not None:
            self.write_parameter(item)
        if len(self._stack_to_write) > 0:
            self._connect.create_param_request('write_file', self._stack_to_write, message_feedback_address)
            self._stack_to_write.clear()

    def __read_status_file(self):
        try:
            status_file = self.__sync_read_file(self.system_params_dict['status'])
            return status_file
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'decrypt_err'  # Помилка дешифрування













