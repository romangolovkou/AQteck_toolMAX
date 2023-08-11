import sys
import random
import time
import datetime
import array
import os
import struct
import threading
import socket
import re
import binascii
from functools import partial
from PyQt5.QtGui import QIcon, QPalette, QPixmap, QFont, QIntValidator, QRegExpValidator, QColor, QStandardItemModel, \
                        QStandardItem, QTransform, QPainter
from PyQt5.QtCore import Qt, QTimer, QRect, QSize, QEvent, QRegExp, QPropertyAnimation, QSettings, QEasingCurve, \
    QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QMenu, QAction, QHBoxLayout, \
    QVBoxLayout, QSizeGrip, QFrame, QSizePolicy, QSplashScreen, QDialog, QComboBox, QLineEdit, QTreeView, QHeaderView, \
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QTableWidget, QTableWidgetItem, QCheckBox, QStyledItemDelegate,\
    QProgressBar
from ToolPanelButtons import AddDeviceButton, VLine_separator, Btn_AddDevices, Btn_DeleteDevices, \
                            Btn_IPAdresess, Btn_Read, Btn_Write, Btn_FactorySettings, Btn_WatchList
from ToolPanelLayouts import replaceToolPanelWidget
from Resize_widgets import resizeWidthR_Qwidget, resizeWidthL_Qwidget, resizeHeigthLow_Qwidget, \
                           resizeHeigthTop_Qwidget, resizeDiag_BotRigth_Qwidget, resizeDiag_BotLeft_Qwidget, \
                           resizeDiag_TopLeft_Qwidget, resizeDiag_TopRigth_Qwidget
from custom_window_templates import main_frame_AQFrame, title_bar_frame_AQFrame, tool_panel_frame_AQFrame, \
                                    main_field_frame_AQFrame, AQDialog, AQComboBox, \
                                    AQLabel, IP_AQLineEdit, Slave_ID_AQLineEdit, AQ_wait_progress_bar_widget
from custom_exception import Connect_err
import serial.tools.list_ports
from pymodbus.client.tcp import ModbusTcpClient
from pymodbus.client.serial import ModbusSerialClient
from pymodbus.file_message import ReadFileRecordRequest
from AQ_communication_func import read_device_name, read_version, read_serial_number, read_default_prg, is_valid_ip, \
                            read_parameter
from AQ_parse_func import get_conteiners_count, get_containers_offset, get_storage_container, parse_tree, \
                            swap_modbus_registers, swap_modbus_bytes, reverse_modbus_registers
from AQ_settings_func import save_current_text_value, save_combobox_current_state, load_last_text_value, \
                             load_last_combobox_state
from AQ_tree_prapare_func import traverse_items
from AQ_window_AddDevices import AddDevices_AQDialog
PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'


class CustomTreeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        # Получаем данные из модели для текущего индекса
        delegate_attributes = index.data(Qt.UserRole)
        if delegate_attributes is not None:
            if delegate_attributes.get('type', '') == 'enum':
                combo_box = QComboBox(parent)
                combo_box.view().setStyleSheet("color: #D0D0D0;")
                combo_box.setStyleSheet("QComboBox { border: 0px solid #D0D0D0; color: #D0D0D0; }")
                enum_strings = delegate_attributes.get('enum_strings', '')
                for i in range(len(enum_strings)):
                    enum_str = enum_strings[i]
                    combo_box.addItem(enum_str)
                return combo_box
            elif delegate_attributes.get('type', '') == 'unsigned' or delegate_attributes.get('type', '') == 'signed'\
                    or delegate_attributes.get('type', '') == 'string' or \
                    delegate_attributes.get('type', '') == 'float':
                if not (delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0):
                    # Здесь создаем стандартный редактор для unsigned (например, QLineEdit)
                    editor = QLineEdit(parent)
                    # Оскільки стандартні комірки в дереві використорують системний шрифт, встановлюємо його і для
                    # кастомних віджетів редагування. "MS Shell Dlg 2" що стоїть у стандартних комірках - НЕ шрифт,
                    # а вказівка викристовувати шрифт системи. На різних компах може бути жеппа, якщо система не знайде
                    # "Segoe UI"
                    font = QFont("Segoe UI", 9)
                    editor.setFont(font)
                    editor.setStyleSheet("border: none; border-style: outset; color: #D0D0D0;")  # Устанавливаем стиль
                    return editor


    def setEditorData(self, editor, index):
        delegate_attributes = index.data(Qt.UserRole)
        if delegate_attributes is not None:
            if delegate_attributes.get('type', '') == 'enum':
                user_data = index.data(Qt.EditRole)
                if user_data is not None:
                    editor.setCurrentIndex(user_data)
            if delegate_attributes.get('type', '') == 'unsigned' or \
                    delegate_attributes.get('type', '') == 'signed' or \
                    delegate_attributes.get('type', '') == 'string' or \
                    delegate_attributes.get('type', '') == 'float':
                user_data = index.data(Qt.EditRole)
                if user_data is not None:
                    editor.setText(str(user_data))

    def setModelData(self, editor, model, index):
        delegate_attributes = index.data(Qt.UserRole)
        if delegate_attributes is not None:
            if delegate_attributes.get('type', '') == 'enum':
                model.setData(index, editor.currentIndex())


class AQ_TreeView(QTreeView):
    def __init__(self, dev_index, device_tree, address, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.dev_index = dev_index
        self.dev_address = address
        delegate = CustomTreeDelegate(self)
        self.setItemDelegateForColumn(1, delegate)
        self.setModel(device_tree)
        self.setGeometry(250, 2, parent.width() - 252,
                                   parent.height() - 4)
        # Получение количества колонок в модели
        column_count = device_tree.columnCount()
        for column in range(column_count):
            self.setColumnWidth(column, 200)
        self.setStyleSheet("""
                            QTreeView {
                                border: 1px solid #9ef1d3;
                                color: #D0D0D0;
                            }

                            QTreeView::item {
                                border: 1px solid #2b2d30;
                            }

                            QHeaderView::section {
                                border: 1px solid #1e1f22;
                                color: #D0D0D0;
                                background-color: #2b2d30;
                                padding-left: 6px;
                            }
                            QTreeView QScrollBar { 
                                background-color: #F0F0F0; 
                                width: 10px; }
                        """)

    def traverse_items_show_delegate(self, item):
        for row in range(item.rowCount()):
            child_item = item.child(row)
            parameter_attributes = child_item.data(Qt.UserRole)
            if parameter_attributes is not None:
                if parameter_attributes.get('type', '') == 'enum':
                    if parameter_attributes.get('W_Only', 0) == 1:
                        # Получаем индекс элемента и открываем для него постоянный редактор
                        index = self.model().index(row, 1, item.index())
                        if index.isValid():
                            self.openPersistentEditor(index)
                    else:
                        index = self.model().index(row, 1, item.index())
                        if index.isValid():
                            item_cur_value = self.model().itemFromIndex(index)
                            item_cur_value.setFlags(item_cur_value.flags() & ~Qt.ItemIsEditable)
                            self.setValue(1, index)
                elif parameter_attributes.get('type', '') == 'unsigned' or \
                        parameter_attributes.get('type', '') == 'signed' or \
                        parameter_attributes.get('type', '') == 'string' or \
                        parameter_attributes.get('type', '') == 'float':
                    index = self.model().index(row, 1, item.index())
                    if not (parameter_attributes.get('R_Only', 0) == 1 and parameter_attributes.get('W_Only', 0) == 0):
                        if index.isValid():
                            self.openPersistentEditor(index)
                    else:
                        if index.isValid():
                            item_cur_value = self.model().itemFromIndex(index)
                            item_cur_value.setFlags(item_cur_value.flags() & ~Qt.ItemIsEditable)
                            item_cur_value.setForeground(QColor("#909090"))
            if child_item is not None:
                self.traverse_items_show_delegate(child_item)

    def traverse_items_R_Only_catalog_check(self, item):
        write_flag = 0
        for row in range(item.rowCount()):
            child_item = item.child(row)
            parameter_attributes = child_item.data(Qt.UserRole)
            if parameter_attributes is not None:
                if not (parameter_attributes.get('R_Only', 0) == 1 and parameter_attributes.get('W_Only', 0) == 0):
                    write_flag += 1
            if child_item is not None:
                write_flag += self.traverse_items_R_Only_catalog_check(child_item)

        return write_flag

    def setValue(self, value, index):
        delegate_attributes = index.data(Qt.UserRole)
        if delegate_attributes is not None:
            if delegate_attributes.get('type', '') == 'enum':
                enum_strings = delegate_attributes.get('enum_strings', '')
                enum_str = enum_strings[value]
                if delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0:
                    self.model().setData(index, enum_str, Qt.DisplayRole)
                else:
                    self.model().setData(index, value, Qt.EditRole)
            elif delegate_attributes.get('type', '') == 'unsigned' or delegate_attributes.get('type', '') == 'signed' \
                    or delegate_attributes.get('type', '') == 'string':
                if delegate_attributes.get('visual_type', '') == 'ip_format':
                    value = socket.inet_ntoa(struct.pack('!L', value))
                elif delegate_attributes.get('visual_type', '') == 'hex':
                    mac_address = binascii.hexlify(value).decode('utf-8').upper()
                    mac_address_with_colons = ':'.join(mac_address[i:i + 2] for i in range(0, len(mac_address), 2))
                    value = mac_address_with_colons
                elif delegate_attributes.get('visual_type', '') == 'bin' and delegate_attributes.get('type', '') == 'unsigned':
                    par_size = delegate_attributes.get('param_size', 0)
                    binary_string = format(value, f'0{par_size * 8}b')
                    grouped_binary_string = ' '.join(
                        [binary_string[i:i + 4] for i in range(0, len(binary_string), 4)])
                    # Создаем объект BitArray из байтового массива
                    value = grouped_binary_string
                if delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0:
                    self.model().setData(index, value, Qt.DisplayRole)
                else:
                    self.model().setData(index, value, Qt.EditRole)
            elif delegate_attributes.get('type', '') == 'float':
                # Округлюємо до 7 знака після коми
                value = round(value, 7)
                if delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0:
                    self.model().setData(index, value, Qt.DisplayRole)
                else:
                    self.model().setData(index, value, Qt.EditRole)

            elif delegate_attributes.get('type', '') == 'date_time':
                value += datetime.datetime(2000, 1, 1).timestamp()
                datetime_obj = datetime.datetime.fromtimestamp(value)
                value = datetime_obj.strftime('%d.%m.%Y %H:%M:%S')
                if delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0:
                    self.model().setData(index, value, Qt.DisplayRole)
                else:
                    self.model().setData(index, value, Qt.EditRole)

    def read_value_by_modbus(self, index):
        cat_or_param_attributes = index.data(Qt.UserRole)
        if cat_or_param_attributes.get('is_catalog', 0) == 1:
            return
        else:
            modbus_reg = cat_or_param_attributes.get('modbus_reg', '')
            if cat_or_param_attributes.get('type', '') == 'enum':
                reg_count = 1
                byte_size = 1
            else:
                byte_size = cat_or_param_attributes.get('param_size', 0)
                if byte_size < 2:
                    reg_count = 1
                else:
                    reg_count = byte_size // 2

        if is_valid_ip(self.dev_address):
            ip = self.dev_address
            client = ModbusTcpClient(ip)
            slave_id = 1
        else:
            # Регулярний вираз для розбору адреси ком-порту
            pattern = r'(\d+)\s*\((\w+)\)'
            match = re.match(pattern, self.dev_address)

            if match:
                slave_id = int(match.group(1))
                selected_port = match.group(2)
            else:
                print("Pattern not found in the string")
            client = ModbusSerialClient(method='rtu', port=selected_port, baudrate=9600)
        param_type = cat_or_param_attributes.get('type', '')
        param_value = read_parameter(client, slave_id, modbus_reg, reg_count, param_type, byte_size)

        next_column_index = index.sibling(index.row(), index.column() + 1)
        self.setValue(param_value, next_column_index)

        # self.read_modbus_thread = Read_value_by_modbus_Thread(self, modbus_reg)
        # self.connect_thread.finished.connect(self.on_connect_thread_finished)
        # self.connect_thread.error.connect(self.on_connect_thread_error)
        # self.connect_thread.result_signal.connect(self.connect_finished)
        # self.connect_thread.start()
        return param_value

    def read_catalog_by_modbus(self, index, show_prorgess_flag):
        cat_or_param_attributes = index.data(Qt.UserRole)
        if show_prorgess_flag == 1:
            self.read_wait_widget = AQ_wait_progress_bar_widget('Reading current values...', self.parent)
            self.read_wait_widget.setGeometry(self.parent.width() // 2 - 170, self.parent.height() // 4, 340, 50)

        if cat_or_param_attributes.get('is_catalog', 0) == 0:
            return
        else:
            item_cur_cat = self.model().itemFromIndex(index)
            if show_prorgess_flag == 1:
                max_value = 100  # Максимальное значение для прогресс-бара
                row_count = item_cur_cat.rowCount()
                step_value = max_value // row_count

            for row in range(item_cur_cat.rowCount()):
                child_item = item_cur_cat.child(row)
                child_index = self.model().index(row, 0, index)
                child_attributes = child_item.data(Qt.UserRole)
                if child_attributes is not None:
                    if child_attributes.get('is_catalog', 0) == 1:
                        self.read_catalog_by_modbus(child_index, 0)
                    else:
                        if is_valid_ip(self.dev_address):
                            ip = self.dev_address
                            client = ModbusTcpClient(ip)
                            slave_id = 1
                        else:
                            # Регулярний вираз для розбору адреси ком-порту
                            pattern = r'(\d+)\s*\((\w+)\)'
                            match = re.match(pattern, self.dev_address)

                            if match:
                                slave_id = int(match.group(1))
                                selected_port = match.group(2)
                            else:
                                print("Pattern not found in the string")
                            client = ModbusSerialClient(method='rtu', port=selected_port, baudrate=9600)
                        param_type = child_attributes.get('type', '')
                        modbus_reg = child_attributes.get('modbus_reg', '')
                        if child_attributes.get('type', '') == 'enum':
                            reg_count = 1
                            byte_size = 1
                        else:
                            byte_size = child_attributes.get('param_size', 0)
                            if byte_size < 2:
                                reg_count = 1
                            else:
                                reg_count = byte_size // 2

                        param_value = read_parameter(client, slave_id, modbus_reg, reg_count, param_type, byte_size)

                        next_column_index = child_index.sibling(child_index.row(), child_index.column() + 1)
                        self.setValue(param_value, next_column_index)

                if show_prorgess_flag == 1:
                    self.read_wait_widget.progress_bar.setValue((row + 1) * step_value)

            if show_prorgess_flag == 1:
                self.read_wait_widget.progress_bar.setValue(max_value)
                self.read_wait_widget.hide()
                self.read_wait_widget.deleteLater()

    def read_all_tree_by_modbus(self, item):
        self.read_wait_widget = AQ_wait_progress_bar_widget('Reading current values...', self.parent)
        self.read_wait_widget.setGeometry(self.parent.width() // 2 - 170, self.parent.height() // 4, 340, 50)

        max_value = 100  # Максимальное значение для прогресс-бара
        row_count = item.rowCount()
        step_value = max_value // row_count
        for row in range(item.rowCount()):
            index = self.model().index(row, 0, item.index())
            self.read_catalog_by_modbus(index, 0)
            self.read_wait_widget.progress_bar.setValue((row + 1) * step_value)

        self.read_wait_widget.progress_bar.setValue(max_value)
        self.read_wait_widget.hide()
        self.read_wait_widget.deleteLater()

    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid() and index.column() == 0:
            # Получаем элемент модели по индексу
            item = self.model().itemFromIndex(index)
            cat_or_param_attributes = index.data(Qt.UserRole)
            if item:
                if cat_or_param_attributes.get('is_catalog', 0) == 1:
                    # Создаем контекстное меню
                    context_menu = QMenu(self)
                    context_menu.setStyleSheet("""
                                                                QMenu {
                                                                    color: #D0D0D0;
                                                                }

                                                                QMenu::item:selected {
                                                                    background-color: #3a3a3a;
                                                                    color: #FFFFFF;
                                                                }
                                                            """)
                    # Добавляем действие в контекстное меню
                    action_read = context_menu.addAction("Read parameters")
                    if self.traverse_items_R_Only_catalog_check(item) > 0:
                        action_write = context_menu.addAction("Write parameters")
                    # Подключаем обработчик события выбора действия
                    action_read.triggered.connect(lambda: self.read_catalog_by_modbus(index, 1))
                    # Показываем контекстное меню
                    context_menu.exec_(event.globalPos())
                else:
                    # Создаем контекстное меню
                    context_menu = QMenu(self)
                    context_menu.setStyleSheet("""
                                            QMenu {
                                                color: #D0D0D0;
                                            }
                                        
                                            QMenu::item:selected {
                                                background-color: #3a3a3a;
                                                color: #FFFFFF;
                                            }
                                        """)
                    # Добавляем действие в контекстное меню
                    action_read = context_menu.addAction("Read parameter")
                    if not (cat_or_param_attributes.get("R_Only", 0) == 1 and cat_or_param_attributes.get("W_Only", 0) == 0):
                        action_write = context_menu.addAction("Write parameter")
                    # Подключаем обработчик события выбора действия
                    action_read.triggered.connect(lambda: self.read_value_by_modbus(index))
                    # Показываем контекстное меню
                    context_menu.exec_(event.globalPos())
        else:
            # Если индекс недействителен, вызывается обработчик события контекстного меню по умолчанию
            super().contextMenuEvent(event)


class Read_value_by_modbus_Thread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result_signal = pyqtSignal(object)  # Сигнал для передачи данных в главное окно
    def __init__(self, parent, modus_reg):
        super().__init__(parent)
        self.parent = parent
        self.modbus_reg = modus_reg

    def run(self):
        try:
            # Здесь выполняем ваш код функции connect_to_device
            # self.parent.connect_to_device()
            # client.connect()
            # # Читаем 16 регистров начиная с адреса 0xF000 (device_name)
            # start_address = 0xF000
            # register_count = 16
            # # Выполняем запрос
            # response = client.read_holding_registers(start_address, register_count, slave_id)
            # # Конвертируем значения регистров в строку
            # hex_string = ''.join(format(value, '04X') for value in response.registers)
            # # Конвертируем строку в массив байт
            # byte_array = bytes.fromhex(hex_string)
            # byte_array = swap_modbus_bytes(byte_array, register_count)
            #
            # client.close()
            result_data = self.parent.connect_to_device()  # Данные, которые нужно передать в главное окно
            self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
            # По завершении успешного выполнения
            self.finished.emit()
        except Exception as e:
            # В случае ошибки передаем текст ошибки обратно в главный поток
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        MainName = 'AQteck Tool MAX'
        PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'
        self.AQicon = QIcon(PROJ_DIR + 'Icons/AQico_silver.png')
        self.icoClose = QIcon(PROJ_DIR + 'Icons/Close.png')
        self.icoMaximize = QIcon(PROJ_DIR + 'Icons/Maximize.png')
        self.icoNormalize = QIcon(PROJ_DIR + 'Icons/_Normalize.png')
        self.icoMinimize = QIcon(PROJ_DIR + 'Icons/Minimize.png')
        self.ico_AddDev_btn = QIcon(PROJ_DIR + 'Icons/test_Button.png')
        self.ico_btn_add_devise = QIcon(PROJ_DIR + 'Icons/Add_device.png')
        self.ico_btn_delete_device = QIcon(PROJ_DIR + 'Icons/Delete_device.png')
        self.ico_btn_ip_adresses = QIcon(PROJ_DIR + 'Icons/ip_adresses.png')
        self.background_pic = QPixmap(PROJ_DIR + 'Icons/industrial_pic.png')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle(MainName)
        self.setWindowIcon(self.AQicon)
        self.setGeometry(100, 100, 600, 500)
        self.setMinimumSize(300, 400)
        self.resizeLineWidth = 4
        self.spacing_between_frame = 2
        self.not_titlebtn_zone = 0
        self.tool_panel_layout_mask = 0
        # Получаем текущий рабочий каталог (папку проекта)
        project_path = os.getcwd()
        # Объединяем путь к папке проекта с именем файла настроек
        settings_path = os.path.join(project_path, "auto_load_settings.ini")
        # Используем полученный путь в QSettings
        self.auto_load_settings = QSettings(settings_path, QSettings.IniFormat)
        # Порожній список для дерев девайсів
        self.devices_trees = []
        self.devices = []
        self.current_active_dev_index = 0

        #MainWindowFrame
        self.main_window_frame = main_frame_AQFrame(self)
        #TitleBarFrame
        self.title_bar_frame = title_bar_frame_AQFrame(self, 60, MainName, self.AQicon, self.main_window_frame)
        # ToolPanelFrame
        self.tool_panel_frame = tool_panel_frame_AQFrame(self.title_bar_frame.height(), self.main_window_frame)
        # MainFieldFrame
        self.main_field_frame = main_field_frame_AQFrame(self.title_bar_frame.height() + self.tool_panel_frame.height(), self)

        # Создаем заставочную картинку для главного поля
        self.main_background_pic = QLabel(self.main_field_frame)
        self.main_background_pic.setPixmap(self.background_pic)
        self.main_background_pic.setScaledContents(True)
        self.main_background_pic.setGeometry(0, 0, 450, 326)

        #Создаем горизонтальный макет панели инструментов
        self.tool_panel_layout = QHBoxLayout(self.tool_panel_frame)
        self.tool_panel_layout.setContentsMargins(4, 0, 0, 0)
        self.tool_panel_layout.setSpacing(0)

        self.tool_separator1 = VLine_separator(self.tool_panel_frame.height())
        self.tool_separator2 = VLine_separator(self.tool_panel_frame.height())
        self.tool_separator3 = VLine_separator(self.tool_panel_frame.height())
        self.tool_separator4 = VLine_separator(self.tool_panel_frame.height())
        self.tool_separator5 = VLine_separator(self.tool_panel_frame.height())
        self.tool_separator6 = VLine_separator(self.tool_panel_frame.height())
        self.tool_separator7 = VLine_separator(self.tool_panel_frame.height())

        # # Создаем кнопки панели инструментов
        self.panel_btn_add_dev = Btn_AddDevices(self.ico_btn_add_devise, self.tool_panel_frame)
        self.panel_btn_add_dev.clicked.connect(self.open_AddDevices)
        self.panel_btn_add_dev1 = Btn_DeleteDevices(self.ico_btn_delete_device, self.tool_panel_frame)
        self.panel_btn_add_dev2 = Btn_IPAdresess(self.ico_btn_ip_adresses, self.tool_panel_frame)
        self.panel_btn_add_dev3 = Btn_Read(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev3.clicked.connect(self.read_parameters)
        self.panel_btn_add_dev4 = Btn_Write(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev5 = Btn_FactorySettings(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev6 = Btn_WatchList(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev7 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev8 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev9 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev10 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev11 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev12 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev13 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev14 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev15 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev16 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev17 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)
        self.panel_btn_add_dev18 = AddDeviceButton(self.ico_AddDev_btn, self.tool_panel_frame)

        # Создаем горизонтальный макет группы коннекта
        self.connect_group_layout = QHBoxLayout(self.tool_panel_frame)
        self.connect_group_layout.setContentsMargins(2, 0, 2, 0)
        self.connect_group_layout.setSpacing(0)

        # Создаем горизонтальный макет группы обмена
        self.MB_exchange_group_layout = QHBoxLayout(self.tool_panel_frame)
        self.MB_exchange_group_layout.setContentsMargins(2, 0, 2, 0)
        self.MB_exchange_group_layout.setSpacing(0)

        # Создаем горизонтальный макет группы настройки
        self.settings_group_layout = QHBoxLayout(self.tool_panel_frame)
        self.settings_group_layout.setContentsMargins(2, 0, 2, 0)
        self.settings_group_layout.setSpacing(0)

        # Создаем горизонтальный макет группы архива
        self.archive_group_layout = QHBoxLayout(self.tool_panel_frame)
        self.archive_group_layout.setContentsMargins(2, 0, 2, 0)
        self.archive_group_layout.setSpacing(0)

        # Создаем горизонтальный макет группы маршрутизатора
        self.router_group_layout = QHBoxLayout(self.tool_panel_frame)
        self.router_group_layout.setContentsMargins(2, 0, 2, 0)
        self.router_group_layout.setSpacing(0)

        # Создаем горизонтальный макет группы обновления ПО
        self.firmware_group_layout = QHBoxLayout(self.tool_panel_frame)
        self.firmware_group_layout.setContentsMargins(2, 0, 2, 0)
        self.firmware_group_layout.setSpacing(0)

        # Создаем горизонтальный макет группы параметры устройтва
        self.properties_group_layout = QHBoxLayout(self.tool_panel_frame)
        self.properties_group_layout.setContentsMargins(2, 0, 2, 0)
        self.properties_group_layout.setSpacing(0)

        self.connect_group_layout.addWidget(self.panel_btn_add_dev, 0)
        self.connect_group_layout.addWidget(self.panel_btn_add_dev1, 0)
        self.connect_group_layout.addWidget(self.panel_btn_add_dev2, 0)

        self.MB_exchange_group_layout.addWidget(self.panel_btn_add_dev3, 0)
        self.MB_exchange_group_layout.addWidget(self.panel_btn_add_dev4, 0)
        self.MB_exchange_group_layout.addWidget(self.panel_btn_add_dev5, 0)
        self.MB_exchange_group_layout.addWidget(self.panel_btn_add_dev6, 0)

        self.settings_group_layout.addWidget(self.panel_btn_add_dev7, 0)
        self.settings_group_layout.addWidget(self.panel_btn_add_dev8, 0)
        self.settings_group_layout.addWidget(self.panel_btn_add_dev9, 0)

        self.archive_group_layout.addWidget(self.panel_btn_add_dev10, 0)
        self.archive_group_layout.addWidget(self.panel_btn_add_dev11, 0)

        self.router_group_layout.addWidget(self.panel_btn_add_dev12, 0)
        self.router_group_layout.addWidget(self.panel_btn_add_dev13, 0)

        self.firmware_group_layout.addWidget(self.panel_btn_add_dev14, 0)
        self.firmware_group_layout.addWidget(self.panel_btn_add_dev15, 0)
        self.firmware_group_layout.addWidget(self.panel_btn_add_dev16, 0)

        self.properties_group_layout.addWidget(self.panel_btn_add_dev17, 0)
        self.properties_group_layout.addWidget(self.panel_btn_add_dev18, 0)

        self.tool_panel_layout.addLayout(self.connect_group_layout, 0)
        self.tool_panel_layout.addWidget(self.tool_separator1, 0)
        self.tool_panel_layout.addLayout(self.MB_exchange_group_layout, 0)
        self.tool_panel_layout.addWidget(self.tool_separator2, 0)
        self.tool_panel_layout.addLayout(self.settings_group_layout, 0)
        self.tool_panel_layout.addWidget(self.tool_separator3, 0)
        self.tool_panel_layout.addLayout(self.archive_group_layout, 0)
        self.tool_panel_layout.addWidget(self.tool_separator4, 0)
        self.tool_panel_layout.addLayout(self.router_group_layout, 0)
        self.tool_panel_layout.addWidget(self.tool_separator5, 0)
        self.tool_panel_layout.addLayout(self.firmware_group_layout, 0)
        self.tool_panel_layout.addWidget(self.tool_separator6, 0)
        self.tool_panel_layout.addLayout(self.properties_group_layout, 0)
        self.tool_panel_layout.addWidget(self.tool_separator7, 0)
        self.tool_panel_layout.addStretch(1)

        # # Создаем виджеты для изменения размеров окна
        self.resizeWidthR_widget = resizeWidthR_Qwidget(self)
        self.resizeWidthL_widget = resizeWidthL_Qwidget(self)
        self.resizeHeigthLow_widget = resizeHeigthLow_Qwidget(self)
        self.resizeHeigthTop_widget = resizeHeigthTop_Qwidget(self)
        self.resizeDiag_BotRigth_widget = resizeDiag_BotRigth_Qwidget(self)
        self.resizeDiag_BotLeft_widget = resizeDiag_BotLeft_Qwidget(self)
        self.resizeDiag_TopLeft_widget = resizeDiag_TopLeft_Qwidget(self)
        self.resizeDiag_TopRigth_widget = resizeDiag_TopRigth_Qwidget(self)

        # Создаем кнопку закрытия
        self.btn_close = QPushButton('', self.title_bar_frame)
        self.btn_close.setIcon(QIcon(self.icoClose))  # установите свою иконку для кнопки
        self.btn_close.setGeometry(self.title_bar_frame.width() - 35, 0, 35, 35)  # установите координаты и размеры кнопки
        self.btn_close.clicked.connect(self.close)  # добавляем обработчик события нажатия на кнопку закрытия
        self.btn_close.setStyleSheet(""" QPushButton:hover {background-color: #555555;}""")

        #Создаем кнопку свернуть
        self.btn_minimize = QPushButton('', self.title_bar_frame)
        self.btn_minimize.setIcon(QIcon(self.icoMinimize))  # установите свою иконку для кнопки
        self.btn_minimize.setGeometry(self.title_bar_frame.width() - 105, 0, 35, 35)  # установите координаты и размеры кнопки
        self.btn_minimize.clicked.connect(self.showMinimized)
        self.btn_minimize.setStyleSheet(""" QPushButton:hover {background-color: #555555;}""")

        #Создаем кнопку развернуть/нормализировать
        self.isMaximized = False  # Флаг, указывающий на текущее состояние окна
        self.btn_maximize = QPushButton('', self.title_bar_frame)
        self.btn_maximize.setIcon(QIcon(self.icoMaximize))  # установите свою иконку для кнопки
        self.btn_maximize.setGeometry(self.title_bar_frame.width() - 70, 0, 35, 35)  # установите координаты и размеры кнопки
        self.btn_maximize.clicked.connect(self.toggleMaximize)  # добавляем обработчик события нажатия на кнопку закрытия
        self.btn_maximize.setStyleSheet(""" QPushButton:hover {background-color: #555555;}""")

    def toggleMaximize(self):
        try:
            if self.isMaximized:
                self.showNormal()
                self.btn_maximize.setIcon(QIcon(self.icoMaximize))
                self.isMaximized = False
            else:
                self.showMaximized()
                self.btn_maximize.setIcon(QIcon(self.icoNormalize))
                self.isMaximized = True
        except Exception as e:
            print(f"Error occurred: {str(e)}")

    def resizeEvent(self, event):
        try:
            # Переопределяем метод resizeEvent и вызываем resize для main_window_frame
            self.main_window_frame.resize(self.width(), self.height())
            self.title_bar_frame.resize(self.width(), self.title_bar_frame.height())
            self.title_bar_frame.custom_resize()
            self.tool_panel_frame.resize(self.main_window_frame.width(), self.tool_panel_frame.height())
            self.main_field_frame.resize(self.main_window_frame.width(), self.height() -
                                        (self.title_bar_frame.height() + self.tool_panel_frame.height() + 2))
            self.btn_maximize.move(self.title_bar_frame.width() - 70, 0)
            self.btn_minimize.move(self.title_bar_frame.width() - 105, 0)
            self.btn_close.move(self.title_bar_frame.width() - 35, 0)
            self.resizeWidthR_widget.setGeometry(self.width() - self.resizeLineWidth,
                                                 self.resizeLineWidth, self.resizeLineWidth,
                                                 self.height() - (self.resizeLineWidth * 2))
            self.resizeWidthL_widget.setGeometry(0, self.resizeLineWidth, self.resizeLineWidth,
                                                 self.height() - (self.resizeLineWidth * 2))
            self.resizeHeigthLow_widget.setGeometry(self.resizeLineWidth, self.height() - self.resizeLineWidth,
                                                    self.width() - (self.resizeLineWidth * 2),
                                                    self.resizeLineWidth)
            self.resizeHeigthTop_widget.setGeometry(self.resizeLineWidth, 0,
                                                    self.width() - (self.resizeLineWidth * 2),
                                                    self.resizeLineWidth)
            self.resizeDiag_BotRigth_widget.move(self.width() - self.resizeLineWidth,
                                                 self.height() - self.resizeLineWidth)
            self.resizeDiag_TopLeft_widget.move(0, 0)
            self.resizeDiag_TopRigth_widget.move(self.width() - self.resizeLineWidth, 0)
            self.resizeDiag_BotLeft_widget.move(0, self.height() - self.resizeLineWidth)

            replaceToolPanelWidget(self, self.tool_panel_layout)

            # Получаем размеры родительского виджета
            parent_size = self.main_field_frame.size()
            # Получаем размеры картинки
            pic_size = self.main_background_pic.size()
            # Вычисляем координаты верхнего левого угла картинки
            x = (parent_size.width() - pic_size.width()) // 2
            y = (parent_size.height() - pic_size.height()) // 2
            # Устанавливаем положение картинки
            self.main_background_pic.move(x, y)

            device_data = self.devices[self.current_active_dev_index]
            if device_data is not None:
                tree_view = device_data.get('tree_view')
                if tree_view is not None:
                    tree_view.setGeometry(250, 2, self.main_field_frame.width() - 252, self.main_field_frame.height() - 4)

            event.accept()
        except Exception as e:
            print(f"Error occurred: {str(e)}")

    def open_AddDevices(self):
        AddDevices_window = AddDevices_AQDialog('Add Devices', self)
        AddDevices_window.exec_()

    def connect_to_device_COM(self, selected_port, slave_id):
        # Если уже установлено соединение, закрываем его
        # if self.serial and self.serial.is_open:
        #     self.serial.close()

        try:
            device_data = {}
            client = ModbusSerialClient(method='rtu', port=selected_port, baudrate=9600)
            device_name = read_device_name(client, slave_id)
            version = read_version(client, slave_id)
            serial_number = read_serial_number(client, slave_id)
            default_prg = read_default_prg(client, slave_id)
            device_data['device_name'] = device_name
            device_data['version'] = version
            device_data['serial_number'] = serial_number
            device_data['default_prg'] = default_prg
            return device_data
        except:
        # "Ошибка при подключении к COM
        #     raise Connect_err('Ошибка при подключении к COM')
            return 'connect_err'

    def connect_to_device_IP(self, ip):
        try:
            device_data = {}
            client = client = ModbusTcpClient(ip)
            slave_id = 1
            device_name = read_device_name(client, slave_id)
            version = read_version(client, slave_id)
            serial_number = read_serial_number(client, slave_id)
            default_prg = read_default_prg(client, slave_id)
            device_data['device_name'] = device_name
            device_data['version'] = version
            device_data['serial_number'] = serial_number
            device_data['default_prg'] = default_prg
            return device_data
        except:
            # "Ошибка при подключении к IP
            # raise Connect_err('Ошибка при подключении к IP')
            return 'connect_err'

    def parse_default_prg (self, default_prg):
        try:
            containers_count = get_conteiners_count(default_prg)
            containers_offset = get_containers_offset(default_prg)
            storage_container = get_storage_container(default_prg, containers_offset)
            device_tree = parse_tree(storage_container)
            self.devices_trees.append(device_tree)
        except:
            return 'parsing_err'


    def add_tree_view(self, dev_index):
        try:
            # device_tree = self.devices_trees[0]
            device_data = self.devices[dev_index]
            device_tree = device_data.get('device_tree')
            # Створення порожнього массиву параметрів
            self.parameter_list = []
            root = device_tree.invisibleRootItem()
            traverse_items(root, self.parameter_list)

            if isinstance(device_tree, QStandardItemModel):
                # Устанавливаем модель для QTreeView и отображаем его
                address = device_data.get('address')
                device_data['tree_view'] = AQ_TreeView(dev_index, device_tree, address, self.main_field_frame)
                device_data.get('tree_view').show()
                root = device_tree.invisibleRootItem()
                device_data.get('tree_view').traverse_items_show_delegate(root)
                device_data.get('tree_view').read_all_tree_by_modbus(root)
        # except:
            # print(f"Помилка парсінгу")
        except Exception as e:
            print(f"Error occurred: {str(e)}")


    def add_data_to_devices(self, device_data):
        device_dict = {}
        device_dict['device_tree'] = self.devices_trees[0]
        device_dict['device_name'] = device_data.get('device_name', 'err_name')
        device_dict['serial_number'] = device_data.get('serial_number', 'err_S/N')
        device_dict['address'] = device_data.get('address', 'err_address')
        device_dict['version'] = device_data.get('version', 'err_version')
        self.devices.append(device_dict)

    def read_parameters(self):
        device_data = self.devices[self.current_active_dev_index]
        device_tree = device_data.get('device_tree')
        root = device_tree.invisibleRootItem()
        device_data.get('tree_view').read_all_tree_by_modbus(root)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("D:/git/AQtech/AQtech Tool MAX/Icons/Splash3.png"))
    splash.show()

    # Имитация загрузки (можно заменить на вашу реализацию)
    time.sleep(2)  # Например, 2 секунды

    window = MainWindow()
    #window.showMaximized()
    window.show()
    splash.close()
    sys.exit(app.exec_())
