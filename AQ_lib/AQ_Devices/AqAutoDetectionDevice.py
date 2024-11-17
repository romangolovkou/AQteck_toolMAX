import os
import threading
import zipfile
from datetime import datetime
import struct
import time

from PySide6.QtCore import Qt

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


class AqAutoDetectionDevice(AqBaseDevice):

    # Format: 'string_name': {start_reg, count, func}
    _system_string = {
        'name':         [0xF000, 16, 3],
        'version':      [0xF010, 16, 3],
        'serial_num':   [0xF084, 16, 3]
    }
    # Format: 'param_name': {start_reg, count, read_func, write_func, itemType, R_Only}
    _system_param = {
        'ip':               [0x001A, 2, 3, 16, 'AqAutoDetectIpParamItem', True],
        # For TIME container (RTC)
        'date_time':        [0xF080, 2, 3, 16, 'AqAutoDetectUnsignedParamItem', False],
        'time_zone':        [0xF082, 1, 3, 16, 'AqAutoDetectSignedParamItem', False],
        'new_time_trig':    [0xF07F, 1, 3, 16, 'AqAutoDetectUnsignedParamItem', False],
        'new_date_time':    [0xF07D, 2, 3, 16, 'AqAutoDetectUnsignedParamItem', False]
    }


    #Create message srtings for files if need (for show in modal message).
    #Must be dict vs keys 'ok', 'error', and other if need.
    reboot_msg_dict = {'ok': AqTranslateManager.tr('Rebooted successfully'),
                       'error': AqTranslateManager.tr('Reboot failed. Please try again')}
    password_msg_dict = {'ok': AqTranslateManager.tr('Password settings successfully updated'),
                         'error': AqTranslateManager.tr('Can`t write new password settings. Please try again')}

    # Format: 'file_name': [file_num, start_record_num, file_size (in bytes), R_Only, File Type, message_dict]
    _system_file = {
        'reboot':       [0xDEAD, 0, 40, False, 'AqAutoDetectModbusFileItem', reboot_msg_dict],
        'status':       [0x0001, 0, 248, True, 'AqAutoDetectModbusFileItem', None],
        'password':     [0x0010, 0, 248, False, 'AqAutoDetectPasswordFileItem', password_msg_dict],
        'default_prg':  [0xFFE0, 0, 248, True, 'AqAutoDetectModbusFileItem', None],  # file_size will be changed later in code
        'arch_header':  [0x4000, 0, 248, True, 'AqAutoDetectModbusFileItem', None],
        'archive':      [0x1000, 0, 248, True, 'AqAutoDetectModbusFileItem', None],
        'calib':        [0xFFA0, 0, 248, True, 'AqAutoDetectModbusFileItem', None]
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
            self._functions['rtc'] = True
        self._functions['password'] = True
        self._functions['gateway'] = self.__check_ugm_container()
        self._functions['set_slave_id'] = True
        self._functions['calibration'] = self.__check_calib_json()
        self._functions['log'] = False  # self.__check_archive_container() #now only true, заглушка
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
                            value += datetime(2000, 1, 1).timestamp()
                            datetime_obj = datetime.fromtimestamp(value)
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
                            try:
                                item_by_uid = self.__get_item_by_UID(int(cell_str, 16))
                            except Exception as e:
                                continue

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

    def __check_ugm_container(self):
        regs = [1540] #rs485_MODE
        for i in range(31):
            regs.append(1024 + i*16) #R1-R31 (rules for gateway)

        for reg in regs:
            item = self.__get_item_by_modbus_reg(reg)
            if not isinstance(item, AqParamItem):
                return False

        return True

    def __check_archive_container(self):
        # regs = [1540] #rs485_MODE
        # for i in range(31):
        #     regs.append(1024 + i*16) #R1-R31 (rules for gateway)
        #
        # for reg in regs:
        #     item = self.__get_item_by_modbus_reg(reg)
        #     if not isinstance(item, AqParamItem):
        #         return False

        return True

    def __check_calib_json(self):
        try:
            calib_file_first_page = self.__sync_read_file(self.system_params_dict['calib'])
            if calib_file_first_page is None:
                return False
            else:
                return True
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return False

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

    def get_item_by_modbus_reg(self, modbus_reg):
        for item in self._params_list:
            parameter_attributes = item.data(Qt.UserRole)
            if parameter_attributes.get('modbus_reg', 0) == modbus_reg:
                return item

    def __get_item_by_modbus_reg(self, modbus_reg):
        param_attributes = None
        if self._device_tree is not None:
            root = self._device_tree.invisibleRootItem()
            param_attributes = self.__traverse_items_find_item_by_modbus_reg(root, modbus_reg)

        return param_attributes

    def __traverse_items_find_item_by_modbus_reg(self, item, modbus_reg):
        for row in range(item.rowCount()):
            child_item = item.child(row)
            if child_item is not None:
                parameter_attributes = child_item.data(Qt.UserRole)
                if parameter_attributes is not None:
                    if parameter_attributes.get('is_catalog', 0) == 1:
                        item_by_uid = self.__traverse_items_find_item_by_modbus_reg(child_item, modbus_reg)
                        if item_by_uid is not None:
                            return item_by_uid
                    else:
                        if parameter_attributes.get('modbus_reg', 0) == modbus_reg:
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

    def update_param_callback(self, message_feedback_address=False, method=None):
        self._event_manager.emit_event('current_device_data_updated', self, self._update_param_stack)
        if message_feedback_address:
            if len(self._update_param_stack) > 0:
                msg_status = 'ok'
                for param in self._update_param_stack:
                    if param.get_status() != 'ok':
                        msg_status = 'error'
                        break

                modal_type = "Success" if msg_status == 'ok' else "Error"

                if method == 'read_param':
                    if msg_status == 'ok':
                        self._message_manager.send_message(message_feedback_address, modal_type,
                                                           f'{self.name}. ' + AqTranslateManager.tr('Read successful'))
                    else:
                        self._message_manager.send_message(message_feedback_address, modal_type,
                                                                f'{self.name}. ' + AqTranslateManager.tr('Read failed. One or more params failed'))
                elif method == 'write_param':
                    if msg_status == 'ok':
                        self._message_manager.send_message(message_feedback_address, modal_type,
                                                                f'{self.name}. ' + AqTranslateManager.tr('Write successful'))
                    else:
                        self._message_manager.send_message(message_feedback_address, modal_type,
                                                                f'{self.name}. ' + AqTranslateManager.tr('Write failed. One or more params failed'))
                elif method == 'read_file' or method == 'write_file':
                    file_item = self._update_param_stack[0]
                    self._message_manager.send_message(message_feedback_address, modal_type, f'{self.name}. {AqTranslateManager.tr(file_item.get_msg_string())}')
                    #TODO: Тимчасовий костиль видалення хендлеру оновлення паролю у випадку успішної зміни.
                    self._event_manager.unregister_event_handler('current_device_data_updated',
                                                                 self.update_new_password_callback)
                else:
                    self._message_manager.send_message(message_feedback_address, "Warning", AqTranslateManager.tr('Unknown operation'))

        with self._core_cv:
            self._core_cv.notify()
        self._update_param_stack.clear()

    def __read_default_prg(self):
        # Read first page from file to determine file size
        first_page = self.__sync_read_file(self.system_params_dict['default_prg'])

        if int.from_bytes((first_page[:3][::-1]), byteorder='big') != 0:
            return 'need_pass'

        file_size = int.from_bytes((first_page[4:8][::-1]), byteorder='big')
        self.system_params_dict['default_prg'].set_file_size(file_size // 2)

        # Read full file
        full_file = self.__sync_read_file(self.system_params_dict['default_prg'])

        # TODO: тимчасове збереження файлу (потрібно для відладки)
        # Ця вставка робить файл default.prg у корні проекту (було необхідно для відладки)
        roaming_folder = os.path.join(os.getenv('APPDATA'), 'AQteck tool MAX', 'Roaming')
        # Проверяем наличие папки Roaming, если её нет - создаем
        if not os.path.exists(roaming_folder):
            os.makedirs(roaming_folder)

        filename = self._info['name'] + '_' + self._info['version'] + '_' + 'default.prg'

        for file in os.listdir(roaming_folder):
            if 'enc_default' in file:
                old_path = os.path.join(roaming_folder, file)
                new_path = os.path.join(roaming_folder, file.replace('enc_default', self._info['name'] + '_' + self._info['version'] + '_' + 'enc_default.prg'))
                try:
                    os.rename(old_path, new_path)
                    print(f'Файл {old_path} переименован в {new_path}')
                except OSError as e:
                    print(f'Ошибка переименования файла {old_path}: {e}')
        # Полный путь к файлу в папке Roaming
        full_filepath = os.path.join(roaming_folder, filename)
        with open(full_filepath, 'wb') as file:
            file.write(full_file)

        return full_file

    def __read_status_file(self):
        try:
            status_file = self.__sync_read_file(self.system_params_dict['status'])
            return status_file
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'decrypt_err'  # Помилка дешифрування

    def read_calib_file(self):
        try:
            file_size = 64000
            self.system_params_dict['calib'].set_file_size(file_size // 2)
            calib_file = self.__sync_read_file(self.system_params_dict['calib'])

            temp_folder_path = 'temp'
            if not os.path.exists(temp_folder_path):
                os.makedirs(temp_folder_path)

            filename = self._info['name'] + '_' + self._info['version'] + '_' + 'FFA0'
            FORMAT = '.zip'
            full_filepath = os.path.join(temp_folder_path, filename + FORMAT)
            with open(full_filepath, 'wb') as file:
                file.write(calib_file)

            # Открытие ZIP-файла
            # with zipfile.ZipFile(full_filepath, 'r') as zip_ref:
            #     # Разархивирование всех файлов в указанную директорию
            #     zip_ref.extractall(temp_folder_path + '/' + filename)
            extract_zip_with_cyrillic(full_filepath, temp_folder_path + '/calib')

            return calib_file
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'decrypt_err'  # Помилка дешифрування

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
            self._message_manager.send_message('main', 'Error', AqTranslateManager.tr('Configuration file from another device'))
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
        dev_model.network_info.append(AqTranslateManager.tr('Protocol: Modbus'))
        dev_model.network_info.append(AqTranslateManager.tr('Byte order: Most significant byte first'))
        dev_model.network_info.append(AqTranslateManager.tr('Register order: Least significant byte first'))
        return dev_model

    def get_device_info_model(self):
        model = None
        status_file = self.__read_status_file()
        if status_file != 'decrypt_err' and status_file != 'connect_err' and \
                status_file != 'modbus_err' and status_file is not None:
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

    def write_device_date_time(self, date_time_dict: dict):
        date_time = date_time_dict['date_time']
        time_zone = date_time_dict['time_zone']

        # for i in range(3):
        #   Скидаємо у приладі триггер встановлення нового часу та дати
        # Спочатку ставимо 1, а потім 0, щоб відпрацював механізм встановлення
        # статусу параметру 'changed'.
        self.system_params_dict['new_time_trig'].value = 1
        self.system_params_dict['new_time_trig'].value = 0
        result = self.__sync_write_param(self.system_params_dict['new_time_trig'])
        if result != 'ok':
            return result

        #   Встановлюємо та записуємо нову дату та час у спеціальний схований параметр
        # Спочатку ставимо all_seconds + 1, а потім all_seconds, щоб відпрацював механізм встановлення
        # статусу параметру 'changed'.
        # Начальный момент времени (2000-01-01 00:00:00)
        min_limit_date = datetime(2000, 1, 1)
        result_date_time = date_time - min_limit_date
        all_seconds = result_date_time.total_seconds()
        if int(all_seconds) == 0:
            self.system_params_dict['new_date_time'].value = 1
        else:
            self.system_params_dict['new_date_time'].value = 0

        self.system_params_dict['new_date_time'].value = int(all_seconds)
        result = self.__sync_write_param(self.system_params_dict['new_date_time'])
        if result != 'ok':
            return result

        #   Встановлюємо та записуємо у прилад зміщення UTC
        min_shift = time_zone.utcoffset(None).total_seconds() / 60
        if int(min_shift) == 0:
            self.system_params_dict['time_zone'].value = 1
        else:
            self.system_params_dict['time_zone'].value = 0

        self.system_params_dict['time_zone'].value = int(min_shift)
        # Примусово ставимо статус 'changed'
        self.system_params_dict['time_zone'].param_status = 'changed'
        result = self.__sync_write_param(self.system_params_dict['time_zone'])
        if result != 'ok':
            return result

        self.system_params_dict['new_time_trig'].value = 1
        result = self.__sync_write_param(self.system_params_dict['new_time_trig'])
        if result != 'ok':
            return result

        # # Перевірка записанного
        # time.sleep(0.3)
        # r_date_time = self.__sync_read_param(self.system_params_dict['date_time'])
        # r_time_zone = self.__sync_read_param(self.system_params_dict['time_zone'])
        # if (r_date_time - int(all_seconds)) < 5 and r_time_zone == int(min_shift):
        #     return 'ok'
        # else:
        #     return 'error'

        return 'ok'

    def reboot(self):
        text = "I will restart the device now!"
        record_data = text.encode('UTF-8')
        item = self.system_params_dict.get('reboot', None)
        item.value = record_data
        self.write_file(item, message_feedback_address='main')

    def read_archive(self):
        self.read_archive_thread = threading.Thread(target=self.read_archive_thread)
        self.read_archive_thread.daemon = True
        self.read_archive_thread.start()

    def read_archive_thread(self):
        try:
            archive_header_bytes = self.__sync_read_file(self.system_params_dict['arch_header'])
            archive_header = archive_header_bytes.decode('ANSI')
            # archive_header = archive_header_bytes.decode('UTF-8')
            archive_header = archive_header_bytes.decode('cp1251')
            archive_bytes = self.__sync_read_file(self.system_params_dict['archive'])
            archive = archive_bytes.decode('ANSI')
            archive = archive_bytes.decode('cp1251')
            return archive_header
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 'decrypt_err'  # Помилка дешифрування

        # if status_file != 'decrypt_err' and status_file != 'connect_err' and \
        #         status_file != 'modbus_err' and status_file is not None:
        #     data = self.__parse_status_file(status_file)
        #     model = self.__load_data_to_info_model(data)
        #
        # return model

    def get_password(self):
        return self._password

    def set_password(self, password: str):
        self._password = str(password) if str(password) != '' else None

    def write_password(self, new_password):
        record_data = new_password.encode('1251')
        item = self.system_params_dict.get('password', None)
        item.value = record_data
        file_size = None
        item.set_file_size(file_size)

        self._event_manager.register_event_handler('current_device_data_updated',
                                                   self.update_new_password_callback)

        self.write_file(item, message_feedback_address='main')

    def update_new_password_callback(self, device, item_stack):
        if device == self:
            if len(item_stack) == 1:
                if isinstance(item_stack[0], AqAutoDetectPasswordFileItem):
                    pass_file_item = item_stack[0]
                    if pass_file_item.get_status() == 'ok':
                        new_password = item_stack[0].value.decode('cp1251')
                        self.set_password(new_password)
