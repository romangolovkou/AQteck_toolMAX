import socket
import struct

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QComboBox, QLineEdit

from custom_window_templates import AQLabel


class AQ_TreeViewComboBox(QComboBox):
    def __init__(self, param_attributes, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.view().setStyleSheet("color: #D0D0D0; background-color: #1e1f22;")
        self.setStyleSheet("QComboBox { border: 0px solid #D0D0D0; color: #D0D0D0; }")
        enum_strings = param_attributes.get('enum_strings', '')
        for i in range(len(enum_strings)):
            enum_str = enum_strings[i]
            self.addItem(enum_str)
        # self.currentIndexChanged.connect(self.parent.commit_editor_data)

    def set_value(self, value):
        self.setCurrentIndex(value)


class AQ_TreeLineEdit(QLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(parent)
        self.min_limit = param_attributes.get('min_limit', None)
        self.max_limit = param_attributes.get('max_limit', None)
        self.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent; \n")  # Задаем цветную границу и цвет шрифта
        self.red_blink_timer = QTimer()
        self.red_blink_timer.setInterval(40)
        self.red_blink_timer.timeout.connect(self.err_blink)
        self.anim_cnt = 0
        self.color_code = 0x2b  # Берется из цвета background-color, первые два символа после # соответствуют RED

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


class AQ_UintTreeLineEdit(AQ_TreeLineEdit):
    def __init__(self, param_attributes, parent=None):
        super().__init__(param_attributes, parent)
        self.min_limit = param_attributes.get('min_limit', None)
        self.max_limit = param_attributes.get('max_limit', None)
        self.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent; \n")  # Задаем цветную границу и цвет шрифта
        self.red_blink_timer = QTimer()
        self.red_blink_timer.setInterval(40)
        self.red_blink_timer.timeout.connect(self.err_blink)
        self.anim_cnt = 0
        self.color_code = 0x2b  # Берется из цвета background-color, первые два символа после # соответствуют RED

    def keyPressEvent(self, event):
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
            if not str_copy.strip():
                self.insert('0')
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
        self.setStyleSheet("color: #D0D0D0; background-color: transparent; border-radius: 3px; \n")  # Задаем цветную границу и цвет шрифта
        self.red_blink_timer = QTimer()
        self.red_blink_timer.setInterval(40)
        self.red_blink_timer.timeout.connect(self.err_blink)
        self.anim_cnt = 0
        self.color_code = 0x2b #Берется из цвета background-color, первые два символа после # соответствуют RED

    def set_value(self, value):
        value = socket.inet_ntoa(struct.pack('!L', value))
        self.setText(value)

    def keyPressEvent(self, event):
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
        self.min_limit = param_attributes.get('min_limit', None)
        self.max_limit = param_attributes.get('max_limit', None)
        # self.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent; \n")  # Задаем цветную границу и цвет шрифта
        self.red_blink_timer = QTimer()
        self.red_blink_timer.setInterval(40)
        self.red_blink_timer.timeout.connect(self.err_blink)
        self.anim_cnt = 0
        self.color_code = 0x2b  # Берется из цвета background-color, первые два символа после # соответствуют RED

    def keyPressEvent(self, event):
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
            if not str_copy.strip():
                self.insert('0')
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
        self.min_limit = param_attributes.get('min_limit', None)
        self.max_limit = param_attributes.get('max_limit', None)
        # self.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent; \n")  # Задаем цветную границу и цвет шрифта
        self.red_blink_timer = QTimer()
        self.red_blink_timer.setInterval(40)
        self.red_blink_timer.timeout.connect(self.err_blink)
        self.anim_cnt = 0
        self.color_code = 0x2b  # Берется из цвета background-color, первые два символа после # соответствуют RED

    def keyPressEvent(self, event):
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
            if not str_copy.strip():
                self.insert('0')
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


class AQ_EditorErrorLabel(AQLabel):
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
