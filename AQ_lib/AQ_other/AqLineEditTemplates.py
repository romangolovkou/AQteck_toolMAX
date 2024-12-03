from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QLineEdit, QLabel


class AqSlaveIdLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.red_blink_timer = QTimer()
        self.red_blink_timer.setInterval(40)
        self.red_blink_timer.timeout.connect(self.err_blink)
        self.anim_cnt = 0
        self.color_code = 0x2b  # Берется из цвета background-color, первые два символа после # соответствуют RED

        self.min_limit = 0
        self.max_limit = 247
        self.max_str_len = 3

    def err_blink(self):
        if self.anim_cnt < 34:
            self.anim_cnt += 1
            if self.anim_cnt < 18:
                self.color_code = self.color_code + 0xA
            else:
                self.color_code = self.color_code - 0xA

            hex_string = format(self.color_code, 'x')
            self.setStyleSheet("border-left: 1px solid #9ef1d3; border-top: 1px solid #9ef1d3; \n"
                               "border-bottom: 1px solid #5bb192; border-right: 1px solid #5bb192; \n"
                               "color: #D0D0D0; background-color: #{}2d30; border-radius: 4px; \n".format(hex_string))
        else:
            self.anim_cnt = 0
            self.color_code = 0x2b
            self.setStyleSheet("border-left: 1px solid #9ef1d3; border-top: 1px solid #9ef1d3; \n"
                               "border-bottom: 1px solid #5bb192; border-right: 1px solid #5bb192; \n"
                               "color: #D0D0D0; background-color: #2b2d30; border-radius: 4px; \n")
            self.red_blink_timer.stop()

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
            return

        if self.hasSelectedText():
            self.backspace()

        cursor_position = self.cursorPosition()
        text = event.text()
        if not text.isdigit():
            # Если не цифра
            return
        # Если цифра
        else:
            str_copy = self.text()
            str_copy = str_copy[:cursor_position] + text + str_copy[cursor_position:]
            slave_id = int(str_copy)  # Преобразуем подстроку в целое число
            if self.min_limit <= slave_id <= self.max_limit and len(str_copy) <= self.max_str_len:
                self.insert(text)
                self.setCursorPosition(cursor_position + 1)
                return
            else:
                self.red_blink_timer.start()
                self.show_err_label()
                return

        super().keyPressEvent(event)

    def show_err_label(self):
        # Получаем координаты поля ввода относительно диалогового окна
        rect = self.geometry()
        pos = self.mapTo(self, rect.topRight())
        self.err_label = QLabel('Invalid value, valid (0...247)', self.parent())
        self.err_label.setStyleSheet("color: #fe2d2d; \n")
        self.err_label.setFixedSize(190, 12)
        self.err_label.move(pos.x() - 190, pos.y() - 15)
        self.err_label.show()
        # Устанавливаем задержку в 2 секунды и затем удаляем метку
        QTimer.singleShot(3000, self.err_label.deleteLater)


class AqIpLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.red_blink_timer = QTimer()
        self.red_blink_timer.setInterval(40)
        self.red_blink_timer.timeout.connect(self.err_blink)
        self.anim_cnt = 0
        self.color_code = 0x2b #Берется из цвета background-color, первые два символа после # соответствуют RED


    def err_blink(self):
        if self.anim_cnt < 34:
            self.anim_cnt += 1
            if self.anim_cnt < 18:
                self.color_code = self.color_code + 0xA
            else:
                self.color_code = self.color_code - 0xA

            hex_string = format(self.color_code, 'x')
            self.setStyleSheet("border-left: 1px solid #9ef1d3; border-top: 1px solid #9ef1d3; \n"
                               "border-bottom: 1px solid #5bb192; border-right: 1px solid #5bb192; \n"
                               "color: #D0D0D0; background-color: #{}2d30; border-radius: 4px; \n".format(hex_string))
        else:
            self.anim_cnt = 0
            self.color_code = 0x2b
            self.setStyleSheet("border-left: 1px solid #9ef1d3; border-top: 1px solid #9ef1d3; \n"
                               "border-bottom: 1px solid #5bb192; border-right: 1px solid #5bb192; \n"
                               "color: #D0D0D0; background-color: #2b2d30; border-radius: 4px; \n")
            self.red_blink_timer.stop()
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
                if left_character.isdigit() and self.text().count(".") < 3:
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
                self.show_err_label()
                return

        super().keyPressEvent(event)

    def show_err_label(self):
        # Получаем координаты поля ввода относительно диалогового окна
        rect = self.geometry()
        pos = self.mapTo(self, rect.topRight())
        self.err_label = QLabel('Invalid value, valid (0...255)', self.parent())
        self.err_label.setStyleSheet("color: #fe2d2d; \n")
        self.err_label.setFixedSize(190, 12)
        self.err_label.move(pos.x() - 190, pos.y() - 15)
        self.err_label.show()
        # Устанавливаем задержку в 2 секунды и затем удаляем метку
        QTimer.singleShot(3000, self.err_label.deleteLater)


class AqFloatLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    # def line_edit_changed_update_value(self, text):
    #     # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
    #     if text != '' and text != '-':
    #         value = float(text)
    #     else:
    #         value = None
    #     self.save_new_value(value)

    # def verify(self, value=None, show_err=False):
    #     if value is None:
    #         if self.text() != '' and self.text() is not None:
    #             try:
    #                 value = int(self.text())
    #             except:
    #                 value = str(self.text())
    #         else:
    #             return None
    #
    #     if self.min_limit is not None or self.max_limit is not None:
    #         if value != '':
    #             value = float(value)
    #             if value < self.min_limit or value > self.max_limit:
    #                 if show_err:
    #                     self.red_blink_timer.start()
    #                     if self.err_label is None:
    #                         show_err_label(self)
    #                 return False
    #             else:
    #                 if self.err_label is not None:
    #                     try:
    #                         self.err_label.hide()
    #                         self.err_label.deleteLater()
    #                         self.err_label = None
    #                     except:
    #                         pass
    #
    #                 return True

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
                # str_copy = self.text()
                # self.verify(str_copy)
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
                            # str_copy = self.text()
                            # user_data = float(str_copy)  # Преобразуем подстроку в целое число
                            # self.verify(user_data, show_err=True)

                            return
                    else:
                        self.setCursorPosition(0)
                        self.insert(text)
                        self.setCursorPosition(1)
                        return
                elif text == '.':
                    if '.' in str_copy:
                        return

                # str_copy = str_copy[:cursor_position] + text + str_copy[cursor_position:]
                # user_data = float(str_copy)  # Преобразуем подстроку в целое число
                #
                # self.verify(user_data, show_err=True)

            super().keyPressEvent(event)


class AqIntLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    # def line_edit_changed_update_value(self, text):
    #     # Этот метод вызывается каждый раз, когда текст в QLineEdit изменяется
    #     if text != '' and text != '-':
    #         value = int(text)
    #     else:
    #         value = None
    #     self.save_new_value(value)

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
                # self.verify(str_copy)
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
                            # str_copy = self.text()
                            # user_data = int(str_copy)  # Преобразуем подстроку в целое число
                            # if self.min_limit is not None:
                            #     if user_data < self.min_limit:
                            #         self.red_blink_timer.start()
                            #         show_err_label(self)
                            # if self.max_limit is not None:
                            #     if user_data > self.max_limit:
                            #         self.red_blink_timer.start()
                            #         show_err_label(self)
                            # self.verify(user_data, show_err=True)

                            return
                    else:
                        self.setCursorPosition(0)
                        self.insert(text)
                        self.setCursorPosition(1)
                        return

                # str_copy = str_copy[:cursor_position] + text + str_copy[cursor_position:]
                # user_data = int(str_copy)  # Преобразуем подстроку в целое число
                # if self.min_limit is not None:
                #     if user_data < self.min_limit:
                #         self.red_blink_timer.start()
                #         show_err_label(self)
                # if self.max_limit is not None:
                #     if user_data > self.max_limit:
                #         self.red_blink_timer.start()
                #         show_err_label(self)
                # self.verify(user_data, show_err=True)

            super().keyPressEvent(event)


