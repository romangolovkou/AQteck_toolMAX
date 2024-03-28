import ipaddress
import re
import socket
from functools import partial

from PySide6.QtCore import Signal, QPoint, Qt, QTimer
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QTableWidget, QFrame, QPushButton, QRadioButton, QStackedWidget, QWidget, \
    QTableWidgetItem, QLineEdit, QLabel

from AqIsValidIpFunc import is_valid_ip
from AqLineEditTemplates import AqSlaveIdLineEdit, AqIpLineEdit
from AqMessageManager import AqMessageManager
from AqWindowTemplate import AqDialogTemplate


class AqGatewayWindow(AqDialogTemplate):
    message_signal = Signal(str, str)

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.maximizeBtnEnable = False

        self.device = None
        self._message_manager = AqMessageManager.get_global_message_manager()

        self.name = 'Gateway'
        self.prepare_ui()

    def prepare_ui(self):
        # Устанавливаем ширину столбцов в таблице справа
        cur_width = self.ui.tableWidget.width()
        self.ui.tableWidget.setColumnWidth(0, int(cur_width * 0.05))
        self.ui.tableWidget.setColumnWidth(1, int(cur_width * 0.17))
        self.ui.tableWidget.setColumnWidth(2, int(cur_width * 0.08))
        self.ui.tableWidget.setColumnWidth(3, int(cur_width * 0.28))
        self.ui.tableWidget.setColumnWidth(4, int(cur_width * 0.17))
        self.ui.tableWidget.setColumnWidth(5, int(cur_width * 0.17))
        self.ui.tableWidget.setColumnWidth(6, int(cur_width * 0.06))
        self.ui.tableFrame.hide()
        self.ui.addDeviceBtn.hide()

        self.ui.mainWidget.prepare_ui()

        self.ui.mainWidget.uiChanged.connect(self.custom_resize)
        self.ui.mainWidget.close_signal.connect(self.close)

        self.message_signal.connect(partial(self._message_manager.show_message, self))
        self._message_manager.subscribe(self.message_signal.emit)

        self.ui.mainWidget.message_signal.connect(self._message_manager.send_main_message)

    def custom_resize(self):
        self.resize(self.width(), self.ui.mainWidget.sizeHint().height())

    def set_working_device(self, device):
        self.ui.mainWidget.set_working_device(device)

    def close(self):
        self._message_manager.de_subscribe(self.message_signal.emit)
        super().close()


class AqGatewayFrame(QFrame):
    uiChanged = Signal()
    close_signal = Signal()
    message_signal = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_ui_elements = None

        self.saveBtn = None
        self.cancelBtn = None
        self.ethRadioBtn = None
        self.rsRadioBtn = None
        self.rtuRadioBtn = None
        self.asciiRadioBtn = None
        self.addDeviceBtn = None
        self.stackedWidget = None
        self.tableFrame = None
        self.tableWidget = None
        self.masterRsPage = None
        self.masterEthPage = None
        self.protocolFrame = None

        self.device = None

    def prepare_ui(self):
        self.saveBtn = self.findChild(QPushButton, 'saveBtn')
        self.cancelBtn = self.findChild(QPushButton, 'cancelBtn')
        self.ethRadioBtn = self.findChild(QRadioButton, 'ethRadioBtn')
        self.rsRadioBtn = self.findChild(QRadioButton, 'rsRadioBtn')
        self.rtuRadioBtn = self.findChild(QRadioButton, 'rtuRadioBtn')
        self.asciiRadioBtn = self.findChild(QRadioButton, 'asciiRadioBtn')
        self.addDeviceBtn = self.findChild(QPushButton, 'addDeviceBtn')
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        self.tableWidget = self.findChild(QTableWidget, 'tableWidget')
        self.tableFrame = self.findChild(QFrame, 'tableFrame')
        self.masterRsPage = self.findChild(QWidget, 'masterRsPage')
        self.masterEthPage = self.findChild(QWidget, 'masterEthPage')
        self.protocolFrame = self.findChild(QWidget, 'protocolFrame')

        self.main_ui_elements = [
            self.saveBtn,
            self.cancelBtn,
            self.ethRadioBtn,
            self.rsRadioBtn,
            self.rtuRadioBtn,
            self.asciiRadioBtn,
            self.addDeviceBtn,
            self.stackedWidget,
            self.tableFrame,
            self.tableWidget,
            self.masterRsPage,
            self.masterEthPage,
            self.protocolFrame
        ]

        for i in self.main_ui_elements:
            if i is None:
                raise Exception(self.objectName() + ' Error: lost UI element')

        self.ethRadioBtn.clicked.connect(self.change_ui_by_selected_mode)
        self.rsRadioBtn.clicked.connect(self.change_ui_by_selected_mode)

        self.saveBtn.clicked.connect(self.save_btn_clicked)
        self.cancelBtn.clicked.connect(self.close_signal.emit)
        self.addDeviceBtn.clicked.connect(self.tableWidget.append_row)

    def set_working_device(self, device):
        self.device = device

    def change_ui_by_selected_mode(self):
        if self.rsRadioBtn.isChecked():
            self.show_rs_master_if()
        else:
            self.show_eth_master_if()

        self.uiChanged.emit()

    def show_rs_master_if(self):
        widget = getattr(self, "masterRsPage")
        self.stackedWidget.setCurrentWidget(widget)
        self.tableFrame.show()
        self.protocolFrame.hide()
        self.addDeviceBtn.show()


    def show_eth_master_if(self):
        self.tableFrame.hide()
        widget = getattr(self, "masterEthPage")
        self.stackedWidget.setCurrentWidget(widget)
        self.protocolFrame.show()
        self.addDeviceBtn.hide()

    def save_btn_clicked(self):
        if self.tableWidget.rowCount() < 1:
            self.message_signal.emit('Error', 'Empty table')
            return
        if self.ethRadioBtn.isChecked():
            self._write_eth_master()
        elif self.rsRadioBtn.isChecked():
            self._write_rs_master()
        else:
            self.message_signal.emit('Error', 'Incorrect rule')
            return

    def _write_rs_master(self):
        items_to_write = list()
        # rs485 mode
        item = self.device.get_item_by_modbus_reg(1540)
        item.value = 1  # slave mode
        item.param_status = 'changed'
        items_to_write.append(item)
        # Rules starting at R1
        pattern = r'^\w{1,2}:\d:[0-9A-F]{1,2}:[A-F0-9]{8}:[0-9A-F]{1,3}:[0-9A-F]{1,2}:[A-Z]$'
        rules_list = list()
        for i in range(31):
            rule_string = self._get_rule_string_from_table(i)
            if rule_string is not None and re.match(pattern, rule_string):
                rules_list.append(rule_string)
            else:
                rules_list.append('')

        for i in range(31):
            item = self.device.get_item_by_modbus_reg(1024 + i*16) #R1-R31 (rules for gateway)
            rule_string = rules_list[i]
            item.value = zero_fill_str(rule_string, item.param_size)
            item.param_status = 'changed'
            items_to_write.append(item)

        # для зручності розгортаємо порядок
        items_to_write = items_to_write[::-1]

        self.device.write_parameters(items_to_write, message_feedback_flag=True)

        # self.close_signal.emit()

    def _write_eth_master(self):
        items_to_write = list()
        # rs485 mode
        item = self.device.get_item_by_modbus_reg(1540)
        item.value = 0  # master mode
        item.param_status = 'changed'
        items_to_write.append(item)
        # Rules starting at R1
        item = self.device.get_item_by_modbus_reg(1024)
        PROT = 'R' if self.rtuRadioBtn.isChecked() else 'A'
        rule_string = f'7:0:G:40:0:S:{PROT}'
        item.value = zero_fill_str(rule_string, item.param_size)
        item.param_status = 'changed'
        items_to_write.append(item)
        # in eth_master mode other rules as 0
        for i in range(30):
            item = self.device.get_item_by_modbus_reg(1040 + i*16) #R2-R31 (rules for gateway)
            rule_string = ''
            item.value = zero_fill_str(rule_string, item.param_size)
            item.param_status = 'changed'
            items_to_write.append(item)

        # для зручності розгортаємо порядок
        items_to_write = items_to_write[::-1]

        self.device.write_parameters(items_to_write, message_feedback_flag=True)

        # self.close_signal.emit()

    def _get_rule_string_from_table(self, row):
        # З таблиці беремо тільки для режиму RS-master тому строка з правилом
        # завжди починаеться з коду вхідного інтерфейсу - RS485
        #
        # Загальний формат строки правила:
        #        v<-----------Вхідний пакет----------------->vv<-----------Вихідний пакет-------------------------------------------->v
        #        'код_вх_інтерфейсу:код_вх_порту:вх_слейв_айді:код_вих_інтерфейсу:код_вих_порту:вих_слейв_айді:вих_протокол(RTU/ASCII/TCP)'
        #
        # коди вхідних інтерфейсів
        # 0х27 - Сервісний для зв'язку з конфігуратором
        # 0х40 - RS485
        # 0х06 - Ethernet
        # у строку додаємо без приставки 0х
        # також є вхідний порт який завжди буде 0 (було зроблено про запас, не застосовується)

        rule_string = '40:0:'
        rule_dict = self.tableWidget.get_row_values(row)
        if rule_dict is None:
            return None

        # Додаємо код вхідного слейв айді
        # 0х00-0хFF - слейв айді у форматі гекс
        # G - Приймати пакети від будь якого слейв айді
        in_slave_id = hex(int(rule_dict['in_slave_id']))[2:]
        rule_string += f'{in_slave_id.upper()}:'

        # Код вихідного інтерфейсу
        # 0х40 - RS485
        # ip-адреса у форматі гекс (приклад: 0x0A0219D2, оріг - 10.2.25.210) - Ethernet
        # 0x00 - доступ до регістрів шлюзу
        out_ip = rule_dict['out_ip']
        out_ip = socket.inet_aton(out_ip).hex()
        rule_string += f'{out_ip.upper()}:'

        # Код вихідного порту У форматі гекс
        out_port = hex(int(rule_dict['out_port']))[2:]
        rule_string += f'{out_port.upper()}:'

        # Код вихідного слейв айді У форматі гекс
        # 0х00-0хFF - слейв айді у форматі гекс
        # S - не міняти слейв айді вхідного пакету (використати вхідний слейв айді)
        out_slave_id = hex(int(rule_dict['out_slave_id']))[2:]
        rule_string += f'{out_slave_id.upper()}:'

        # Вихідний протокол
        # A - ASCII
        # P - TCP
        # R - RTU
        # у цій функции додаємо тільки P - TCP
        rule_string += 'P'

        return rule_string


class AqGatewayTableWidget(QTableWidget):
    clickedRow = Signal(int, QPoint)

    row_number_col = 0
    in_slave_id_col = 1
    decor_arrow_col = 2
    out_ip_col = 3
    out_port_col = 4
    out_slave_id_col = 5
    delete_btn_col = 6

    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setMinimumSectionSize(8)
        self.setRowCount(0)
        self.setFixedWidth(420)
        self.setMaximumHeight(420)
        self.verticalScrollBar().rangeChanged.connect(self.on_vertical_scrollbar_range_changed)
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        # Убираем рамку таблицы
        self.setStyleSheet("""QTableWidget { border: none; color: #D0D0D0; background-color: #16191d;}
                            QTableWidget::item { padding-left: 3px; }
                            QTableWidget::item:!focus {
                            background-color: transparent;}
                            QScrollBar:vertical {
                                background: #1e1f22;
                                width: 10px;  /* Ширина вертикального скроллбара */
                            }
                            QScrollBar:horizontal {
                                background: #1e1f22;
                                height: 10px;  /* Высота горизонтального скроллбара */
                            }
                            """)
        self.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self, row, col):
        if col == 6:
            self.removeRow(row)
            self.refresh_row_numbers()

        self.clickedRow.emit(row, col)

    def append_row(self):
        # if new_row_index is None:
        new_row_index = self.rowCount()
        if new_row_index == 31:
            return
        self.setRowCount(self.rowCount() + 1)
        # Создаем элементы таблицы для каждой строки
        # number_item = QTableWidgetItem(str(new_row_index + 1))
        # number_item.setFlags(number_item.flags() & ~Qt.ItemIsEditable)
        number_item = QLineEdit(str(new_row_index + 1))
        number_item.setReadOnly(True)
        # in_slave_id_item = QTableWidgetItem(str(new_row_index + 1))
        in_slave_id_item = AqSlaveIdGatewayLineEdit(self)
        in_slave_id_item.setText(str(new_row_index + 1))
        in_slave_id_item.setAlignment(Qt.AlignmentFlag.AlignCenter)

        decor_label_item = QLabel()
        # Додаємо декоративну іконку
        decor_label_item.setPixmap(QPixmap('UI/icons/arrow_right_blue.png').scaled(self.columnWidth(2)*0.75, 10))

        if new_row_index == 0:
            prev_ip = '192.168.1.100'
        else:
            prev_ip = self.cellWidget(new_row_index - 1, self.out_ip_col).text()
            if is_valid_ip(prev_ip):
                ip_int = int(ipaddress.ip_address(prev_ip))
                prev_ip = str(ipaddress.ip_address(ip_int + 1))
            else:
                prev_ip = '192.168.1.100'

        # out_ip_address_item = QTableWidgetItem(prev_ip)
        out_ip_address_item = AqIpGatewayLineEdit(self)
        out_ip_address_item.setAlignment(Qt.AlignmentFlag.AlignCenter)
        out_ip_address_item.setText(prev_ip)
        out_ip_port_item = AqPortGatewayLineEdit(self)
        out_ip_port_item.setAlignment(Qt.AlignmentFlag.AlignCenter)
        out_ip_port_item.setText('502')
        # out_slave_id = QTableWidgetItem('1')
        out_slave_id_item = AqSlaveIdGatewayLineEdit(self)
        out_slave_id_item.setAlignment(Qt.AlignmentFlag.AlignCenter)
        out_slave_id_item.setText('1')
        delete_btn_item = QTableWidgetItem()
        # Додаємо іконку видалити
        icon = QIcon('UI/icons/trash.png')
        # item = self.item(new_row_index, 6)
        delete_btn_item.setIcon(icon)
        delete_btn_item.setTextAlignment(Qt.AlignCenter)

        # Устанавливаем элементы таблицы
        self.setCellWidget(new_row_index, self.row_number_col, number_item)
        self.setCellWidget(new_row_index, self.in_slave_id_col, in_slave_id_item)
        self.setCellWidget(new_row_index, self.decor_arrow_col, decor_label_item)
        self.setCellWidget(new_row_index, self.out_ip_col, out_ip_address_item)
        self.setCellWidget(new_row_index, self.out_port_col, out_ip_port_item)
        self.setCellWidget(new_row_index, self.out_slave_id_col, out_slave_id_item)
        self.setItem(new_row_index, self.delete_btn_col, delete_btn_item)

    def refresh_row_numbers(self):
        for i in range(self.rowCount()):
            self.cellWidget(i, self.row_number_col).setText(str(i + 1))

    def on_vertical_scrollbar_range_changed(self, minimum, maximum):
        pass

    def get_row_values(self, row):
        if row >= self.rowCount():
            return None
        row_dict = dict()
        row_dict['in_slave_id'] = self.cellWidget(row, self.in_slave_id_col).text()
        row_dict['out_ip'] = self.cellWidget(row, self.out_ip_col).text()
        row_dict['out_port'] = self.cellWidget(row, self.out_port_col).text()
        row_dict['out_slave_id'] = self.cellWidget(row, self.out_slave_id_col).text()

        return row_dict

class AqSlaveIdGatewayLineEdit(AqSlaveIdLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def err_blink(self):
        if self.anim_cnt < 34:
            self.anim_cnt += 1
            if self.anim_cnt < 18:
                self.color_code = self.color_code + 0xA
            else:
                self.color_code = self.color_code - 0xA

            hex_string = format(self.color_code, 'x')
            self.setStyleSheet("background-color: #{}2d30; \n".format(hex_string))
        else:
            self.anim_cnt = 0
            self.color_code = 0x2b
            self.setStyleSheet("background-color: transparent; \n")
            self.red_blink_timer.stop()

    def show_err_label(self):
        pass
        # # Получаем координаты поля ввода относительно диалогового окна
        # rect = self.geometry()
        # pos = self.mapTo(self, rect.topRight())
        # self.err_label = QLabel('Invalid value, <br> valid (0...247)', self.parent())
        # self.err_label.setStyleSheet("color: #fe2d2d; \n")
        # self.err_label.setFixedSize(100, 35)
        # self.err_label.move(pos.x() - 90, pos.y() - 35)
        # self.err_label.show()
        # # Устанавливаем задержку в 2 секунды и затем удаляем метку
        # QTimer.singleShot(3000, self.err_label.deleteLater)


class AqIpGatewayLineEdit(AqIpLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def err_blink(self):
        if self.anim_cnt < 34:
            self.anim_cnt += 1
            if self.anim_cnt < 18:
                self.color_code = self.color_code + 0xA
            else:
                self.color_code = self.color_code - 0xA

            hex_string = format(self.color_code, 'x')
            self.setStyleSheet("background-color: #{}2d30;\n".format(hex_string))
        else:
            self.anim_cnt = 0
            self.color_code = 0x2b
            self.setStyleSheet("background-color: transparent;\n")
            self.red_blink_timer.stop()

    def show_err_label(self):
        pass
        # # Получаем координаты поля ввода относительно диалогового окна
        # rect = self.geometry()
        # pos = self.mapTo(self, rect.topRight())
        # self.err_label = QLabel('Invalid value, valid (0...255)', self.parent())
        # self.err_label.setStyleSheet("color: #fe2d2d; background-color: #200000; padding: 3px;\n")
        # # self.err_label.setFixedSize(190, 12)
        # self.err_label.move(pos.x() - 150, pos.y() - 15)
        # self.err_label.show()
        # # Устанавливаем задержку в 2 секунды и затем удаляем метку
        # QTimer.singleShot(3000, self.err_label.deleteLater)


class AqPortGatewayLineEdit(AqSlaveIdGatewayLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.min_limit = 0
        self.max_limit = 65535
        self.max_str_len = 5


def zero_fill_str(string, size):
    for count in range(size - len(string)):
        string += '\x00'

    return string
