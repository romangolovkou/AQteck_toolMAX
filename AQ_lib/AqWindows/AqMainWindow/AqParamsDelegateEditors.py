import binascii
import datetime
import ipaddress
import socket
import struct
import re

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QComboBox, QLineEdit, QLabel


class AqTreeLineEdit(QLineEdit):
    edit_done_signal = Signal(object)

    def __init__(self, param_attributes, parent=None):
        super().__init__(parent)
        self.min_limit = param_attributes.get('min_limit', None)
        self.max_limit = param_attributes.get('max_limit', None)
        self.manager_item_handler = None
        self.setStyleSheet(
            "border: none; color: #D0D0D0; background-color: transparent; \n")  # Задаем цветную границу и цвет шрифта
        self.red_blink_timer = QTimer()
        self.red_blink_timer.setInterval(40)
        self.red_blink_timer.timeout.connect(self.err_blink)
        self.anim_cnt = 0
        self.color_code = 0x2b  # Берется из цвета background-color, первые два символа после # соответствуют RED
        self.err_label = None
        if param_attributes.get('R_Only', 0) == 1 and param_attributes.get('W_Only', 0) == 0:
            self.setReadOnly(True)
            self.setStyleSheet("border: none; color: #909090; background-color: transparent; \n")
        else:
            self.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent; \n")
            self.textChanged.connect(self.line_edit_changed_update_value)

        self.returnPressed.connect(lambda: self.edit_done_signal.emit(self.manager_item_handler.get_sourse_item()))

    def line_edit_changed_update_value(self, text):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        if text != '' and text is not None:
            value = int(text)
        else:
            value = None
        self.save_new_value(value)

    def set_manager_item_handler(self, manager_item_handler):
        self.manager_item_handler = manager_item_handler

    def enter_pressed(self):
        self.edit_done_signal.emit(self.manager_item_handler.get_sourse_item())

    def save_new_value(self, value):
        self.manager_item_handler.save_new_value(value)

    def set_value(self, value):
        if value is None:
            self.setText('')
        else:
            self.setText(str(value))

    def verify(self, value=None, show_err=False):
        if value is None:
            if self.text() != '' and self.text() is not None:
                try:
                    value = int(self.text())
                except:
                    value = str(self.text())
            else:
                return None

        if self.min_limit is not None or self.max_limit is not None:
            if value != '':
                value = int(value)
                if value < self.min_limit or value > self.max_limit:
                    if show_err:
                        self.red_blink_timer.start()
                        if self.err_label is None:
                            show_err_label(self)
                    return False
                else:
                    if self.err_label is not None:
                        try:
                            self.err_label.hide()
                            self.err_label.deleteLater()
                            self.err_label = None
                        except:
                            pass

                    return True

    def make_err_label_none(self):
        self.err_label = None

    def err_blink(self):
        if self.anim_cnt < 34:
            self.anim_cnt += 1
            if self.anim_cnt < 18:
                self.color_code = self.color_code + 0xA
            else:
                self.color_code = self.color_code - 0xA

            hex_string = format(self.color_code, 'x')
            self.setStyleSheet("border: none; color: #D0D0D0; background-color: #{}2d30;\n".format(hex_string))
        else:
            self.anim_cnt = 0
            self.color_code = 0x2b
            self.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent;\n")
            self.red_blink_timer.stop()

    def setText(self, text):
        if not self.hasFocus():
            super().setText(text)

    def focusInEvent(self, event):
        # Викликається при отриманні єдітором фокусу
        if self.manager_item_handler is not None:
            self.manager_item_handler.set_blocked(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        # Викликається при втраті єдітором фокусу
        if self.manager_item_handler is not None:
            self.manager_item_handler.set_blocked(False)
        super().focusOutEvent(event)


class AqEnumTreeComboBox(QComboBox):
    edit_done_signal = Signal(object)

    def __init__(self, param_attributes, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.view().setStyleSheet("color: #D0D0D0; background-color: #1e1f22;")
        self.setStyleSheet("QComboBox { border: 0px solid #D0D0D0; color: #D0D0D0; background-color: #16191d;}")
        # Отключение обработчика события колеса мыши
        self.wheelEvent = lambda event: event.ignore()
        self.manager_item_handler = None
        self.enum_str_dict = param_attributes.get('enum_strings', '')
        enum_strings = self.enum_str_dict.values()
        enum_strings = list(enum_strings)
        for i in range(len(enum_strings)):
            enum_str = enum_strings[i]
            self.addItem(enum_str)

        self.currentIndexChanged.connect(self.updateIndex)
        self.activated.connect(self.popupActivated)
        self.highlighted.connect(self.popupOpened)

    def updateIndex(self, index):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        string = self.itemText(index)
        key = self.get_key_by_value(self.enum_str_dict, string)
        self.save_new_value(key)
        self.edit_done_signal.emit(self.manager_item_handler.get_sourse_item())

    def popupActivated(self):
        self.manager_item_handler.set_blocked(False)
        print('unblock')

    def set_manager_item_handler(self, manager_item_handler):
        self.manager_item_handler = manager_item_handler

    def save_new_value(self, value):
        self.manager_item_handler.save_new_value(value)

    def set_value(self, value):
        if not self.hasFocus():
            string = self.enum_str_dict.get(value, '')
            self.setCurrentText(string)
            # self.setCurrentIndex(value)

    def get_key_by_value(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None  # Возвращаем None, если объект не найден

    def focusInEvent(self, event):
        # Викликається при отриманні єдітором фокусу
        super().focusInEvent(event)
        self.manager_item_handler.set_blocked(True)

        print('block')

    def popupOpened(self):
        self.manager_item_handler.set_blocked(True)

        print('block')

    def focusOutEvent(self, event):
        # Викликається при втраті єдітором фокусу
        super().focusOutEvent(event)
        if not self.view().isVisible():
            self.manager_item_handler.set_blocked(False)
            print('unblock')




class AqEnumROnlyTreeLineEdit(AqTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)
        self.enum_str_dict = param_attributes.get('enum_strings', '')

    def set_value(self, value):
        self.setText(self.enum_str_dict.get(value, ''))


class AqUintTreeLineEdit(AqTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)
        self.visual_type = param_attributes.get('visual_type', '')
        self.param_size = param_attributes.get('param_size', 0)

    def set_value(self, value):
        if self.visual_type == 'hex':
            mac_address = binascii.hexlify(value).decode('utf-8').upper()
            mac_address_with_colons = ':'.join(mac_address[i:i + 2] for i in range(0, len(mac_address), 2))
            value = mac_address_with_colons
        elif self.visual_type == 'bin':
            binary_string = format(value, f'0{self.param_size * 8}b')
            grouped_binary_string = ' '.join(
                [binary_string[i:i + 4] for i in range(0, len(binary_string), 4)])
            # Создаем объект BitArray из байтового массива
            value = grouped_binary_string

        self.setText(str(value))

    def keyPressEvent(self, event):
        if self.isReadOnly() is False:
            key = event.key()
            if key == Qt.Key_Left:
                cursor_position = self.cursorPosition()
                self.setCursorPosition(cursor_position - 1)
                return
            elif key == Qt.Key_Right:
                cursor_position = self.cursorPosition()
                self.setCursorPosition(cursor_position + 1)
                return
            elif key == Qt.Key_Backspace:
                self.backspace()
                str_copy = self.text()
                self.verify(str_copy)
                return
            elif key == Qt.Key_Return:
                super().keyPressEvent(event)
                return

            cursor_position = self.cursorPosition()
            text = event.text()
            if not text.isdigit():
                # Якщо не цифра
                return
            # Если цифра
            else:
                if self.hasSelectedText():
                    self.backspace()

                str_copy = self.text()
                str_copy = str_copy[:cursor_position] + text + str_copy[cursor_position:]
                user_data = int(str_copy)  # Преобразуем подстроку в целое число

                # if self.min_limit is not None:
                #     if user_data < self.min_limit:
                #         self.red_blink_timer.start()
                #         show_err_label(self)
                # if self.max_limit is not None:
                #     if user_data > self.max_limit:
                #         self.red_blink_timer.start()
                #         show_err_label(self)
                # if self.min_limit is not None or self.max_limit is not None:
                #     if user_data < self.min_limit or user_data > self.max_limit:
                #         self.red_blink_timer.start()
                #         show_err_label(self)
                #     else:
                #         if hasattr(self, 'err_label'):
                #             self.err_label.deleteLater()
                self.verify(user_data, show_err=True)

            super().keyPressEvent(event)


class AqIpTreeLineEdit(AqTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)
        self.min_limit = 0
        self.max_limit = 255
        self.setMaxLength(15)  # Устанавливаем максимальную длину IP-адреса (15 символов)

    def line_edit_changed_update_value(self, text):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        if self.is_valid_ip(text):
            # Разделяем IP-адрес на октеты
            octets = text.split('.')
            # Преобразуем каждый октет в числовое значение
            int_octets = [int(octet) for octet in octets]
            # Получаем 32-битное целое число из октетов
            ip_as_integer = (int_octets[0] << 24) | (int_octets[1] << 16) | (int_octets[2] << 8) | int_octets[3]
        else:
            ip_as_integer = None

        self.save_new_value(ip_as_integer)

    def is_valid_ip(self, address):
        try:
            ipaddress.ip_address(address)
            return True
        except ValueError:
            return False

    def set_value(self, value):
        value = socket.inet_ntoa(struct.pack('!L', value))
        self.setText(value)

    def keyPressEvent(self, event):
        if self.isReadOnly() is False:
            key = event.key()
            if key == Qt.Key_Left:
                cursor_position = self.cursorPosition()
                self.setCursorPosition(cursor_position - 1)
                return
            elif key == Qt.Key_Right:
                cursor_position = self.cursorPosition()
                if cursor_position == len(self.text()) - 1:
                    left_character = self.text()[cursor_position - 1]
                    if left_character.isdigit() and  self.text().count(".") < 3:
                        self.insert('.')
                self.setCursorPosition(cursor_position + 1)
                return
            elif key == Qt.Key_Backspace:
                cursor_position = self.cursorPosition()
                if cursor_position > 0:
                    if cursor_position == len(self.text()) - 1 and self.text()[cursor_position - 1] == '.' and \
                            self.text()[cursor_position] == '.':
                        self.backspace()
                        self.backspace()
                        return
                    if cursor_position > 1 and \
                            self.text()[cursor_position - 2].isdigit() and \
                            self.text()[cursor_position - 1] == '.':
                        self.setCursorPosition(cursor_position - 1)
                        self.backspace()
                        return
                    self.backspace()
                return
            elif key == Qt.Key_Return:
                super().keyPressEvent(event)
                return

            if self.hasSelectedText():
                self.backspace()

            cursor_position = self.cursorPosition()
            text = event.text()
            if not text.isdigit():
            #Если не цифра
                if text == '.' and self.text().count(".") < 3:
                    if cursor_position == len(self.text()) - 1 and self.text()[cursor_position] == '.':
                        self.insert('.')
                    elif cursor_position < len(self.text()) and self.text()[cursor_position] == '.':
                        self.setCursorPosition(cursor_position + 1)
                    else:
                        self.insert('.')
                elif text == '.' and cursor_position < len(self.text()) and self.text()[cursor_position] == '.':
                    self.setCursorPosition(cursor_position + 1)
                return
            #Если цифра
            elif cursor_position == 0 and self.text().count(".") < 3:
                self.insert(text + '.')
                self.setCursorPosition(1)
                return

            #Лимит на ввод цифры в последнюю тетраду не больше трех
            elif self.text().count(".") > 2 and self.text()[cursor_position - 3:cursor_position].isdigit():
                return
            else: #cursor_position >= 2:
                str_copy = self.text()
                str_copy = str_copy[:cursor_position] + text + str_copy[cursor_position:]
                start_pos = 0
                end_pos = len(str_copy)
                for i in range(cursor_position, -1, -1):
                    if str_copy[i] == '.':
                        start_pos = i + 1
                        break
                for i in range(cursor_position, len(self.text()) + 1, +1):
                    if str_copy[i] == '.':
                        end_pos = i
                        break
                str_tetrada = str_copy[start_pos:end_pos]  # Получаем подстроку
                tetrada = int(str_tetrada)  # Преобразуем подстроку в целое число
                if tetrada < 256 and len(str_tetrada) < 4:
                    if  self.text()[cursor_position - 2:cursor_position].isdigit():
                        if self.text().count(".") < 3:
                            self.insert(text + '.')
                        else:
                            self.insert(text)
                            self.setCursorPosition(cursor_position + 2)
                        return
                else:
                    self.red_blink_timer.start()
                    show_err_label(self)
                    return

            super().keyPressEvent(event)


class AqIntTreeLineEdit(AqTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)

    def line_edit_changed_update_value(self, text):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        if text != '' and text != '-':
            value = int(text)
        else:
            value = None
        self.save_new_value(value)

    def keyPressEvent(self, event):
        if self.isReadOnly() is False:
            key = event.key()
            if key == Qt.Key_Left:
                cursor_position = self.cursorPosition()
                self.setCursorPosition(cursor_position - 1)
                return
            elif key == Qt.Key_Right:
                cursor_position = self.cursorPosition()
                self.setCursorPosition(cursor_position + 1)
                return
            elif key == Qt.Key_Backspace:
                self.backspace()
                str_copy = self.text()
                self.verify(str_copy)
                return
            elif key == Qt.Key_Return:
                super().keyPressEvent(event)
                return

            if self.hasSelectedText():
                self.backspace()

            cursor_position = self.cursorPosition()
            text = event.text()
            if not text.isdigit() and text != '-':
                # Якщо не цифра та не мінус
                return
            # Если цифра
            else:
                str_copy = self.text()
                if text == '-':
                    # Перевірка чи не порожня строка
                    if str_copy.strip():
                        if str_copy[0] == '-':
                            return
                        else:
                            self.setCursorPosition(0)
                            self.insert(text)
                            self.setCursorPosition(cursor_position + 1)
                            str_copy = self.text()
                            user_data = int(str_copy)  # Преобразуем подстроку в целое число
                            # if self.min_limit is not None:
                            #     if user_data < self.min_limit:
                            #         self.red_blink_timer.start()
                            #         show_err_label(self)
                            # if self.max_limit is not None:
                            #     if user_data > self.max_limit:
                            #         self.red_blink_timer.start()
                            #         show_err_label(self)
                            self.verify(user_data, show_err=True)

                            return
                    else:
                        self.setCursorPosition(0)
                        self.insert(text)
                        self.setCursorPosition(1)
                        return

                str_copy = str_copy[:cursor_position] + text + str_copy[cursor_position:]
                user_data = int(str_copy)  # Преобразуем подстроку в целое число
                # if self.min_limit is not None:
                #     if user_data < self.min_limit:
                #         self.red_blink_timer.start()
                #         show_err_label(self)
                # if self.max_limit is not None:
                #     if user_data > self.max_limit:
                #         self.red_blink_timer.start()
                #         show_err_label(self)
                self.verify(user_data, show_err=True)

            super().keyPressEvent(event)


class AqFloatTreeLineEdit(AqTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)

    def line_edit_changed_update_value(self, text):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        if text != '' and text != '-':
            value = float(text)
        else:
            value = None
        self.save_new_value(value)

    def verify(self, value=None, show_err=False):
        if value is None:
            if self.text() != '' and self.text() is not None:
                try:
                    value = int(self.text())
                except:
                    value = str(self.text())
            else:
                return None

        if self.min_limit is not None or self.max_limit is not None:
            if value != '':
                value = float(value)
                if value < self.min_limit or value > self.max_limit:
                    if show_err:
                        self.red_blink_timer.start()
                        if self.err_label is None:
                            show_err_label(self)
                    return False
                else:
                    if self.err_label is not None:
                        try:
                            self.err_label.hide()
                            self.err_label.deleteLater()
                            self.err_label = None
                        except:
                            pass

                    return True

    def keyPressEvent(self, event):
        if self.isReadOnly() is False:
            key = event.key()
            if key == Qt.Key_Left:
                cursor_position = self.cursorPosition()
                self.setCursorPosition(cursor_position - 1)
                return
            elif key == Qt.Key_Right:
                cursor_position = self.cursorPosition()
                self.setCursorPosition(cursor_position + 1)
                return
            elif key == Qt.Key_Backspace:
                self.backspace()
                str_copy = self.text()
                self.verify(str_copy)
                return
            elif key == Qt.Key_Return:
                super().keyPressEvent(event)
                return

            if self.hasSelectedText():
                self.backspace()

            cursor_position = self.cursorPosition()
            text = event.text()
            if not text.isdigit() and text != '-' and text != '.':
                # Якщо не цифра та не мінус
                return
            # Если цифра
            else:
                str_copy = self.text()
                if text == '-':
                    # Перевірка чи не порожня строка
                    if str_copy.strip():
                        if str_copy[0] == '-':
                            return
                        else:
                            self.setCursorPosition(0)
                            self.insert(text)
                            self.setCursorPosition(cursor_position + 1)
                            str_copy = self.text()
                            user_data = float(str_copy)  # Преобразуем подстроку в целое число
                            # if self.min_limit is not None:
                            #     if user_data < self.min_limit:
                            #         self.red_blink_timer.start()
                            #         show_err_label(self)
                            # if self.max_limit is not None:
                            #     if user_data > self.max_limit:
                            #         self.red_blink_timer.start()
                            #         show_err_label(self)
                            self.verify(user_data, show_err=True)

                            return
                    else:
                        self.setCursorPosition(0)
                        self.insert(text)
                        self.setCursorPosition(1)
                        return
                elif text == '.':
                    if '.' in str_copy:
                        return

                str_copy = str_copy[:cursor_position] + text + str_copy[cursor_position:]
                user_data = float(str_copy)  # Преобразуем подстроку в целое число
                # if self.min_limit is not None:
                #     if user_data < self.min_limit:
                #         self.red_blink_timer.start()
                #         show_err_label(self)
                # if self.max_limit is not None:
                #     if user_data > self.max_limit:
                #         self.red_blink_timer.start()
                #         show_err_label(self)
                self.verify(user_data, show_err=True)


            super().keyPressEvent(event)


class AqStringTreeLineEdit(AqTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)

    def line_edit_changed_update_value(self, text):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        self.save_new_value(text)


class AqDateTimeLineEdit(AqTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)

    def line_edit_changed_update_value(self, text):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        # self.save_new_value(text)
        pass

    def set_value(self, value):
        value += datetime.datetime(2000, 1, 1).timestamp()
        datetime_obj = datetime.datetime.fromtimestamp(value)
        value = datetime_obj.strftime('%d.%m.%Y %H:%M:%S')
        self.setText(str(value))


class AqBitLineEdit(AqTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)
        self.setReadOnly(True)

    def mousePressEvent(self, event):
        # Меняем значение при каждом клике мышью
        try:
            current_value = int(self.text())
            new_value = 1 if current_value == 0 else 0
            QLineEdit.setText(self, str(new_value))
            self.edit_done_signal.emit(self.manager_item_handler.get_sourse_item())
        except:
            print(self.objectName() + ' error editor')


class AqBitMaskLineEdit(AqTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)
        self.param_size = param_attributes['param_size']
        self.R_Only = 1 if param_attributes['R_Only'] == 1 and \
            param_attributes["W_Only"] == 0 else 0
        self.setReadOnly(True)

    def set_value(self, value):
        if value is None:
            self.setText('')
        else:
            bin_value = bin(value)[2:]
            bin_value = bin_value.zfill(self.param_size * 8)
            bin_value = ' '.join(re.findall('.{1,4}', bin_value[::-1]))[::-1]
            self.setText(str(bin_value))

    def line_edit_changed_update_value(self, text):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        if self.R_Only == 0:
            if text != '' and text is not None:
                text = text.replace(' ', '')
                value = int(text, 2)
            else:
                value = None
            self.save_new_value(value)

    def mousePressEvent(self, event):
        if self.R_Only == 0:
            try:
                clicked_index = None
                current_text = self.text()
                # Получаем ширину текста с учетом метрик шрифта
                # text_width = self.fontMetrics().width(self.text())
                # start_len = len(current_text)
                # Получаем позицию клика мыши
                # у рядку нижче "-2" чарівне число отримане практичним шляхом
                # невідоме зміщення без якого єдітор працює некорректно.
                click_position = max(event.pos().x() - 2, 0)

                # Определяем ширину одного символа
                # char_width = self.fontMetrics().averageCharWidth()
                # char_width = text_width / len(current_text)

                # Определяем индекс символа в строке, на который был клик
                # clicked_index = int(click_position / char_width)

                # Получаем координаты каждого символа
                char_coordinates = self.get_character_coordinates()

                # Определяем, на какой символ был клик
                for i, coord in enumerate(char_coordinates):
                    if i < len(char_coordinates) - 1:
                        next_coord = char_coordinates[i + 1]
                        if coord <= click_position < next_coord:
                            clicked_index = i
                            break
                    else:
                        # Если клик был на последнем символе или за его пределами
                        if click_position >= coord:
                            clicked_index = i
                            break

                spaces = current_text[clicked_index:].count(' ')

                current_text = current_text.replace(' ', '')
                current_value = int(current_text, 2)

                # Определяем на какой бит был клик
                bit_index = int(len(self.text()) - clicked_index - spaces - 1)

                # Меняем значение соответствующего бита
                if 0 <= bit_index < len(self.text()) and self.text()[clicked_index] != ' ':
                    new_value = current_value ^ (1 << bit_index)
                    new_value = bin(new_value)
                    new_bitmask = str(new_value)[2:]
                    new_bitmask = new_bitmask.zfill(self.param_size * 8)
                    bitmask_list = re.findall('.{1,4}', new_bitmask)
                    new_bitmask = ' '.join(bitmask_list)
                    QLineEdit.setText(self, new_bitmask)
                    self.edit_done_signal.emit(self.manager_item_handler.get_sourse_item())
            except Exception as e:
                print(self.objectName() + f' error editor: {e}')

    def get_character_coordinates(self):
        # Получаем текущий текст
        text = self.text()
        font_metrics = self.fontMetrics()

        # Список для хранения координат
        coordinates = []
        current_x = 0  # Начальная координата X

        for char in text:
            # Сохраняем текущую координату начала символа
            coordinates.append(current_x)

            # Получаем ширину текущего символа
            char_width = font_metrics.horizontalAdvance(char)

            # Обновляем текущую координату X для следующего символа
            current_x += char_width

        return coordinates


class AqSignedToFloatTreeLineEdit(AqFloatTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)
        self.enum_str_dict = param_attributes.get('enum_strings', None)
        self.multiply = param_attributes.get('multiply', None)

    def set_value(self, value):
        if self.enum_str_dict is not None:
            err_code = self.enum_str_dict.get(value, None)
        else:
            err_code = None

        if err_code is not None:
            self.setText(str(err_code))
        else:
            value_in_float = value * self.multiply
            self.setText(str(value_in_float))

    def line_edit_changed_update_value(self, text):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        if text != '' and text != '-':
            value = float(text)/self.multiply
            value = int(value)
        else:
            value = None
        self.save_new_value(value)


class AqFloatEnumTreeComboBox(AqEnumTreeComboBox):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)

    def updateIndex(self, index):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        string = self.itemText(index)
        key = self.get_key_by_value(self.enum_str_dict, string)
        # value = bin(key)[2:]
        value = float(key)
        self.save_new_value(value)

    def set_value(self, value):
        value = int(value)
        # value = '0b' + str(value)
        # value = int(value, 2)
        string = self.enum_str_dict.get(value, '')
        self.setCurrentText(string)


class AqFloatEnumROnlyTreeLineEdit(AqEnumROnlyTreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)

    def set_value(self, value):
        value = int(value)
        value = '0b' + str(value)
        value = int(value, 2)
        self.setText(self.enum_str_dict.get(value, ''))


class AqEditorErrorLabel(QLabel):
    def __init__(self, pos, min_limit, max_limit, callback=None, parent=None):
        super().__init__('Invalid value', parent)
        self.callback = callback
        if min_limit is None:
            min_limit = ''
        if max_limit is None:
            max_limit = ''
        self.setText('Invalid value, valid ({}...{})'.format(min_limit, max_limit))
        self.setStyleSheet("color: #fe2d2d; background-color: #1e1f22; border-radius: 3px;\n")
        self.setFixedHeight(20)
        self.setFont(QFont("Segoe UI", 10))  # Задаем шрифт и размер
        self.move(pos.x() - 195, pos.y() - 20)
        self.show()
        # Устанавливаем задержку в 2 секунды и затем удаляем метку
        QTimer.singleShot(3000, self.delete)

    def delete(self):
        self.callback()
        self.deleteLater()

def show_err_label(self):
    # Получаем координаты поля ввода относительно окна
    rect = self.geometry()
    pos = self.mapTo(self, rect.topRight())
    self.err_label = AqEditorErrorLabel(pos, self.min_limit, self.max_limit,
                                        self.make_err_label_none, self.parent())
