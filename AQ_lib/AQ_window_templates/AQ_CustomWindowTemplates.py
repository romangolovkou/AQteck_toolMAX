from PySide6.QtWidgets import QWidget, QFrame, QLabel, QDialog, QPushButton, QComboBox, QLineEdit, QProgressBar
from PySide6.QtCore import Qt, QTimer, QRect, QSize
from PySide6.QtGui import QIcon, QFont, QPainter, QColor, QPen
from AQ_MouseEventFunc import mousePressEvent_Dragging, mouseMoveEvent_Dragging, mouseReleaseEvent_Dragging
from functools import partial

from AQ_ResizeWidgets import resizeWidthR_Qwidget, resizeHeigthLow_Qwidget, resizeHeigthTop_Qwidget, \
    resizeDiag_BotRigth_Qwidget, resizeWidthL_Qwidget, resizeDiag_BotLeft_Qwidget, resizeDiag_TopLeft_Qwidget, \
    resizeDiag_TopRigth_Qwidget

PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'

class AQ_SimplifiedMainFrame(QFrame):
    def __init__(self, event_manager, window_name, icon, parent=None):
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, parent.width(), parent.height()))
        self.setMaximumSize(QSize(16777215, 16777215))
        self.setStyleSheet("background-color: #1e1f22;")
        self.setObjectName("main_window_frame")
        # TitleBarFrame
        self.title_bar_frame = AQ_SimplifiedTitleBarFrame(event_manager, 35, window_name, icon, self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.title_bar_frame.resize(self.width(), self.title_bar_frame.height())

        event.accept()


class AQ_FullMainFrame(AQ_SimplifiedMainFrame):
    def __init__(self, event_manager, window_name, icon, parent=None):
        super().__init__(event_manager, window_name, icon, parent)

        self.event_manager = event_manager
        # TitleBarFrame
        self.title_bar_frame = AQ_FullTitleBarFrame(self.event_manager, 35, window_name, icon, self)

        # # Создаем виджеты для изменения размеров окна
        self.resizeLineWidth = 4
        self.resizeWidthR_widget = resizeWidthR_Qwidget(self.event_manager, window_name, self)
        self.resizeWidthL_widget = resizeWidthL_Qwidget(self.event_manager, window_name, self)
        self.resizeHeigthLow_widget = resizeHeigthLow_Qwidget(self.event_manager, window_name, self)
        self.resizeHeigthTop_widget = resizeHeigthTop_Qwidget(self.event_manager, window_name, self)
        self.resizeDiag_BotRigth_widget = resizeDiag_BotRigth_Qwidget(self.event_manager, window_name, self)
        self.resizeDiag_BotLeft_widget = resizeDiag_BotLeft_Qwidget(self.event_manager, window_name, self)
        self.resizeDiag_TopLeft_widget = resizeDiag_TopLeft_Qwidget(self.event_manager, window_name, self)
        self.resizeDiag_TopRigth_widget = resizeDiag_TopRigth_Qwidget(self.event_manager, window_name, self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.title_bar_frame.resize(self.width(), self.title_bar_frame.height())
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

        event.accept()


class AQ_SimplifiedTitleBarFrame(QFrame):
    def __init__(self, event_manager, height, name, icon, parent=None):
        super().__init__(parent)
        self.event_manager = event_manager
        self.setGeometry(QRect(0, 0, parent.width(), height))
        self.setStyleSheet("background-color: #2b2d30;\n"
                                          "border-top-left-radius: 0px;\n"
                                          "border-top-right-radius: 0px;\n"
                                          "border-bottom-left-radius: 0px;\n"
                                          "border-bottom-right-radius: 0px;")
        self.setObjectName("title_bar_frame")
        self.mousePressEvent = partial(mousePressEvent_Dragging, self)
        self.mouseMoveEvent = partial(mouseMoveEvent_Dragging, self, self.event_manager, 'dragging_' + name)
        self.mouseReleaseEvent = partial(mouseReleaseEvent_Dragging, self)

        self.title_name = QLabel(name, self)
        self.title_name.setFont(QFont("Verdana", 10))
        self.title_name.setStyleSheet("color: #D0D0D0;")
        self.title_name.setAlignment(Qt.AlignHCenter)
        self.title_name.setGeometry(0, 8, self.width(), 35)

        self.app_icon_label = QLabel(self)
        self.app_icon_label.setPixmap(icon.pixmap(30, 30))
        self.app_icon_label.setGeometry(2, 2, 30, 30)

        # Создаем кнопку свернуть
        self.btn_minimize = QPushButton('', self)
        self.icoMinimize = QIcon('Icons/Minimize.png')
        self.btn_minimize.setIcon(QIcon(self.icoMinimize))  # установите свою иконку для кнопки
        self.btn_minimize.setGeometry(self.width() - 70, 0, 35, 35)  # установите координаты и размеры кнопки
        self.btn_minimize.clicked.connect(lambda: self.event_manager.emit_event('minimize_' + name))
        self.btn_minimize.setStyleSheet(""" QPushButton:hover {background-color: #555555;}""")

        # Создаем кнопку закрытия
        self.btn_close = QPushButton('', self)
        self.icoClose = QIcon('Icons/Close.png')
        self.btn_close.setIcon(QIcon(self.icoClose))  # установите свою иконку для кнопки
        self.btn_close.setGeometry(self.width() - 35, 0, 35, 35)  # установите координаты и размеры кнопки
        self.btn_close.clicked.connect(lambda: self.event_manager.emit_event('close_' + name))  # добавляем обработчик события нажатия на кнопку закрытия
        self.btn_close.setStyleSheet(""" QPushButton:hover {background-color: #555555;}""")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.title_name.setGeometry(0, 8, self.width(), 35)
        self.btn_minimize.move(self.width() - 70, 0)
        self.btn_close.move(self.width() - 35, 0)

        event.accept()


class AQ_FullTitleBarFrame(AQ_SimplifiedTitleBarFrame):
    def __init__(self, event_manager, height, name, icon, parent=None):
        super().__init__(event_manager, height, name, icon, parent)
        self.name = name
        self.btn_close.setGeometry(self.width() - 35, 0, 35,
                                   35)  # установите координаты и размеры кнопки

        # Переміщюємо кнопку згорнути
        self.btn_minimize.setGeometry(self.width() - 105, 0, 35,
                                      35)  # установите координаты и размеры кнопки

        # Создаем кнопку развернуть/нормализировать
        self.icoMaximize = QIcon('Icons/Maximize.png')
        self.icoNormalize = QIcon('Icons/_Normalize.png')
        self.isMaximized = False  # Флаг, указывающий на текущее состояние окна
        self.btn_maximize = QPushButton('', self)
        self.btn_maximize.setIcon(QIcon(self.icoMaximize))  # установите свою иконку для кнопки
        self.btn_maximize.setGeometry(self.width() - 70, 0, 35,
                                      35)  # установите координаты и размеры кнопки
        self.btn_maximize.clicked.connect(self.toggleMaximize)
        self.btn_maximize.setStyleSheet(""" QPushButton:hover {background-color: #555555;}""")

    def toggleMaximize(self):
        try:
            if self.isMaximized:
                self.event_manager.emit_event('normalize_' + self.name)
                self.btn_maximize.setIcon(QIcon(self.icoMaximize))
                self.isMaximized = False
            else:
                self.event_manager.emit_event('maximize_' + self.name)
                self.btn_maximize.setIcon(QIcon(self.icoNormalize))
                self.isMaximized = True
        except Exception as e:
            print(f"Error occurred: {str(e)}")

    def name_label_resize(self):
        self.title_name.setGeometry(0, 8, self.width(), 30)  # Устанавливаем геометрию метки

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.btn_maximize.move(self.width() - 70, 0)
        self.btn_minimize.move(self.width() - 105, 0)
        self.btn_close.move(self.width() - 35, 0)
        self.name_label_resize()
        event.accept()


# MainFieldFrame
class AQ_ReducedMainFieldFrame(QFrame):
    def __init__(self, shift_y, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(QRect(0, (shift_y + 2),
                                          parent.width(), parent.height() - (shift_y + 2)))
        self.setStyleSheet("background-color: #1e1f22;\n")
        self.setObjectName("main_field_frame")


class AQ_SimplifiedDialog(QDialog):
    def __init__(self, event_manager, window_name='default'):
        super().__init__()
        self.window_name = window_name
        self.event_manager = event_manager
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 800, 600)

        self.AQicon = QIcon('Icons/AQico_silver.png')

        self.setWindowTitle(window_name)
        self.setWindowIcon(self.AQicon)
        self.setObjectName("AQ_simplified_Dialog")

        # Рєєструємо обробники подій
        self.event_manager.register_event_handler('minimize_' + window_name, self.showMinimized)
        self.event_manager.register_event_handler('close_' + window_name, self.close)
        self.event_manager.register_event_handler('dragging_' + window_name, self.move)

        # MainWindowFrame
        self.main_window_frame = AQ_SimplifiedMainFrame(self.event_manager, window_name, self.AQicon, self)
        self.main_window_frame.setGeometry(0, 0, self.main_window_frame.width(), self.main_window_frame.height())

        # Прибрати коли буде UI
        self.left_border = QFrame(self)
        self.left_border.setGeometry(0, 0, 1, self.height())
        self.left_border.setStyleSheet("background-color: #FFFFFF;\n")
        self.right_border = QFrame(self)
        self.right_border.setGeometry(0, self.height() - 1, self.width(), 1)
        self.right_border.setStyleSheet("background-color: #FFFFFF;\n")
        self.bottom_border = QFrame(self)
        self.bottom_border.setGeometry(self.width() - 1, 0, 1, self.height())
        self.bottom_border.setStyleSheet("background-color: #FFFFFF;\n")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.main_window_frame.resize(self.width(), self.height())
        # Прибрати коли буде UI
        self.left_border.setGeometry(0, 0, 1, self.height())
        self.right_border.setGeometry(0, self.height() - 1, self.width(), 1)
        self.bottom_border.setGeometry(self.width() - 1, 0, 1, self.height())
        event.accept()

class AQ_FullDialog(AQ_SimplifiedDialog):
    def __init__(self, event_manager, window_name='default'):
        super().__init__(event_manager, window_name)
        self.setObjectName("AQ_full_Dialog")
        self.event_manager.register_event_handler('maximize_' + window_name, self.showMaximized)
        self.event_manager.register_event_handler('normalize_' + window_name, self.showNormal)
        self.event_manager.register_event_handler('resize_' + window_name, self.resize_window)
        # MainWindowFrame
        self.main_window_frame = AQ_FullMainFrame(event_manager, window_name, self.AQicon, self)
        self.main_window_frame.setGeometry(0, 0, self.main_window_frame.width(), self.main_window_frame.height())

        # Прибрати коли буде UI
        self.left_border = QFrame(self)
        self.left_border.setGeometry(0, 0, 1, self.height())
        self.left_border.setStyleSheet("background-color: #FFFFFF;\n")
        self.right_border = QFrame(self)
        self.right_border.setGeometry(0, self.height() - 1, self.width(), 1)
        self.right_border.setStyleSheet("background-color: #FFFFFF;\n")
        self.bottom_border = QFrame(self)
        self.bottom_border.setGeometry(self.width() - 1, 0, 1, self.height())
        self.bottom_border.setStyleSheet("background-color: #FFFFFF;\n")


    def resize_window(self, pos_x, pos_y, width, height):
        if pos_x == '%':
            pos_x = self.pos().x()
        if pos_y == '%':
            pos_y = self.pos().y()
        if width == '%':
            width = self.width()
        if height == '%':
            height = self.height()

        self.setGeometry(pos_x, pos_y, width, height)

    def resizeEvent(self, event):
        # Переопределяем метод resizeEvent и вызываем resize для main_window_frame
        self.main_window_frame.resize(self.width(), self.height())
        # Прибрати коли буде UI
        self.left_border.setGeometry(0, 0, 1, self.height())
        self.right_border.setGeometry(0, self.height() - 1, self.width(), 1)
        self.bottom_border.setGeometry(self.width() - 1, 0, 1, self.height())
        event.accept()


# Создание комбо-бокса
class AQ_ComboBox(QComboBox):
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
class AQ_Label(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setStyleSheet("color: #D0D0D0;")
        self.setFixedHeight(20)
        self.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.setText(text)


class AQ_SlaveIdLineEdit(QLineEdit):
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
        self.err_label = AQ_Label('Invalid value, valid (0...247)', self.parent())
        self.err_label.setStyleSheet("color: #fe2d2d; \n")
        self.err_label.setFixedSize(190, 12)
        self.err_label.move(pos.x() - 190, pos.y() - 15)
        self.err_label.show()
        # Устанавливаем задержку в 2 секунды и затем удаляем метку
        QTimer.singleShot(3000, self.err_label.deleteLater)


class AQ_IpLineEdit(QLineEdit):
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
        self.err_label = AQ_Label('Invalid value, valid (0...255)', self.parent())
        self.err_label.setStyleSheet("color: #fe2d2d; \n")
        self.err_label.setFixedSize(190, 12)
        self.err_label.move(pos.x() - 190, pos.y() - 15)
        self.err_label.show()
        # Устанавливаем задержку в 2 секунды и затем удаляем метку
        QTimer.singleShot(3000, self.err_label.deleteLater)


class AQ_wait_progress_bar_widget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 340, 50)
        self.frame.setStyleSheet("border: 1px solid #9ef1d3; border-radius: 25px;")
        self.text_label = AQ_Label(text, self)
        self.text_label.move(30, 5)
        self.text_label.setStyleSheet("border: none; color: #D0D0D0")
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(30, 30, 280, 6)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("")  # Убираем текст с процентами
        self.progress_bar.setStyleSheet('''
                    QProgressBar {
                        border: 1px solid #FFFFFF; /* Изменение цвета рамки */
                        border-radius: 2px; /* Скругление углов */
                    }
                    QProgressBar::chunk {
                        background-color: #9ef1d3; /* Цвет заполнения */
                        text-align: none; /* Убираем метку с процентами */
                    }
                ''')
        # self.progress_bar.show()
        self.show()


class AQ_have_error_widget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 230, 80)
        self.frame.setStyleSheet("border: 2px solid #fe2d2d; border-radius: 5px; background-color: #1e1f22")
        self.text_label = QLabel(text, self)
        self.text_label.setFont(QFont("Segoe UI", 12))
        self.text_label.move(10, 5)
        self.text_label.setStyleSheet("border: none; color: #E0E0E0; background-color: transparent")
        self.show()



