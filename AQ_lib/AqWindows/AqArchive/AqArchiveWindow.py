import csv
import datetime
import os
import struct
from functools import partial

from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import QFileDialog

from AQ_EventManager import AQ_EventManager
from AqCustomNamesByUID import *
from AqMessageManager import AqMessageManager
from AqModbusTips import swap_bytes_at_registers
from AqReadArchiveTread import ReadArchiveTread
from AqSettingsFunc import AqSettingsManager
from AqTranslateManager import AqTranslateManager
from AqWatchListCore import AqWatchListCore
from AqWindowTemplate import AqDialogTemplate


class AqArchiveWidget(AqDialogTemplate):
    message_signal = Signal(str, str)
    srv_progress_signal = Signal(int, str)

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.minimizeBtnEnable = False
        self.maximizeBtnEnable = False
        self.progress_bar_is_active = False
        AqWatchListCore.set_pause_flag(True)

        self.name = AqTranslateManager.tr('Log')
        self.event_manager = AQ_EventManager.get_global_event_manager()
        # self.event_manager.register_event_handler('DeviceLog', self.close_btn_block)

        self._message_manager = AqMessageManager.get_global_message_manager()

        self.message_signal.connect(partial(self._message_manager.show_message, self))
        self._message_manager.subscribe('LogDevice', self.message_signal.emit)

        self.ui.logSetSettingsBtn.clicked.connect(self.write_logging_settings)
        self.ui.saveLogBtn.clicked.connect(self.read_archive)

        self.device = None
        self.log_settings = None

        self._params_dict_from_tree = {}
        self._ui_edit_lines_dict = {}
        self._settings_values = {}
        self.ui.progressTextLabel.hide()
        self.ui.progressBar.hide()
        self._part_count = 1
        self._saved_service_value = 0

        self.srv_progress_signal.connect(self.progress_update)

    def set_logging_device(self, device):
        # self.event_manager.emit_event('set_logging_device', device)
        self.device = device
        self.log_settings = self.device.get_log_settings()
        if self.log_settings is not None:
            self.ui.logIntervalLineEdit.setText(str(self.log_settings['log_interval']))
            self._ui_edit_lines_dict['log_interval'] = self.ui.logIntervalLineEdit
            self.ui.logNumberFilesLineEdit.setText(str(self.log_settings['log_num_files']))
            self._ui_edit_lines_dict['log_num_files'] = self.ui.logNumberFilesLineEdit
            self.ui.logFileSizeLineEdit.setText(str(self.log_settings['log_file_size']))
            self._ui_edit_lines_dict['log_file_size'] = self.ui.logFileSizeLineEdit

        self.ui.devNameLabel.setText(self.device.name)
        self.ui.devSnLabel.setText('S/N' + self.device.info('serial_num'))

        for key in self.log_settings.keys():
            item = self.device.system_params_dict[key]
            param_attributes = item.data(Qt.UserRole)
            self._params_dict_from_tree[key] = self.device.get_item_by_modbus_reg(param_attributes['modbus_reg'])
            param_attributes = self._params_dict_from_tree[key].data(Qt.UserRole)
            self._ui_edit_lines_dict[key].min_limit = param_attributes['min_limit']
            self._ui_edit_lines_dict[key].max_limit = param_attributes['max_limit']

        self.device.connect_progress.connect(self.progress_update)

    def write_logging_settings(self):
        try:
            interval = int(self.ui.logIntervalLineEdit.text())
            num_files = int(self.ui.logNumberFilesLineEdit.text())
            file_size = int(self.ui.logFileSizeLineEdit.text())
        except:
            self._message_manager.send_message('LogDevice', "Error", AqTranslateManager.tr('Values must be an UINT'))
            return None

        if isinstance(interval, int) and isinstance(num_files, int) and isinstance(file_size, int):
            settings_dict = {'log_interval': interval, 'log_num_files': num_files, 'log_file_size': file_size}
        else:
            self._message_manager.send_message('LogDevice', "Error", AqTranslateManager.tr('Values must be an UINT'))
            return None

        items_to_write = list()
        for key in settings_dict.keys():
            if settings_dict[key] < self._ui_edit_lines_dict[key].min_limit or \
                    settings_dict[key] > self._ui_edit_lines_dict[key].max_limit:
                self._message_manager.send_message('LogDevice', "Error",
                                                   AqTranslateManager.tr('Value') + ' ' +
                                                   key[4:] + ' ' +
                                                   AqTranslateManager.tr('less or more than permissible'))
                return None

            item = self._params_dict_from_tree[key]
            item.value = settings_dict[key]
            item.param_status = 'changed'
            items_to_write.append(item)

        self.device.write_parameters(items_to_write, message_feedback_address='LogDevice')

    def read_archive(self):
        self.ui.saveLogBtn.setEnabled(False)
        self.progress_bar_is_active = True
        self.ui.progressTextLabel.setText('')
        self.ui.progressTextLabel.show()
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        self._part_count = 1
        self._saved_service_value = 0
        self.read_archive_thread = ReadArchiveTread(self.device.read_archive)
        self.read_archive_thread.error.connect(self.read_archive_error)
        self.read_archive_thread.result_signal.connect(self.save_archive_as_file)
        self.read_archive_thread.start()

    def read_archive_error(self):
        self.ui.saveLogBtn.setEnabled(True)
        self.ui.progressTextLabel.hide()
        self.ui.progressBar.hide()
        self._message_manager.send_message('LogDevice', "Error", AqTranslateManager.tr('Read has been failed'))
        return None

    def save_archive_as_file(self, result):
        archive_csv_data = self.create_archive_csv_data(result)

        now = datetime.datetime.now()
        formatted_time = now.strftime("_%d-%m-%y_%H-%M-%S")

        # Сохраняем данные в файл CSV
        self.device_str = ''.join((self.device.info('name'), '_', self.device.info('serial_num')))
        def_name = 'Log_' + self.device_str + formatted_time + '.csv'
        # Начальный путь для диалога
        initial_path = AqSettingsManager.get_last_path('archive_csv_path')
        if initial_path == '':
            initial_path = "C:/"
        self.file_dialog = QFileDialog(self)
        options = self.file_dialog.options()

        path = initial_path + '/' + def_name

        # Открываем диалог для выбора файла и места сохранения
        filename, _ = self.file_dialog.getSaveFileName(self, "Save device log as CSV", path, "CSV Files (*.csv);;All Files (*)", options=options)
        if filename != '':
            try:
                with open(filename, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile, delimiter=";")  # ← выбери нужный разделитель
                    writer.writerows(archive_csv_data)

            except Exception as e:
                self._message_manager.send_message('LogDevice', 'Error', AqTranslateManager.tr('File access denied. The file may be occupied by another application.'))

            # Извлекаем путь к каталогу
            directory_path = os.path.dirname(filename)
            AqSettingsManager.save_last_path('archive_csv_path', directory_path)

        self.ui.progressTextLabel.hide()
        self.ui.progressBar.hide()
        self.ui.saveLogBtn.setEnabled(True)

    def progress_update(self, value, servise_msg):
        if servise_msg == 'read_file' and self.progress_bar_is_active:
            self._part_count += 1

            self.ui.progressTextLabel.setText(AqTranslateManager.tr('Reading part_') +
                                             str(self._part_count))

        elif servise_msg == 'parse_file' and self.progress_bar_is_active:
            self.ui.progressTextLabel.setText(AqTranslateManager.tr('Parsing file'))
            self.ui.progressBar.setValue(value)

        elif servise_msg == 'create_table' and self.progress_bar_is_active:
            self.ui.progressTextLabel.setText(AqTranslateManager.tr('Create CSV table'))
            self.ui.progressBar.setValue(value)

    def create_archive_csv_data(self, raw_data):
        lines_list = list()

        progress_len = len(raw_data)
        progress_count = 0
        progress_percent = 0

        for line in raw_data:
            try:
                name, time, time_point_str, value, state = self.prepare_line_data(line)
            except Exception as e:
                raise e

            lines_list.append(dict({'time_point': time,
                                    'time_point_str': time_point_str,
                                    'name': name,
                                    'value': value,
                                    'state': state}))

            progress_count += 1
            progress_percent = int((progress_count/progress_len)*100)
            self.srv_progress_signal.emit(progress_percent, 'parse_file')

        timestamps = [item["time_point_str"] for item in lines_list if "time_point_str" in item]

        unique_sorted_time = sorted(set(timestamps))

        unique_sorted_names = list()

        for line in lines_list:
            if line['name'] not in unique_sorted_names:
                unique_sorted_names.append(line['name'])

        csv_data = list()
        first_line = list()
        first_line.append('Data/Time')

        for name in unique_sorted_names:
            first_line.append(str(name) + '.Value')
            first_line.append(str(name) + '.Quality')

        csv_data.append(first_line)

        temp_line_vs = list()

        progress_len = len(unique_sorted_time)
        progress_count = 0
        progress_percent = 0

        for time in unique_sorted_time:
            for name in unique_sorted_names:
                new_name_cycle_flag = True
                for item in lines_list:
                    if item.get("time_point_str") == time and item.get("name") == name:
                        temp_line_vs.append(item['value'])
                        temp_line_vs.append(item['state'])
                        new_name_cycle_flag = False

                if new_name_cycle_flag:
                    temp_line_vs.append(' ')
                    temp_line_vs.append(' ')

            csv_data.append([time] + temp_line_vs)
            temp_line_vs.clear()

            progress_count += 1
            progress_percent = int((progress_count / progress_len) * 100)
            self.srv_progress_signal.emit(progress_percent, 'create_table')

        return csv_data

    def prepare_line_data(self, line):
        if line[0] == 'Invalid record':
            name = 'Invalid record'
            time = 'Invalid record'
            time_point_str = 'Invalid record'
            value = 'Invalid record'
            state = 'Invalid record'
            return name, time, time_point_str, value, state

        #*****************************************

        time = line[0]

        time += datetime.datetime(2000, 1, 1).timestamp()
        datetime_obj = datetime.datetime.fromtimestamp(time)
        value = datetime_obj.strftime('%d.%m.%Y %H:%M:%S')
        time_point_str = str(value)

        #*****************************************

        uid = line[1]
        name = uid
        item = self.device.get_item_by_UID(int(uid, 16))
        try:
            # item = self.device.get_item_by_UID(int(uid, 16))
            if item is not None:
                parameter_attributes = item.data(Qt.UserRole)
                name = parameter_attributes.get('cat_prefix_name', uid)
            else:
                hidden_names_dict = HIDDEN_PARAMS_NAMES_BY_UID_EN
                if AqTranslateManager.get_current_lang() == 'UA':
                    hidden_names_dict = HIDDEN_PARAMS_NAMES_BY_UID_UA

                name = hidden_names_dict.get(int(uid, 16), uid)
        except:
            name = uid

        # *****************************************

        if item is not None:
            parameter_attributes = item.data(Qt.UserRole)
            type = parameter_attributes.get('type')

            if type == 'unsigned' or\
                type == 'signed':
                value = int(line[2], 16)
            elif type == 'float' or \
                type == 'fix_point_float':
                raw = bytes.fromhex(line[2].decode())
                value = struct.unpack('<f', raw)[0]
            elif type == 'enum':
                try:
                    enum_str = parameter_attributes.get('enum_strings', None)
                    if enum_str is not None:
                        value = enum_str[int(line[2], 16)]
                except:
                    value = line[2]
        else:
            value = line[2]

        # else:
        # 'float',
        # 1: 'fix_point_float',
        # 2: 'unsigned',
        # 3: 'signed',
        # 4: 'enum',
        # 5: 'date_time',
        # 6: 'date',
        # 7: 'time',
        # 8: 'string',
        # 9: 'stream'

        # value = line[2]
        # type = parameter_attributes['type']

        # *****************************************
        if line[3]:
            state = 'GOOD'
        else:
            state = 'BAD'

        return name, time, time_point_str, value, state

    def close(self):
        # self.event_manager.unregister_event_handler('DeviceLog', self.close_btn_block)
        AqWatchListCore.set_pause_flag(False)
        super().close()
