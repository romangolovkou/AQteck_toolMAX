from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QDialog, QPushButton, QComboBox, QLineEdit
from PyQt5.QtCore import Qt, QTimer, QRect, QSize
from PyQt5.QtGui import QIcon, QPalette, QPixmap, QFont
from MouseEvent_func import mousePressEvent_Dragging, mouseMoveEvent_Dragging, mouseReleaseEvent_Dragging
from functools import partial

#MainFrame
class main_frame_AQFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, parent.width(), parent.height()))
        self.setMaximumSize(QSize(16777215, 16777215))
        self.setStyleSheet("background-color: #1e1f22;\n")
        self.setObjectName("main_window_frame")


#TitleBarFrame
class title_bar_frame_AQFrame(QFrame):
    def __init__(self, window_parent, height, name, icon, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, parent.width(), height))
        self.setStyleSheet("background-color: #2b2d30;\n"
                                          "border-top-left-radius: 0px;\n"
                                          "border-top-right-radius: 0px;\n"
                                          "border-bottom-left-radius: 0px;\n"
                                          "border-bottom-right-radius: 0px;")
        self.setObjectName("title_bar_frame")
        # Добавляем обработку событий мыши для перетаскивания окна
        self.mousePressEvent = partial(mousePressEvent_Dragging, window_parent)
        self.mouseMoveEvent = partial(mouseMoveEvent_Dragging, window_parent)
        self.mouseReleaseEvent = partial(mouseReleaseEvent_Dragging, window_parent)

        # Создаем метку с названием приложения
        self.title_name = QLabel(name, self)
        self.title_name.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.title_name.setStyleSheet("color: #D0D0D0;")  # Задаем цвет шрифта (серый)
        self.title_name.setAlignment(Qt.AlignHCenter)  # Выравнивание по горизонтали по центру
        self.title_name.setGeometry(0, 8, self.width(), 35)  # Устанавливаем геометрию метки

        # Создаем QLabel для отображения иконки приложения
        self.app_icon_label = QLabel(self)
        self.app_icon_label.setPixmap(icon.pixmap(30, 30))  # Устанавливаем иконку и масштабируем ее
        self.app_icon_label.setGeometry(2, 2, 30, 30)  # Устанавливаем координаты и размеры QLabel

    def custom_resize(self):
        self.title_name.setGeometry(0, 8, self.width(), 30)  # Устанавливаем геометрию метки



# ToolPanelFrame
class tool_panel_frame_AQFrame(QFrame):
    def __init__(self, shift_y, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(0, shift_y + 2, parent.width(), 90))
        self.setStyleSheet("background-color: #2b2d30;\n"
                                           "border-top-left-radius: 0px;\n"
                                           "border-top-right-radius: 0px;\n"
                                           "border-bottom-left-radius: 0px;\n"
                                           "border-bottom-right-radius: 0px;")
        self.setObjectName("tool_panel_frame")


# MainFieldFrame
class main_field_frame_AQFrame(QFrame):
    def __init__(self, shift_y, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(QRect(0, (shift_y + 2),
                                          parent.width(), parent.height() - (shift_y + 2)))
        self.setStyleSheet("background-color: #1e1f22;\n")
        self.setObjectName("main_field_frame")


class AQDialog(QDialog):
    def __init__(self, name='default'):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(0, 0, 800, 600)
        # self.move(self.screen_geometry.width() // 2 - self.width() // 2,
        #           self.screen_geometry.height() // 2 - self.height() // 2,)

        PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'
        self.AQicon = QIcon(PROJ_DIR + 'Icons/AQico_silver.png')
        self.icoMinimize = QIcon(PROJ_DIR + 'Icons/Minimize.png')
        self.icoClose = QIcon(PROJ_DIR + 'Icons/Close.png')
        self.setWindowTitle(name)
        self.setWindowIcon(self.AQicon)
        self.not_titlebtn_zone = 0
        self.setObjectName("template_window")
        self.setStyleSheet("#template_window { border: 1px solid #9ef1d3;\n }")

        # MainWindowFrame
        self.main_window_frame = main_frame_AQFrame(self)
        self.main_window_frame.setGeometry(1, 0, self.main_window_frame.width() - 2, self.main_window_frame.height() - 1)
        # TitleBarFrame
        self.title_bar_frame = title_bar_frame_AQFrame(self, 35, name, self.AQicon, self.main_window_frame)

        # Создаем кнопку свернуть
        self.btn_minimize = QPushButton('', self.title_bar_frame)
        self.btn_minimize.setIcon(QIcon(self.icoMinimize))  # установите свою иконку для кнопки
        self.btn_minimize.setGeometry(self.title_bar_frame.width() - 70, 0, 35,
                                      35)  # установите координаты и размеры кнопки
        self.btn_minimize.clicked.connect(self.showMinimized)
        self.btn_minimize.setStyleSheet(""" QPushButton:hover {background-color: #555555;}""")

        # Создаем кнопку закрытия
        self.btn_close = QPushButton('', self.title_bar_frame)
        self.btn_close.setIcon(QIcon(self.icoClose))  # установите свою иконку для кнопки
        self.btn_close.setGeometry(self.title_bar_frame.width() - 35, 0, 35,
                                   35)  # установите координаты и размеры кнопки
        self.btn_close.clicked.connect(self.close)  # добавляем обработчик события нажатия на кнопку закрытия
        self.btn_close.setStyleSheet(""" QPushButton:hover {background-color: #555555;}""")


# Создание комбо-бокса
class AQComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        # self.setStyleSheet("border: 1px solid #9ef1d3; color: #D0D0D0; background-color: #2b2d30;")  # Задаем цветную границу и цвет шрифта
        # self.setStyleSheet("color: #D0D0D0; background-color: #2b2d30;")  # Задаем цветную границу и цвет шрифта
        self.setStyleSheet("border-left: 1px solid #9ef1d3; border-top: 1px solid #9ef1d3; \n"
                           "border-bottom: 1px solid #5bb192; border-right: 1px solid #5bb192; \n"
                           "color: #D0D0D0; background-color: #2b2d30; border-radius: 4px; \n")  # Задаем цветную границу и цвет шрифта
        self.view().setStyleSheet("color: #D0D0D0;")  # Задаем цвет шрифта в выпадающем списке


# Создаем текстовую метку
class AQLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setStyleSheet("color: #D0D0D0; \n")
        self.setFixedHeight(20)
        self.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.setText(text)


class Slave_ID_AQLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.setStyleSheet("border-left: 1px solid #9ef1d3; border-top: 1px solid #9ef1d3; \n"
                           "border-bottom: 1px solid #5bb192; border-right: 1px solid #5bb192; \n"
                           "color: #D0D0D0; background-color: #2b2d30; border-radius: 4px; \n")  # Задаем цветную границу и цвет шрифта
        self.red_blink_timer = QTimer()
        self.red_blink_timer.setInterval(40)
        self.red_blink_timer.timeout.connect(self.err_blink)
        self.anim_cnt = 0
        self.color_code = 0x2b  # Берется из цвета background-color, первые два символа после # соответствуют RED

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
            if slave_id < 248 and len(str_copy) < 4:
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
        self.err_label = AQLabel('Invalid value, valid (0...247)', self.parent())
        self.err_label.setStyleSheet("color: #fe2d2d; \n")
        self.err_label.setFixedSize(190, 12)
        self.err_label.move(pos.x() - 190, pos.y() - 15)
        self.err_label.show()
        # Устанавливаем задержку в 2 секунды и затем удаляем метку
        QTimer.singleShot(3000, self.err_label.deleteLater)


class IP_AQLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaxLength(15)  # Устанавливаем максимальную длину IP-адреса (15 символов)
        self.setFixedHeight(30)
        self.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.setStyleSheet("border-left: 1px solid #9ef1d3; border-top: 1px solid #9ef1d3; \n"
                           "border-bottom: 1px solid #5bb192; border-right: 1px solid #5bb192; \n"
                           "color: #D0D0D0; background-color: #2b2d30; border-radius: 4px; \n")  # Задаем цветную границу и цвет шрифта
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
                self.show_err_label()
                return

        super().keyPressEvent(event)

    def show_err_label(self):
        # Получаем координаты поля ввода относительно диалогового окна
        rect = self.geometry()
        pos = self.mapTo(self, rect.topRight())
        self.err_label = AQLabel('Invalid value, valid (0...255)', self.parent())
        self.err_label.setStyleSheet("color: #fe2d2d; \n")
        self.err_label.setFixedSize(190, 12)
        self.err_label.move(pos.x() - 190, pos.y() - 15)
        self.err_label.show()
        # Устанавливаем задержку в 2 секунды и затем удаляем метку
        QTimer.singleShot(3000, self.err_label.deleteLater)