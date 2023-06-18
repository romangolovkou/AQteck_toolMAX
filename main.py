import sys
import random
import time
from functools import partial
from PyQt5.QtGui import QIcon, QPalette, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QRect, QSize, QEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QMenu, QAction, QHBoxLayout, \
    QVBoxLayout, QSizeGrip, QFrame, QSizePolicy, QSplashScreen, QDialog, QComboBox
from ToolPanelButtons import AddDeviceButton, VLine_separator, Btn_AddDevices, Btn_DeleteDevices, \
                            Btn_IPAdresess, Btn_Read, Btn_Write, Btn_FactorySettings, Btn_WatchList
from ToolPanelLayouts import replaceToolPanelWidget
from Resize_widgets import resizeWidthR_Qwidget, resizeWidthL_Qwidget, resizeHeigthLow_Qwidget, \
                           resizeHeigthTop_Qwidget, resizeDiag_BotRigth_Qwidget, resizeDiag_BotLeft_Qwidget, \
                           resizeDiag_TopLeft_Qwidget, resizeDiag_TopRigth_Qwidget
from custom_window_templates import main_frame_QFrame, title_bar_frame_QFrame, tool_panel_frame_QFrame, \
                                    main_field_frame_QFrame, template_window_QDialog
import serial.tools.list_ports


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        MainName = 'AQtech Tool MAX'
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


        #MainWindowFrame
        self.main_window_frame = main_frame_QFrame(self)
        #TitleBarFrame
        self.title_bar_frame = title_bar_frame_QFrame(self, 60, MainName, self.AQicon, self.main_window_frame)
        # ToolPanelFrame
        self.tool_panel_frame = tool_panel_frame_QFrame(self.title_bar_frame.height(), self.main_window_frame)
        # MainFieldFrame
        self.main_field_frame = main_field_frame_QFrame(self.title_bar_frame.height() + self.tool_panel_frame.height(), self)

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

            event.accept()
        except Exception as e:
            print(f"Error occurred: {str(e)}")

    def open_AddDevices(self):
        AddDevices_window = AddDevices_QDialog('Add Devices')
        AddDevices_window.exec_()


class AddDevices_QDialog(template_window_QDialog):
    def __init__(self, name):
        super().__init__(name)

        self.screen_geometry = QApplication.desktop().screenGeometry()
        self.move(self.screen_geometry.width() // 2 - self.width() // 2,
                  self.screen_geometry.height() // 2 - self.height() // 2,)

        # Создание комбо-бокса
        self.combo_box = QComboBox(self.main_window_frame)
        self.combo_box.setFixedHeight(35)
        self.combo_box.addItem("Ethernet")  # Добавление опции "Ethernet"
        self.combo_box.setFont(QFont("Verdana", 11))  # Задаем шрифт и размер
        self.combo_box.setStyleSheet("border: 1px solid #9ef1d3; color: #D0D0D0;")  # Задаем цветную границу и цвет шрифта
        self.combo_box.view().setStyleSheet("color: #D0D0D0;")  # Задаем цвет шрифта в выпадающем списке
        # Получаем список доступных COM-портов
        com_ports = serial.tools.list_ports.comports()
        # Заполняем выпадающий список COM-портами
        for port in com_ports:
            self.combo_box.addItem(port.description)

        self.serial = None

        layout = QVBoxLayout(self.main_window_frame)
        layout.setContentsMargins(20, 0, 420, 0)  # Устанавливаем отступы макета
        layout.addWidget(self.combo_box)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("D:/git/AQtech/AQtech Tool MAX/Icons/Splash.png"))
    splash.show()

    # Имитация загрузки (можно заменить на вашу реализацию)
    time.sleep(2)  # Например, 2 секунды

    window = MainWindow()
    #window.showMaximized()
    window.show()
    splash.close()
    sys.exit(app.exec_())
