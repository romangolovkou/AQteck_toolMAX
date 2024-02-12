import datetime
import struct
import time

from PySide6.QtCore import Qt

from AqAutoDetectionItems import AqAutoDetectStringParamItem, AqAutoDetectModbusFileItem
from AqBaseDevice import AqBaseDevice
from AqBaseTreeItems import AqParamItem
from AqCRC32 import Crc32
from AqDeviceConfig import AqDeviceConfig
from AqConnect import AqModbusConnect
from AqDeviceInfoModel import AqDeviceInfoModel
from AqDeviceStrings import get_translated_string
from AqParser import build_item
from AqTreeViewItemModel import AqTreeItemModel
from SystemLibrary.AqModbusTips import swap_bytes_at_registers, remove_empty_bytes, \
    reverse_registers

from SystemLibrary.AqAutoDetectionLibrary import get_containers_count, \
    get_containers_offset, get_storage_container, parse_tree


class AqAutoDetectionDevice(AqBaseDevice):

    # Format: 'param_name': {start_reg, count, func}
    _system_string = {
        'name':         [0xF000, 16, 3],
        'version':      [0xF010, 16, 3],
        'serial_num':   [0xF084, 10, 3]
    }
    _system_param = {
        'ip':           [0x001A, 2, 3, 'AqAutoDetectIpParamItem'],
        'date_time':    [0xF080, 2, 3, 'AqAutoDetectUnsignedParamItem'],
        'time_zone':    [0xF082, 1, 3, 'AqAutoDetectSignedParamItem']
    }

    # Format: 'file_name': [file_num, start_record_num, file_size (in bytes), R_Only]
    _system_file = {
        'reboot':       [0xDEAD, 0, 40, False],
        'status':       [0x0001, 0, 248, True],
        'default_prg':  [0xFFE0, 0, 248, True]  # file_size will be changed later in code
    }

    system_params_dict = dict()

    # Add to init all what we need
    def __init__(self, event_manager, connect: AqModbusConnect):
        self._password = None
        super().__init__(event_manager, connect)
        self._default_prg = None
        self._password = None
        self._connect = connect

    def init_device(self) -> bool:
        self.__create_system_params()
        self.__create_system_files()
        self._info['name'] = self.__sync_read_param(self.system_params_dict['name'])
        if self._connect.status == 'connect_err':
            self._status = 'connect_err'
            return False
        self._info['version'] = self.__sync_read_param(self.system_params_dict['version'])
        self._info['serial_num'] = self.__sync_read_param(self.system_params_dict['serial_num'])
        self._info['password'] = None
        self._default_prg = self.__read_default_prg()

        if self._default_prg == 'decrypt_err':
            self._status = 'decrypt_err'
            return False

        if self._default_prg == 'need_pass':
            self._status = 'need_pass'
            return True

        self._device_tree = self.__parse_default_prg()
        if self._device_tree == 'parsing_err' or \
                self._device_tree is None:
            self._status = 'parsing_err'
            return False

        # TODO: describe rules to chache which functions are supported
        # into AutoDetectionDevice
        # later should be json file inside device with definitions
        self._functions['read_write'] = True,
        if self.__sync_read_param(self.system_params_dict['time_zone']) is None:
            self._functions['rtc'] = False
        else:
            self._functions['rtc'] = True
        self._functions['password'] = False
        self._functions['set_slave_id'] = True
        self._functions['calibration'] = False
        self._functions['log'] = False
        self._functions['fw_update'] = False
        self._functions['restart'] = True

        self._status = 'ok'
        return True

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
            param_attributes['param_size'] = 2*self._system_string[keys_list[i]][1]
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
            param_attributes['R_Only'] = 1
            param_attributes['W_Only'] = 0
            self.system_params_dict[keys_list[i]] = build_item(self._system_param[keys_list[i]][3], param_attributes)
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
            self.system_params_dict[keys_list[i]] = AqAutoDetectModbusFileItem(param_attributes, self.get_password)
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

    def __parse_status_file(self, status_file):
        data_string = status_file.decode('ANSI')
        # Разделение строк по переводу строки
        data_rows = data_string.split('\n')
        data = []
        for row in data_rows:
            # Разделение записи на поля по символу ';'
            fields = row.split(';')
            data.append(fields)

        return data

    def __load_data_to_info_model(self, data):
        model = AqDeviceInfoModel()
        for i, row in enumerate(data):
            # Додаємо тільки строки з другої по п'яту
            if i > 0 and i < 5:
                info_str = None
                info_value = None
                for j, cell_str in enumerate(row):
                    if j < len(row) - 1:  # Убедимся, что мы не добавляем последнюю колонку
                        if i == 4 and j == 1:
                            value = int(cell_str, 16)
                            value += datetime.datetime(2000, 1, 1).timestamp()
                            datetime_obj = datetime.datetime.fromtimestamp(value)
                            date_time_str = datetime_obj.strftime('%d.%m.%Y %H:%M:%S')
                            info_value = date_time_str
                        else:
                            if j == 1:
                                info_value = cell_str
                            else:
                                info_str = cell_str

                model.add_general_info(info_str, info_value)

            # Додаємо тільки строки з другої по п'яту
            if i > 4:
                break

        for i, row in enumerate(data):
            # Додаємо тільки строки з п'ятої по передостанню
            if i > 4 and i < len(data) - 1:
                info_str = None
                info_value = None
                item_by_uid = None
                for j, cell_str in enumerate(row):
                    if j < len(row) - 1:  # Убедимся, что мы не добавляем последнюю колонку
                        if j == 0:
                            # Замінюємо UID на ім'я параметру
                            item_by_uid = self.__get_item_by_UID(int(cell_str, 16))
                            if item_by_uid is not None:
                                parameter_attributes = item_by_uid.get_param_attributes()
                                name = parameter_attributes.get('name', 'err_name')
                                info_str = name
                            else:
                                info_str = cell_str
                        else:
                            info_value = cell_str

                if item_by_uid is not None:
                    info_value = item_by_uid.value

                model.add_operating_info(info_str, info_value, item_by_uid)

        return model

    def __get_item_by_UID(self, uid):
        param_attributes = None
        if self._device_tree is not None:
            root = self._device_tree.invisibleRootItem()
            param_attributes = self.__traverse_items_find_item_by_uid(root, uid)

        return param_attributes

    def __traverse_items_find_item_by_uid(self, item, uid):
        for row in range(item.rowCount()):
            child_item = item.child(row)
            if child_item is not None:
                parameter_attributes = child_item.data(Qt.UserRole)
                if parameter_attributes is not None:
                    if parameter_attributes.get('is_catalog', 0) == 1:
                        item_by_uid = self.__traverse_items_find_item_by_uid(child_item, uid)
                        if item_by_uid is not None:
                            return item_by_uid
                    else:
                        if parameter_attributes.get('UID', 0) == uid:
                            return child_item
        # Якщо дійшли сюди, то співдпадінь немає
        return None

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

    def read_file(self, item):
        # if len(self._request_count) == 0:
            if item is not None:
                self.read_parameter(item)
            if len(self._stack_to_read) > 0:
                # self._request_count.append(len(self._stack_to_read))
                self._connect.create_param_request('read_file', self._stack_to_read)
                self._stack_to_read.clear()

    def write_file(self, item):
        # if len(self._request_count) == 0:
            if item is not None:
                self.write_parameter(item)
            if len(self._stack_to_write) > 0:
                # self._request_count.append(len(self._stack_to_read))
                self._connect.create_param_request('write_file', self._stack_to_write)
                self._stack_to_write.clear()

    # def __read_string(self, name):
    #     try:
    #         # Выполняем запрос
    #         response = self._connect.read_param(self.system_params_dict[name])
    #     except Exception as e:
    #         print(f"Error occurred: {str(e)}")
    #         self._status = 'connect_err'
    #         return None
    #
    #     result_str = self.system_params_dict[name].value
    #
    #     return result_str

    def __read_file(self, name): #Now Not Use
        record_size = 124
        left_to_read = self._system_file[name][2] // 2
        encrypt_file = bytearray()

        record_number = self._system_file[name][1]
        while left_to_read:
            read_size = record_size if left_to_read > record_size else left_to_read
            try:
                result = self._connect.read_file_record(self._system_file[name][0], record_number, read_size)
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                self._status = 'connect_err'
                return None
            record_number += read_size
            left_to_read -= read_size
            encrypt_file += result.records[0].record_data

        try:
            # Перевірка на кратність 8 байтам, потрібно для DES
            if (len(encrypt_file) % 8) > 0:
                padding = 8 - (len(encrypt_file) % 8)
                encrypt_file = encrypt_file + bytes([padding] * padding)
            decrypt_file = self.__decrypt_data(encrypt_file)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            self._status = 'decrypt_err'
            return None  # Помилка дешифрування

        return decrypt_file

    def __read_default_prg(self):
        # Read first page from file to determine file size
        first_page = self.__sync_read_file(self.system_params_dict['default_prg'])

        if int.from_bytes((first_page[:3][::-1]), byteorder='big') != 0:
            return 'need_pass'

        file_size = int.from_bytes((first_page[4:8][::-1]), byteorder='big')
        self.system_params_dict['default_prg'].set_file_size(file_size // 2)

        # Read full file
        full_file = self.__sync_read_file(self.system_params_dict['default_prg'])

        # Ця вставка робить файл default.prg у корні проекту (було необхідно для відладки)
        filename = 'default.prg'
        with open(filename, 'wb') as file:
            file.write(full_file)

        return full_file

    def __read_status_file(self):
        try:
            status_file = self.__sync_read_file(self.system_params_dict['status'])
            return status_file
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'decrypt_err'  # Помилка дешифрування

    # def __decrypt_data(self, encrypted_data):
    #     # Используется стандарт шифроdания DES CBC(Cipher Block Chain)
    #     cipher = DES.new(self.__get_hash(), DES.MODE_CBC, self.__get_key())
    #     decrypted_data = cipher.decrypt(encrypted_data)  # encrypted_data - зашифрованные данные
    #
    #     return decrypted_data
    #
    # def __encrypt_data(self, data):
    #     # Используется стандарт шифроdания DES CBC(Cipher Block Chain)
    #     cipher = DES.new(self.__get_hash(), DES.MODE_CBC, self.__get_key())
    #     encrypted_data = cipher.encrypt(data)
    #
    #     return encrypted_data
    #
    # def __get_key(self):
    #     # return self._info['password'] if self._info['password'] else b'superkey'
    #     return self.info('password') if self.info('password') else b'superkey'
    #
    # def __get_hash(self):
    #     # Ключ это свапнутая версия EMPTY_HASH из исходников котейнерной, в ПО контейнерной оригинал 0x24556FA7FC46B223
    #     return b"\x23\xB2\x46\xFC\xA7\x6F\x55\x24"  # 0x23B246FCA76F5524"

    def get_configuration(self) -> AqDeviceConfig:
        config = AqDeviceConfig()
        config.device_name = self.info('name')

        for devParam in self._params_list:
            param_attributes = devParam.get_param_attributes()
            if not (param_attributes.get('R_Only', 0) == 1 and param_attributes.get('W_Only', 0) == 0):
                config.saved_param_list.append({'UID': param_attributes.get('UID', 0),
                                                'modbus_reg': param_attributes.get('modbus_reg', 0),
                                                'value': devParam.value})

        return config

    def set_configuration(self, config: AqDeviceConfig):
        if self.info('name') != config.device_name:
            return NotImplementedError
            #TODO: need generate custom exception or generate event to display error message

        for cfgParam in config.saved_param_list:
            for devParam in self._params_list:
                param_attributes = devParam.get_param_attributes()
                modbusReg = param_attributes.get('modbus_reg', 0)
                if cfgParam['modbus_reg'] == modbusReg:
                    devParam.value = cfgParam['value']
        #TODO: optimize this algorithm

        self._event_manager.emit_event('current_device_data_updated', self)

    def get_device_param_list_model(self):
        dev_model = super().get_device_param_list_model()
        dev_model.network_info.append(get_translated_string('protocol_modbus_str'))
        dev_model.network_info.append(get_translated_string('byte_order_ms_str'))
        dev_model.network_info.append(get_translated_string('register_order_ls_str'))
        return dev_model

    def get_device_info_model(self):
        model = None
        status_file = self.__read_status_file()
        if status_file != 'decrypt_err' and status_file != 'connect_err' and \
                status_file != 'modbus_err':
            data = self.__parse_status_file(status_file)
            model = self.__load_data_to_info_model(data)

        return model

    def get_device_date_time(self):
        try:
            date_time = self.__sync_read_param(self.system_params_dict['date_time'])
            time_zone = self.__sync_read_param(self.system_params_dict['time_zone'])
            return {'date_time': date_time, 'time_zone': time_zone}
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 0

    def reboot(self):
        text = "I will restart the device now!"
        record_data = text.encode('UTF-8')
        item = self.system_params_dict.get('reboot', None)
        item.value = record_data
        self.write_file(item)

    def get_password(self):
        return self._password

    def set_password(self, password: str):
        self._password = password
