import datetime
import struct
import socket
import re
import binascii
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMenu, QTreeView

from AQ_TreeViewDelegates import AQ_NameTreeDelegate, AQ_ValueTreeDelegate
from custom_window_templates import AQ_wait_progress_bar_widget, AQ_have_error_widget
from pymodbus.client.tcp import ModbusTcpClient
from pymodbus.client.serial import ModbusSerialClient
from AQ_communication_func import is_valid_ip, write_parameter



class AQ_TreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        name_delegate = AQ_NameTreeDelegate(self)
        self.setItemDelegateForColumn(0, name_delegate)
        value_delegate = AQ_ValueTreeDelegate(self)
        self.setItemDelegateForColumn(1, value_delegate)

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

    def setModel(self, model):
        super().setModel(model)
        # Получение количества колонок в модели
        column_count = model.columnCount()
        for column in range(column_count):
            self.setColumnWidth(column, 200)

        root = model.invisibleRootItem()
        self.traverse_items_show_delegate(root)

    def traverse_items_show_delegate(self, item):
        for row in range(item.rowCount()):
            child_item = item.child(row)
            parameter_attributes = child_item.data(Qt.UserRole)
            if parameter_attributes is not None:
                if parameter_attributes.get('is_catalog', 0) == 1:
                    self.traverse_items_show_delegate(child_item)
                else:
                    index = self.model().index(row, 1, item.index())
                    self.openPersistentEditor(index)

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

                                            QMenu::item:disabled {
                                                color: #808080; /* Цвет для неактивных действий */
                                            }
                                        """)
                    # Добавляем действие в контекстное меню
                    action_read = context_menu.addAction("Read parameters")
                    # Подключаем обработчик события выбора действия
                    action_read.triggered.connect(lambda: self.model().read_parameter(index))
                    if self.traverse_items_R_Only_catalog_check(item) > 0:
                        action_write = context_menu.addAction("Write parameters")
                        # Подключаем обработчик события выбора действия
                        action_write.triggered.connect(lambda: self.model().write_parameter(index))
                    # # Показываем контекстное меню
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

                                            QMenu::item:disabled {
                                                color: #808080; /* Цвет для неактивных действий */
                                            }
                                        """)
                    # Добавляем действие в контекстное меню
                    action_read = context_menu.addAction("Read parameter")
                    # Подключаем обработчик события выбора действия
                    action_read.triggered.connect(lambda: self.model().read_parameter(index))
                    if not (cat_or_param_attributes.get("R_Only", 0) == 1 and cat_or_param_attributes.get("W_Only", 0) == 0):
                        action_write = context_menu.addAction("Write parameter")
                        # Подключаем обработчик события выбора действия
                        action_write.triggered.connect(lambda: self.model().write_parameter(index))

                    # Показываем контекстное меню
                    context_menu.exec_(event.globalPos())
        else:
            # Если индекс недействителен, вызывается обработчик события контекстного меню по умолчанию
            super().contextMenuEvent(event)

    def show_have_error_label(self):
        # Получаем координаты поля ввода относительно диалогового окна
        self.have_err_widget = AQ_have_error_widget("<html>Writing is not possible.<br>One or more parameters<br>\
                                                        have incorrect values<html>", self.parent)
        self.have_err_widget.move(self.parent.width() // 2 - self.have_err_widget.width() // 2,
                                  self.parent.height() // 3 - self.have_err_widget.height() // 2)
        self.have_err_widget.show()
        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.have_err_widget.deleteLater)

    def show_read_error_label(self):
        # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
        self.read_err_widget = AQ_have_error_widget("<html>Failed to read value.<br>The device is offline, connect<br>\
                                                        the device and try again<html>", self.parent)
        self.read_err_widget.move(self.parent.width() // 2 - self.read_err_widget.width() // 2,
                                  self.parent.height() // 3 - self.read_err_widget.height() // 2)
        self.read_err_widget.show()
        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.read_err_widget.deleteLater)

    def show_write_error_label(self):
        # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
        self.write_err_widget = AQ_have_error_widget("<html>Failed to write value.<br>The device is offline, connect<br>\
                                                        the device and try again<html>", self.parent)
        self.write_err_widget.move(self.parent.width() // 2 - self.write_err_widget.width() // 2,
                                   self.parent.height() // 3 - self.write_err_widget.height() // 2)
        self.write_err_widget.show()
        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.write_err_widget.deleteLater)



# import datetime
# import struct
# import socket
# import re
# import binascii
# from PyQt5.QtGui import QColor
# from PyQt5.QtCore import Qt, QTimer
# from PyQt5.QtWidgets import QMenu, QTreeView
#
# from AQ_tree_view_delegates import AQ_NameTreeDelegate, AQ_ValueTreeDelegate
# from custom_window_templates import AQ_wait_progress_bar_widget, AQ_have_error_widget
# from pymodbus.client.tcp import ModbusTcpClient
# from pymodbus.client.serial import ModbusSerialClient
# from AQ_communication_func import is_valid_ip, read_parameter, write_parameter
#
#
#
# class AQ_TreeView(QTreeView):
#     def __init__(self, dev_index, device_tree, address, parent=None):
#         super().__init__(parent)
#         self.parent = parent
#         self.dev_index = dev_index
#         self.dev_address = address
#         name_delegate = AQ_NameTreeDelegate(self)
#         self.setItemDelegateForColumn(0, name_delegate)
#         value_delegate = AQ_ValueTreeDelegate(self)
#         self.setItemDelegateForColumn(1, value_delegate)
#         self.setModel(device_tree)
#         self.setGeometry(250, 2, parent.width() - 252,
#                          parent.height() - 4)
#         # Получение количества колонок в модели
#         column_count = device_tree.columnCount()
#         for column in range(column_count):
#             self.setColumnWidth(column, 200)
#         self.setStyleSheet("""
#                             QTreeView {
#                                 border: 1px solid #9ef1d3;
#                                 color: #D0D0D0;
#                             }
#
#                             QTreeView::item {
#                                 border: 1px solid #2b2d30;
#                             }
#
#                             QHeaderView::section {
#                                 border: 1px solid #1e1f22;
#                                 color: #D0D0D0;
#                                 background-color: #2b2d30;
#                                 padding-left: 6px;
#                             }
#                             QTreeView QScrollBar {
#                                 background-color: #F0F0F0;
#                                 width: 10px; }
#                         """)
#
#     def traverse_items_show_delegate(self, item):
#         for row in range(item.rowCount()):
#             child_item = item.child(row)
#             parameter_attributes = child_item.data(Qt.UserRole)
#             if parameter_attributes is not None:
#                 if parameter_attributes.get('type', '') == 'enum':
#                     if parameter_attributes.get('W_Only', 0) == 1:
#                         # Получаем индекс элемента и открываем для него постоянный редактор
#                         index = self.model().index(row, 1, item.index())
#                         if index.isValid():
#                             self.openPersistentEditor(index)
#                     else:
#                         index = self.model().index(row, 1, item.index())
#                         if index.isValid():
#                             item_cur_value = self.model().itemFromIndex(index)
#                             item_cur_value.setFlags(item_cur_value.flags() & ~Qt.ItemIsEditable)
#                             # self.setValue(1, index)
#                 elif parameter_attributes.get('type', '') == 'unsigned' or \
#                         parameter_attributes.get('type', '') == 'signed' or \
#                         parameter_attributes.get('type', '') == 'string' or \
#                         parameter_attributes.get('type', '') == 'float':
#                     index = self.model().index(row, 1, item.index())
#                     if not (parameter_attributes.get('R_Only', 0) == 1 and parameter_attributes.get('W_Only', 0) == 0):
#                         if index.isValid():
#                             self.openPersistentEditor(index)
#                     else:
#                         if index.isValid():
#                             item_cur_value = self.model().itemFromIndex(index)
#                             item_cur_value.setFlags(item_cur_value.flags() & ~Qt.ItemIsEditable)
#                             item_cur_value.setForeground(QColor("#909090"))
#             if child_item is not None:
#                 self.traverse_items_show_delegate(child_item)
#
#     def traverse_items_R_Only_catalog_check(self, item):
#         write_flag = 0
#         for row in range(item.rowCount()):
#             child_item = item.child(row)
#             parameter_attributes = child_item.data(Qt.UserRole)
#             if parameter_attributes is not None:
#                 if not (parameter_attributes.get('R_Only', 0) == 1 and parameter_attributes.get('W_Only', 0) == 0):
#                     write_flag += 1
#             if child_item is not None:
#                 write_flag += self.traverse_items_R_Only_catalog_check(child_item)
#
#         return write_flag
#
#     def setLineColor(self, index, color):
#         delegate_for_column = self.itemDelegateForColumn(0)
#         delegate_for_column.set_item_color(index, QColor(color))
#         # Також встановлюємо підсвітку відповідних каталогів
#         catalog_index = index.parent()
#         self.travers_up_set_cat_line_color(catalog_index, color)
#
#     def travers_up_set_cat_line_color(self, cat_index, color):
#         if cat_index.isValid():
#             delegate_for_column = self.itemDelegateForColumn(0)
#             parent_index = cat_index.parent()
#             have_changed = self.travers_have_changed_check(cat_index)
#             have_error = self.travers_have_error_check(cat_index)
#             if have_changed > 0 or have_error > 0:
#                 if have_error > 0:
#                     delegate_for_column.set_item_color(cat_index, QColor('#9d4d4f'))
#                     self.travers_up_set_cat_line_color(parent_index, '#9d4d4f')
#                 else:
#                     delegate_for_column.set_item_color(cat_index, QColor('#429061'))
#                     self.travers_up_set_cat_line_color(parent_index, '#429061')
#             else:
#                 delegate_for_column.set_item_color(cat_index, QColor(color))
#                 self.travers_up_set_cat_line_color(parent_index, color)
#
#     def travers_have_changed_check(self, cat_index):
#         delegate_for_column = self.itemDelegateForColumn(1)  # Делегат другої колонки зі значеннями
#         have_changed = 0
#         row_count = self.model().rowCount(cat_index)
#         for row in range(row_count):
#             child_index = self.model().index(row, 0, cat_index)  # Первый столбец
#             next_column_index = child_index.sibling(child_index.row(), child_index.column() + 1) # Второй столбец
#             if delegate_for_column.changed_dict.get(next_column_index, False) == True:
#                 have_changed += 1
#             # Если у текущего дочернего индекса есть дочерние элементы, рекурсивно обойдем их
#             if self.model().hasChildren(child_index):
#                 have_changed += self.travers_have_changed_check(child_index)
#
#         return have_changed
#
#     def travers_have_error_check(self, cat_index):
#         delegate_for_column = self.itemDelegateForColumn(1)  # Делегат другої колонки зі значеннями
#         have_error = 0
#         row_count = self.model().rowCount(cat_index)
#         for row in range(row_count):
#             child_index = self.model().index(row, 0, cat_index)  # Первый столбец
#             next_column_index = child_index.sibling(child_index.row(), child_index.column() + 1) # Второй столбец
#             if delegate_for_column.error_dict.get(next_column_index, False) == True:
#                 have_error += 1
#             # Если у текущего дочернего индекса есть дочерние элементы, рекурсивно обойдем их
#             if self.model().hasChildren(child_index):
#                 have_error += self.travers_have_error_check(child_index)
#
#         return have_error
#
#     def travers_all_tree_have_error_check(self, root_item):
#         have_error = 0
#         for row in range(root_item.rowCount()):
#             child_item = root_item.child(row)
#             child_index = self.model().indexFromItem(child_item)
#             have_error += self.travers_have_error_check(child_index)
#
#         return have_error
#
#     def setValue(self, value, index):
#         delegate_attributes = index.data(Qt.UserRole)
#         # Ставимо мітку що значення змінюється зсередини коду, а не користувачем (для не відображення підсвітки рядка)
#         delegate_for_column = self.itemDelegateForColumn(1)
#         delegate_for_column.set_by_prog_flag(index, True)
#         if delegate_attributes is not None:
#             if delegate_attributes.get('type', '') == 'enum':
#                 enum_strings = delegate_attributes.get('enum_strings', '')
#                 enum_str = enum_strings[value]
#                 if delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0:
#                     self.model().setData(index, enum_str, Qt.DisplayRole)
#                 else:
#                     self.model().setData(index, value, Qt.EditRole)
#             elif delegate_attributes.get('type', '') == 'unsigned' or delegate_attributes.get('type', '') == 'signed' \
#                     or delegate_attributes.get('type', '') == 'string':
#                 if delegate_attributes.get('visual_type', '') == 'ip_format':
#                     value = socket.inet_ntoa(struct.pack('!L', value))
#                 elif delegate_attributes.get('visual_type', '') == 'hex':
#                     mac_address = binascii.hexlify(value).decode('utf-8').upper()
#                     mac_address_with_colons = ':'.join(mac_address[i:i + 2] for i in range(0, len(mac_address), 2))
#                     value = mac_address_with_colons
#                 elif delegate_attributes.get('visual_type', '') == 'bin' and delegate_attributes.get('type', '') == 'unsigned':
#                     par_size = delegate_attributes.get('param_size', 0)
#                     binary_string = format(value, f'0{par_size * 8}b')
#                     grouped_binary_string = ' '.join(
#                         [binary_string[i:i + 4] for i in range(0, len(binary_string), 4)])
#                     # Создаем объект BitArray из байтового массива
#                     value = grouped_binary_string
#                 if delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0:
#                     self.model().setData(index, value, Qt.DisplayRole)
#                 else:
#                     self.model().setData(index, value, Qt.EditRole)
#             elif delegate_attributes.get('type', '') == 'float':
#                 # Округлюємо до 7 знака після коми
#                 value = round(value, 7)
#                 if delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0:
#                     self.model().setData(index, value, Qt.DisplayRole)
#                 else:
#                     self.model().setData(index, value, Qt.EditRole)
#
#             elif delegate_attributes.get('type', '') == 'date_time':
#                 value += datetime.datetime(2000, 1, 1).timestamp()
#                 datetime_obj = datetime.datetime.fromtimestamp(value)
#                 value = datetime_obj.strftime('%d.%m.%Y %H:%M:%S')
#                 if delegate_attributes.get('R_Only', 0) == 1 and delegate_attributes.get('W_Only', 0) == 0:
#                     self.model().setData(index, value, Qt.DisplayRole)
#                 else:
#                     self.model().setData(index, value, Qt.EditRole)
#
#             delegate_for_column.set_item_chandeg_flag(index, False)
#
#
#     def read_value_by_modbus(self, index):
#         try:
#             cat_or_param_attributes = index.data(Qt.UserRole)
#             if cat_or_param_attributes.get('is_catalog', 0) == 1:
#                 return
#             else:
#                 modbus_reg = cat_or_param_attributes.get('modbus_reg', '')
#                 if cat_or_param_attributes.get('type', '') == 'enum':
#                     if cat_or_param_attributes.get('param_size', 0) > 16:
#                         reg_count = 2
#                         byte_size = 4
#                     else:
#                         reg_count = 1
#                         byte_size = 1
#                 else:
#                     byte_size = cat_or_param_attributes.get('param_size', 0)
#                     if byte_size < 2:
#                         reg_count = 1
#                     else:
#                         reg_count = byte_size // 2
#
#             if is_valid_ip(self.dev_address):
#                 ip = self.dev_address
#                 client = ModbusTcpClient(ip)
#                 slave_id = 1
#             else:
#                 # Регулярний вираз для розбору адреси ком-порту
#                 pattern = r'(\d+)\s*\((\w+)\)'
#                 match = re.match(pattern, self.dev_address)
#
#                 if match:
#                     slave_id = int(match.group(1))
#                     selected_port = match.group(2)
#                 else:
#                     print("Pattern not found in the string")
#                 client = ModbusSerialClient(method='rtu', port=selected_port, baudrate=9600)
#             param_type = cat_or_param_attributes.get('type', '')
#             param_value = read_parameter(client, slave_id, modbus_reg, reg_count, param_type, byte_size)
#
#             next_column_index = index.sibling(index.row(), index.column() + 1)
#             self.setValue(param_value, next_column_index)
#             self.setLineColor(index, '#1e1f22')
#         except Exception as e:
#             print(f"Error occurred: {str(e)}")
#             self.show_read_error_label()
#
#
#     def read_catalog_by_modbus(self, index, show_prorgess_flag):
#         try:
#             cat_or_param_attributes = index.data(Qt.UserRole)
#             if show_prorgess_flag == 1:
#                 self.wait_widget = AQ_wait_progress_bar_widget('Reading current values...', self.parent)
#                 self.wait_widget.setGeometry(self.parent.width() // 2 - 170, self.parent.height() // 4, 340, 50)
#
#             if cat_or_param_attributes.get('is_catalog', 0) == 0:
#                 return
#             else:
#                 item_cur_cat = self.model().itemFromIndex(index)
#                 if show_prorgess_flag == 1:
#                     max_value = 100  # Максимальное значение для прогресс-бара
#                     row_count = item_cur_cat.rowCount()
#                     step_value = max_value // row_count
#
#                 for row in range(item_cur_cat.rowCount()):
#                     child_item = item_cur_cat.child(row)
#                     child_index = self.model().index(row, 0, index)
#                     child_attributes = child_item.data(Qt.UserRole)
#                     if child_attributes is not None:
#                         if child_attributes.get('is_catalog', 0) == 1:
#                             self.read_catalog_by_modbus(child_index, 0)
#                         else:
#                             if is_valid_ip(self.dev_address):
#                                 ip = self.dev_address
#                                 client = ModbusTcpClient(ip)
#                                 slave_id = 1
#                             else:
#                                 # Регулярний вираз для розбору адреси ком-порту
#                                 pattern = r'(\d+)\s*\((\w+)\)'
#                                 match = re.match(pattern, self.dev_address)
#
#                                 if match:
#                                     slave_id = int(match.group(1))
#                                     selected_port = match.group(2)
#                                 else:
#                                     print("Pattern not found in the string")
#                                 client = ModbusSerialClient(method='rtu', port=selected_port, baudrate=9600)
#                             param_type = child_attributes.get('type', '')
#                             modbus_reg = child_attributes.get('modbus_reg', '')
#                             if child_attributes.get('type', '') == 'enum':
#                                 if child_attributes.get('param_size', 0) > 16:
#                                     reg_count = 2
#                                     byte_size = 4
#                                 else:
#                                     reg_count = 1
#                                     byte_size = 1
#                             else:
#                                 byte_size = child_attributes.get('param_size', 0)
#                                 if byte_size < 2:
#                                     reg_count = 1
#                                 else:
#                                     reg_count = byte_size // 2
#
#                             param_value = read_parameter(client, slave_id, modbus_reg, reg_count, param_type, byte_size)
#
#                             next_column_index = child_index.sibling(child_index.row(), child_index.column() + 1)
#                             self.setValue(param_value, next_column_index)
#                             self.setLineColor(child_index, '#1e1f22')
#
#                     if show_prorgess_flag == 1:
#                         self.wait_widget.progress_bar.setValue((row + 1) * step_value)
#
#                 if show_prorgess_flag == 1:
#                     self.wait_widget.progress_bar.setValue(max_value)
#                     self.wait_widget.hide()
#                     self.wait_widget.deleteLater()
#                 return 'ok'
#         except Exception as e:
#             print(f"Error occurred: {str(e)}")
#             if hasattr(self, 'wait_widget'):
#                 self.wait_widget.hide()
#                 self.wait_widget.deleteLater()
#             self.show_read_error_label()
#             return 'read_error'
#
#
#     def read_all_tree_by_modbus(self, item):
#         self.wait_widget = AQ_wait_progress_bar_widget('Reading current values...', self.parent)
#         self.wait_widget.setGeometry(self.parent.width() // 2 - 170, self.parent.height() // 4, 340, 50)
#
#         max_value = 100  # Максимальное значение для прогресс-бара
#         row_count = item.rowCount()
#         step_value = max_value // row_count
#         for row in range(item.rowCount()):
#             index = self.model().index(row, 0, item.index())
#             result = self.read_catalog_by_modbus(index, 0)
#             if result == 'read_error':
#                 self.wait_widget.hide()
#                 self.wait_widget.deleteLater()
#                 return
#             self.wait_widget.progress_bar.setValue((row + 1) * step_value)
#
#         self.wait_widget.progress_bar.setValue(max_value)
#         self.wait_widget.hide()
#         self.wait_widget.deleteLater()
#
#     def write_value_by_modbus(self, index):
#         try:
#             cat_or_param_attributes = index.data(Qt.UserRole)
#             if cat_or_param_attributes.get('is_catalog', 0) == 1:
#                 return
#             else:
#                 modbus_reg = cat_or_param_attributes.get('modbus_reg', '')
#                 if cat_or_param_attributes.get('type', '') == 'enum':
#                     if cat_or_param_attributes.get('param_size', 0) > 16:
#                         reg_count = 2
#                         byte_size = 4
#                     else:
#                         reg_count = 1
#                         byte_size = 1
#                 else:
#                     byte_size = cat_or_param_attributes.get('param_size', 0)
#                     if byte_size < 2:
#                         reg_count = 1
#                     else:
#                         reg_count = byte_size // 2
#
#             if is_valid_ip(self.dev_address):
#                 ip = self.dev_address
#                 client = ModbusTcpClient(ip)
#                 slave_id = 1
#             else:
#                 # Регулярний вираз для розбору адреси ком-порту
#                 pattern = r'(\d+)\s*\((\w+)\)'
#                 match = re.match(pattern, self.dev_address)
#
#                 if match:
#                     slave_id = int(match.group(1))
#                     selected_port = match.group(2)
#                 else:
#                     print("Pattern not found in the string")
#                 client = ModbusSerialClient(method='rtu', port=selected_port, baudrate=9600)
#
#             param_type = cat_or_param_attributes.get('type', '')
#             visual_type = cat_or_param_attributes.get('visual_type', '')
#
#             next_column_index = index.sibling(index.row(), index.column() + 1)
#             delegate_for_column = self.itemDelegateForColumn(1)
#             have_error = delegate_for_column.error_dict.get(next_column_index, False)
#             if have_error is False:
#                 value = self.model().data(next_column_index, Qt.EditRole)
#                 write_parameter(client, slave_id, modbus_reg, param_type, visual_type, byte_size, value)
#                 delegate_for_column.set_item_chandeg_flag(next_column_index, False)
#                 self.setLineColor(index, '#1e1f22')
#         except Exception as e:
#             print(f"Error occurred: {str(e)}")
#             self.show_write_error_label()
#
#
#     def write_catalog_by_modbus(self, index, show_prorgess_flag):
#         try:
#             cat_or_param_attributes = index.data(Qt.UserRole)
#             if show_prorgess_flag == 1:
#                 self.wait_widget = AQ_wait_progress_bar_widget('Writing new values...', self.parent)
#                 self.wait_widget.setGeometry(self.parent.width() // 2 - 170, self.parent.height() // 4, 340, 50)
#
#             if cat_or_param_attributes.get('is_catalog', 0) == 0:
#                 return
#             else:
#                 item_cur_cat = self.model().itemFromIndex(index)
#                 if show_prorgess_flag == 1:
#                     max_value = 100  # Максимальное значение для прогресс-бара
#                     row_count = item_cur_cat.rowCount()
#                     step_value = max_value // row_count
#
#                 for row in range(item_cur_cat.rowCount()):
#                     child_item = item_cur_cat.child(row)
#                     child_index = self.model().index(row, 0, index)
#                     child_attributes = child_item.data(Qt.UserRole)
#                     if child_attributes is not None:
#                         if child_attributes.get('is_catalog', 0) == 1:
#                             self.write_catalog_by_modbus(child_index, 0)
#                         elif not (child_attributes.get('R_Only', 0) == 1 and child_attributes.get('W_Only', 0) == 0):
#                             if is_valid_ip(self.dev_address):
#                                 ip = self.dev_address
#                                 client = ModbusTcpClient(ip)
#                                 slave_id = 1
#                             else:
#                                 # Регулярний вираз для розбору адреси ком-порту
#                                 pattern = r'(\d+)\s*\((\w+)\)'
#                                 match = re.match(pattern, self.dev_address)
#
#                                 if match:
#                                     slave_id = int(match.group(1))
#                                     selected_port = match.group(2)
#                                 else:
#                                     print("Pattern not found in the string")
#                                 client = ModbusSerialClient(method='rtu', port=selected_port, baudrate=9600)
#                             modbus_reg = child_attributes.get('modbus_reg', '')
#                             if child_attributes.get('type', '') == 'enum':
#                                 if child_attributes.get('param_size', 0) > 16:
#                                     reg_count = 2
#                                     byte_size = 4
#                                 else:
#                                     reg_count = 1
#                                     byte_size = 1
#                             else:
#                                 byte_size = child_attributes.get('param_size', 0)
#                                 if byte_size < 2:
#                                     reg_count = 1
#                                 else:
#                                     reg_count = byte_size // 2
#
#                             param_type = child_attributes.get('type', '')
#                             visual_type = child_attributes.get('visual_type', '')
#
#                             next_column_index = child_index.sibling(child_index.row(), child_index.column() + 1)
#                             delegate_for_column = self.itemDelegateForColumn(1)
#                             if delegate_for_column.changed_dict.get(next_column_index, False) == True:
#                                 value = self.model().data(next_column_index, Qt.EditRole)
#
#                                 write_parameter(client, slave_id, modbus_reg, param_type, visual_type, byte_size, value)
#                                 delegate_for_column.set_item_chandeg_flag(next_column_index, False)
#                                 self.setLineColor(child_index, '#1e1f22')
#
#                     if show_prorgess_flag == 1:
#                         self.wait_widget.progress_bar.setValue((row + 1) * step_value)
#
#                 if show_prorgess_flag == 1:
#                     self.wait_widget.progress_bar.setValue(max_value)
#                     self.wait_widget.hide()
#                     self.wait_widget.deleteLater()
#                 return 'ok'
#         except Exception as e:
#             print(f"Error occurred: {str(e)}")
#             if hasattr(self, 'wait_widget'):
#                 self.wait_widget.hide()
#                 self.wait_widget.deleteLater()
#             self.show_write_error_label()
#             return 'write_error'
#
#     def write_all_tree_by_modbus(self, item):
#         self.wait_widget = AQ_wait_progress_bar_widget('Writing new values...', self.parent)
#         self.wait_widget.setGeometry(self.parent.width() // 2 - 170, self.parent.height() // 4, 340, 50)
#
#         max_value = 100  # Максимальное значение для прогресс-бара
#         row_count = item.rowCount()
#         step_value = max_value // row_count
#         for row in range(item.rowCount()):
#             index = self.model().index(row, 0, item.index())
#             result = self.write_catalog_by_modbus(index, 0)
#             if result == 'write_error':
#                 self.wait_widget.hide()
#                 self.wait_widget.deleteLater()
#                 return
#             self.wait_widget.progress_bar.setValue((row + 1) * step_value)
#
#         self.wait_widget.progress_bar.setValue(max_value)
#         self.wait_widget.hide()
#         self.wait_widget.deleteLater()
#
#     def contextMenuEvent(self, event):
#         index = self.indexAt(event.pos())
#         if index.isValid() and index.column() == 0:
#             # Получаем элемент модели по индексу
#             item = self.model().itemFromIndex(index)
#             cat_or_param_attributes = index.data(Qt.UserRole)
#             if item:
#                 if cat_or_param_attributes.get('is_catalog', 0) == 1:
#                     # Создаем контекстное меню
#                     context_menu = QMenu(self)
#                     context_menu.setStyleSheet("""
#                                             QMenu {
#                                                 color: #D0D0D0;
#                                             }
#
#                                             QMenu::item:selected {
#                                                 background-color: #3a3a3a;
#                                                 color: #FFFFFF;
#                                             }
#
#                                             QMenu::item:disabled {
#                                                 color: #808080; /* Цвет для неактивных действий */
#                                             }
#                                         """)
#                     # Добавляем действие в контекстное меню
#                     action_read = context_menu.addAction("Read parameters")
#                     # Подключаем обработчик события выбора действия
#                     action_read.triggered.connect(lambda: self.read_catalog_by_modbus(index, 1))
#                     if self.traverse_items_R_Only_catalog_check(item) > 0:
#                         action_write = context_menu.addAction("Write parameters")
#                         have_error = self.travers_have_error_check(index)
#                         if have_error > 0:
#                             action_write.setDisabled(True)
#                         # Подключаем обработчик события выбора действия
#                         action_write.triggered.connect(lambda: self.write_catalog_by_modbus(index, 1))
#                     # Показываем контекстное меню
#                     context_menu.exec_(event.globalPos())
#                 else:
#                     # Создаем контекстное меню
#                     context_menu = QMenu(self)
#                     context_menu.setStyleSheet("""
#                                             QMenu {
#                                                 color: #D0D0D0;
#                                             }
#
#                                             QMenu::item:selected {
#                                                 background-color: #3a3a3a;
#                                                 color: #FFFFFF;
#                                             }
#
#                                             QMenu::item:disabled {
#                                                 color: #808080; /* Цвет для неактивных действий */
#                                             }
#                                         """)
#                     # Добавляем действие в контекстное меню
#                     action_read = context_menu.addAction("Read parameter")
#                     # Подключаем обработчик события выбора действия
#                     action_read.triggered.connect(lambda: self.read_value_by_modbus(index))
#                     if not (cat_or_param_attributes.get("R_Only", 0) == 1 and cat_or_param_attributes.get("W_Only", 0) == 0):
#                         action_write = context_menu.addAction("Write parameter")
#                         delegate_for_column = self.itemDelegateForColumn(1)
#                         next_column_index = index.sibling(index.row(), index.column() + 1)
#                         have_error = delegate_for_column.error_dict.get(next_column_index, False)
#                         if have_error is True:
#                             action_write.setDisabled(True)
#                         # Подключаем обработчик события выбора действия
#                         action_write.triggered.connect(lambda: self.write_value_by_modbus(index))
#
#                     # Показываем контекстное меню
#                     context_menu.exec_(event.globalPos())
#         else:
#             # Если индекс недействителен, вызывается обработчик события контекстного меню по умолчанию
#             super().contextMenuEvent(event)
#
#     def show_have_error_label(self):
#         # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
#         self.have_err_widget = AQ_have_error_widget("<html>Writing is not possible.<br>One or more parameters<br>\
#                                                         have incorrect values<html>", self.parent)
#         self.have_err_widget.move(self.parent.width() // 2 - self.have_err_widget.width() // 2,
#                                   self.parent.height() // 3 - self.have_err_widget.height() // 2)
#         self.have_err_widget.show()
#         # Запускаем таймер на 4 секунды, чтобы скрыть плашку
#         QTimer.singleShot(4000, self.have_err_widget.deleteLater)
#
#     def show_read_error_label(self):
#         # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
#         self.read_err_widget = AQ_have_error_widget("<html>Failed to read value.<br>The device is offline, connect<br>\
#                                                         the device and try again<html>", self.parent)
#         self.read_err_widget.move(self.parent.width() // 2 - self.read_err_widget.width() // 2,
#                                   self.parent.height() // 3 - self.read_err_widget.height() // 2)
#         self.read_err_widget.show()
#         # Запускаем таймер на 4 секунды, чтобы скрыть плашку
#         QTimer.singleShot(4000, self.read_err_widget.deleteLater)
#
#     def show_write_error_label(self):
#         # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
#         self.write_err_widget = AQ_have_error_widget("<html>Failed to write value.<br>The device is offline, connect<br>\
#                                                         the device and try again<html>", self.parent)
#         self.write_err_widget.move(self.parent.width() // 2 - self.write_err_widget.width() // 2,
#                                    self.parent.height() // 3 - self.write_err_widget.height() // 2)
#         self.write_err_widget.show()
#         # Запускаем таймер на 4 секунды, чтобы скрыть плашку
#         QTimer.singleShot(4000, self.write_err_widget.deleteLater)