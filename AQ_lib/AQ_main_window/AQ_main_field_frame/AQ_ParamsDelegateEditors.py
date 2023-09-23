import binascii
import datetime
import ipaddress
import socket
import struct

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QComboBox, QLineEdit
from AQ_CustomWindowTemplates import AQ_Label


class AQ_TreeLineEdit(QLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(parent)
        self.min_limit = param_attributes.get('min_limit', None)
        self.max_limit = param_attributes.get('max_limit', None)
        self.save_new_value = None
        self.setStyleSheet(
            "border: none; color: #D0D0D0; background-color: transparent; \n")  # Задаем цветную границу и цвет шрифта
        self.red_blink_timer = QTimer()
        self.red_blink_timer.setInterval(40)
        self.red_blink_timer.timeout.connect(self.err_blink)
        self.anim_cnt = 0
        self.color_code = 0x2b  # Берется из цвета background-color, первые два символа после # соответствуют RED
        if param_attributes.get('R_Only', 0) == 1 and param_attributes.get('W_Only', 0) == 0:
            self.setReadOnly(True)
            self.setStyleSheet("border: none; color: #909090; background-color: transparent; \n")
        else:
            self.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent; \n")
            self.textChanged.connect(self.line_edit_changed_update_value)

    def line_edit_changed_update_value(self, text):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        if text != '':
            value = int(text)
        else:
            value = None
        self.save_new_value(value)

    def set_new_value_handler(self, handler):
        self.save_new_value = handler

    def set_value(self, value):
        self.setText(str(value))

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


class AQ_EnumTreeComboBox(QComboBox):
    def __init__(self, param_attributes, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.view().setStyleSheet("color: #D0D0D0; background-color: #1e1f22;")
        self.setStyleSheet("QComboBox { border: 0px solid #D0D0D0; color: #D0D0D0; }")
        self.save_new_value = None
        enum_strings = param_attributes.get('enum_strings', '')
        for i in range(len(enum_strings)):
            enum_str = enum_strings[i]
            self.addItem(enum_str)

        self.currentIndexChanged.connect(self.updateIndex)

    def updateIndex(self, index):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        self.save_new_value(index)

    def set_new_value_handler(self, handler):
        self.save_new_value = handler

    def set_value(self, value):
        self.setCurrentIndex(value)


class AQ_EnumROnlyTreeLineEdit(AQ_TreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)
        self.enum_strings = param_attributes.get('enum_strings', '')

    def set_value(self, value):
        self.setText(self.enum_strings[value])


class AQ_UintTreeLineEdit(AQ_TreeLineEdit):
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
                return

            cursor_position = self.cursorPosition()
            text = event.text()
            if not text.isdigit():
                # Якщо не цифра
                return
            # Если цифра
            else:
                str_copy = self.text()
                str_copy = str_copy[:cursor_position] + text + str_copy[cursor_position:]
                user_data = int(str_copy)  # Преобразуем подстроку в целое число
                if self.min_limit is not None:
                    if user_data < self.min_limit:
                        self.red_blink_timer.start()
                        show_err_label(self)
                if self.max_limit is not None:
                    if user_data > self.max_limit:
                        self.red_blink_timer.start()
                        show_err_label(self)


            super().keyPressEvent(event)


class AQ_IpTreeLineEdit(AQ_TreeLineEdit):
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


class AQ_IntTreeLineEdit(AQ_TreeLineEdit):
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
                return

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
                            if self.min_limit is not None:
                                if user_data < self.min_limit:
                                    self.red_blink_timer.start()
                                    show_err_label(self)
                            if self.max_limit is not None:
                                if user_data > self.max_limit:
                                    self.red_blink_timer.start()
                                    show_err_label(self)
                            return
                    else:
                        self.setCursorPosition(0)
                        self.insert(text)
                        self.setCursorPosition(1)
                        return

                str_copy = str_copy[:cursor_position] + text + str_copy[cursor_position:]
                user_data = int(str_copy)  # Преобразуем подстроку в целое число
                if self.min_limit is not None:
                    if user_data < self.min_limit:
                        self.red_blink_timer.start()
                        show_err_label(self)
                if self.max_limit is not None:
                    if user_data > self.max_limit:
                        self.red_blink_timer.start()
                        show_err_label(self)


            super().keyPressEvent(event)


class AQ_FloatTreeLineEdit(AQ_TreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)

    def line_edit_changed_update_value(self, text):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        if text != '' and text != '-':
            value = float(text)
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
                return

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
                            if self.min_limit is not None:
                                if user_data < self.min_limit:
                                    self.red_blink_timer.start()
                                    show_err_label(self)
                            if self.max_limit is not None:
                                if user_data > self.max_limit:
                                    self.red_blink_timer.start()
                                    show_err_label(self)
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
                if self.min_limit is not None:
                    if user_data < self.min_limit:
                        self.red_blink_timer.start()
                        show_err_label(self)
                if self.max_limit is not None:
                    if user_data > self.max_limit:
                        self.red_blink_timer.start()
                        show_err_label(self)


            super().keyPressEvent(event)


class AQ_StringTreeLineEdit(AQ_TreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)

    def line_edit_changed_update_value(self, text):
        # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
        self.save_new_value(text)


class AQ_DateTimeLineEdit(AQ_TreeLineEdit):
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


class AQ_EditorErrorLabel(AQ_Label):
    def __init__(self, pos, min_limit, max_limit, parent=None):
        super().__init__('Invalid value', parent)
        if min_limit is None:
            min_limit = ''
        if max_limit is None:
            max_limit = ''
        self.setText('Invalid value, valid ({}...{})'.format(min_limit, max_limit))
        self.setStyleSheet("color: #fe2d2d; background-color: #1e1f22; border-radius: 3px;\n")
        self.move(pos.x() - 195, pos.y() - 20)
        self.show()
        # Устанавливаем задержку в 2 секунды и затем удаляем метку
        QTimer.singleShot(3000, self.deleteLater)


def show_err_label(self):
    # Получаем координаты поля ввода относительно окна
    rect = self.geometry()
    pos = self.mapTo(self, rect.topRight())
    self.err_label = AQ_EditorErrorLabel(pos, self.min_limit, self.max_limit, self.parent())
