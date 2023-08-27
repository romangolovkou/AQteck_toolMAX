from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QFrame, QGraphicsView, QGraphicsScene, \
                            QGraphicsPixmapItem, QTableWidget, QTableWidgetItem, QCheckBox
from custom_window_templates import AQDialog, AQComboBox, AQLabel, IP_AQLineEdit, Slave_ID_AQLineEdit
from custom_exception import Connect_err
import serial.tools.list_ports
from AQ_communication_func import is_valid_ip
from AQ_settings_func import save_current_text_value, save_combobox_current_state, load_last_text_value, \
                             load_last_combobox_state
from AQ_network_frame import AQ_network_settings_frame


class AQ_DialogAddDevices(AQDialog):
    def __init__(self, event_manager, devices_list, parent):
        super().__init__('Add Devices')

        PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'

        self.setObjectName("AQ_Dialog_add_device")
        self.parent = parent
        self.screen_geometry = QApplication.desktop().screenGeometry()
        self.move(self.screen_geometry.width() // 2 - self.width() // 2,
                  self.screen_geometry.height() // 2 - self.height() // 2,)

        # Создаем QGraphicsPixmapItem и добавляем его в сцену
        self.gear_big = RotatingGear(QPixmap(PROJ_DIR + 'Icons/gear182.png'), 40, 1)

        # Создаем виджет QGraphicsView и устанавливаем его для окна
        self.gear_big_view = QGraphicsView(self)
        self.gear_big_view.setStyleSheet("background: transparent;")
        self.gear_big_view.setFrameStyle(QFrame.NoFrame)  # Убираем рамку
        self.gear_big_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Создаем сцену и устанавливаем ее для виджета
        self.gear_big_scene = QGraphicsScene(self)
        self.gear_big_scene.addItem(self.gear_big)
        self.gear_big_view.setScene(self.gear_big_scene)
        self.gear_big_view.setGeometry(700, 500, 182, 182)

        # Создаем QGraphicsPixmapItem и добавляем его в сцену
        self.gear_small = RotatingGear(QPixmap(PROJ_DIR + 'Icons/gear127.png'), 40, 4)

        # Создаем виджет QGraphicsView и устанавливаем его для окна
        self.gear_small_view = QGraphicsView(self)
        self.gear_small_view.setStyleSheet("background: transparent;")
        self.gear_small_view.setFrameStyle(QFrame.NoFrame)  # Убираем рамку
        self.gear_small_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Создаем сцену и устанавливаем ее для виджета
        self.gear_small_scene = QGraphicsScene(self)
        self.gear_small_scene.addItem(self.gear_small)
        self.gear_small_view.setScene(self.gear_small_scene)
        self.gear_small_view.setGeometry(610, 540, 127, 127)

        # Створюємо фрейм з налаштуваннями з'єднання
        self.network_settings_frame = AQ_network_settings_frame(event_manager, self)
        self.network_settings_frame.setGeometry(25, self.title_bar_frame.height() + 2, int(self.width() * 0.4),
                                                self.height() - self.title_bar_frame.height() - 4)

        # Создаем QTableWidget с 4 столбцами
        self.table_widget = QTableWidget(self.main_window_frame)
        self.table_widget.setColumnCount(4)
        self.table_widget.horizontalHeader().setMinimumSectionSize(8)

        # Добавляем заголовки столбцов
        self.table_widget.setHorizontalHeaderLabels(["", "Name", "Address", "Version"])
        self.table_widget.move(self.main_window_frame.width()//2 - 28, self.title_bar_frame.height() + 5)
        self.table_widget.setFixedWidth(self.main_window_frame.width()//2 + 20)
        # Устанавливаем ширину столбцов
        cur_width = self.table_widget.width()
        self.table_widget.setColumnWidth(0, int(cur_width * 0.05))
        self.table_widget.setColumnWidth(1, int(cur_width * 0.48))
        self.table_widget.setColumnWidth(2, int(cur_width * 0.27))
        self.table_widget.setColumnWidth(3, int(cur_width * 0.20))
        # Установите высоту строк по умолчанию
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        # Убираем рамку таблицы
        self.table_widget.setStyleSheet("""QTableWidget { border: none; color: #D0D0D0;}
                                           QTableWidget::item { padding-left: 3px; }""")

        self.finded_dev_count = 0

    def set_style_table_widget(self, row, err_flag=0):
        if err_flag == 0:
            # self.table_widget.setStyleSheet("""QTableWidget { border: none; color: #D0D0D0;}
            #                                 QTableWidget::item { padding-left: 3px; background-color: #429061}""")
            for i in range(4):
                self.table_widget.item(row, i).setBackground(QColor("#429061"))
        else:
            # self.table_widget.setStyleSheet("""QTableWidget { border: none; color: #D0D0D0;}
            #                                             QTableWidget::item { padding-left: 3px; background-color: #9d4d4f}""")
            for i in range(4):
                self.table_widget.item(row, i).setBackground(QColor("#9d4d4f"))

    def handle_combobox_selection(self):
        selected_item = self.interface_combo_box.currentText()
        if selected_item == "Ethernet":
            self.ip_line_edit_label.setVisible(True)
            self.ip_line_edit.setVisible(True)
            self.slave_id_line_edit_label.setVisible(False)
            self.slave_id_line_edit.setVisible(False)
        else:
            self.ip_line_edit_label.setVisible(False)
            self.ip_line_edit.setVisible(False)
            self.slave_id_line_edit_label.setVisible(True)
            self.slave_id_line_edit.setVisible(True)

    def add_device_to_table_widget(self, index, device_data, err_flag = 0):
        self.table_widget.setRowCount(index + 1)
        # Создаем элементы таблицы для каждой строки
        self.checkbox_item = QTableWidgetItem()
        self.name_item = QTableWidgetItem(device_data.get('device_name') + ' S/N' + device_data.get('serial_number'))
        self.name_item.setFlags(self.name_item.flags() & ~Qt.ItemIsEditable)
        self.address_item = QTableWidgetItem(device_data.get('address'))
        self.address_item.setFlags(self.address_item.flags() & ~Qt.ItemIsEditable)
        self.version_item = QTableWidgetItem(device_data.get('version'))
        self.version_item.setFlags(self.version_item.flags() & ~Qt.ItemIsEditable)

        # Устанавливаем элементы таблицы
        self.table_widget.setItem(index, 0, self.checkbox_item)
        self.table_widget.setItem(index, 1, self.name_item)
        self.table_widget.setItem(index, 2, self.address_item)
        self.table_widget.setItem(index, 3, self.version_item)
        new_height = self.table_widget.height() + self.table_widget.rowHeight(index)
        if new_height > 420:
            new_height = 420
        self.table_widget.setFixedHeight(new_height)

        # Устанавливаем чекбокс в первую колонку
        checkbox = QCheckBox()
        if err_flag == 0:
            checkbox.setChecked(True)
        else:
            checkbox.setChecked(False)
            checkbox.setEnabled(False)

        checkbox.setStyleSheet("QCheckBox { background-color: transparent; border: none;}")
        self.table_widget.setCellWidget(index, 0, checkbox)
        item = self.table_widget.item(index, 0)
        item.setTextAlignment(Qt.AlignCenter)

        self.set_style_table_widget(self.finded_dev_count, err_flag)

        bottom_right_corner_table_widget = self.table_widget.mapTo(self.main_window_frame, self.table_widget.rect().bottomRight())

        if hasattr(self, 'add_btn'):
            self.add_btn.deleteLater()
        # Создаем кнопку поиска
        self.add_btn = QPushButton("Add device", self.main_window_frame)
        self.add_btn.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.add_btn.setFixedSize(100, 35)
        self.add_btn.move(bottom_right_corner_table_widget.x() - self.add_btn.width() - 3,
                          bottom_right_corner_table_widget.y() + 5)
        self.add_btn.clicked.connect(self.add_finded_devices)
        self.add_btn.setStyleSheet("""
                    QPushButton {
                        border-left: 1px solid #9ef1d3;
                        border-top: 1px solid #9ef1d3;
                        border-bottom: 1px solid #5bb192;
                        border-right: 1px solid #5bb192;
                        color: #D0D0D0;
                        background-color: #2b2d30;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #3c3e41;
                    }
                    QPushButton:pressed {
                        background-color: #429061;
                    }
                """)
        # if err_flag != 0:
        #     self.add_btn.setEnabled(False)
        #     self.add_btn.setStyleSheet("""
        #                         QPushButton {
        #                             border-left: 1px solid #9ef1d3;
        #                             border-top: 1px solid #9ef1d3;
        #                             border-bottom: 1px solid #5bb192;
        #                             border-right: 1px solid #5bb192;
        #                             color: #3c3e41;
        #                             background-color: #2b2d30;
        #                             border-radius: 4px;
        #                         }
        #                         QPushButton:hover {
        #                             background-color: #3c3e41;
        #                         }
        #                         QPushButton:pressed {
        #                             background-color: #429061;
        #                         }
        #                     """)

        self.add_btn.show()

    def add_finded_devices(self):
        devices_count = self.table_widget.rowCount()
        for i in range(devices_count):
            checkbox_item = self.table_widget.cellWidget(i, 0)
            if checkbox_item is not None and isinstance(checkbox_item, QCheckBox):
                if checkbox_item.checkState() == Qt.Checked:
                    item = self.table_widget.item(i, 2)
                    dev_address = item.text()
                    for j in range(len(self.parent.ready_to_add_devices)):
                        ready_device_data = self.parent.ready_to_add_devices[j]
                        if dev_address == ready_device_data.get('address', ''):
                            self.parent.devices.append(self.parent.ready_to_add_devices[j])
                            # Видаляємо зі списку ready доданий девайс
                            self.parent.ready_to_add_devices.pop(j)
                            self.parent.add_tree_view()
                            break
                else:
                    print("Галочка не установлена")

    def connect_finished(self, device_data):
        if isinstance(device_data, dict):
            default_prg = device_data.get('default_prg')
        else:
            default_prg = device_data
        self.gear_small.stop()
        self.gear_big.stop()
        if default_prg == 'connect_err':
            self.show_connect_err_label()
        elif default_prg == 'empty_field_slave_id':
            self.slave_id_line_edit.red_blink_timer.start()
            self.slave_id_line_edit.show_err_label()
        elif default_prg == 'empty_field_ip' or default_prg == 'invalid_ip':
            self.ip_line_edit.red_blink_timer.start()
            self.ip_line_edit.show_err_label()
        elif default_prg == 'decrypt_err':
            self.add_device_to_table_widget(self.finded_dev_count, device_data, 1)
            self.finded_dev_count += 1
        else:
            try:
                self.parent.parse_default_prg(default_prg)
                self.parent.add_data_to_ready_devices(device_data)
                self.add_device_to_table_widget(self.finded_dev_count, device_data, 0)
                self.finded_dev_count += 1
            except:
                self.add_device_to_table_widget(self.finded_dev_count, device_data, 1)
                self.finded_dev_count += 1

    def on_find_button_clicked(self):
        self.gear_small.start()
        self.gear_big.start()
        # Запускаем функцию connect_to_device в отдельном потоке
        self.connect_thread = ConnectDeviceThread(self)
        self.connect_thread.finished.connect(self.on_connect_thread_finished)
        self.connect_thread.error.connect(self.on_connect_thread_error)
        self.connect_thread.result_signal.connect(self.connect_finished)
        self.connect_thread.start()

    def on_connect_thread_finished(self):
        # Выполняется после успешного завершения connect_to_device
        # В этом слоте можно выполнить действия, которые должны произойти после завершения функции
        self.gear_small.stop()
        self.gear_big.stop()

    def on_connect_thread_error(self, error_message):
        # Выполняется в случае ошибки при выполнении connect_to_device
        # В этом слоте можно выполнить действия, которые должны произойти в случае ошибки
        self.show_connect_err_label()
        self.gear_small.stop()
        self.gear_big.stop()


    def connect_to_device (self):
        selected_item = self.interface_combo_box.currentText()
        save_combobox_current_state(self.parent.auto_load_settings, self.interface_combo_box)
        device_data = {}
        if selected_item == "Ethernet":
            try:
                ip = self.ip_line_edit.text()
            except:
                return 'empty_field_ip'
            if not is_valid_ip(ip):
                return 'invalid_ip'

            save_current_text_value(self.parent.auto_load_settings, self.ip_line_edit)

            try:
                device_data = self.parent.connect_to_device_IP(ip)
                device_data['address'] = str(ip)
            except Connect_err:
                self.show_connect_err_label()

            return device_data
        else:
            try:
                slave_id = int(self.slave_id_line_edit.text())
            except:
                return 'empty_field_slave_id'
            for port in self.com_ports:
                if port.description == selected_item:
                    save_current_text_value(self.parent.auto_load_settings, self.slave_id_line_edit)
                    selected_port = port.device
                    try:
                        device_data = self.parent.connect_to_device_COM(selected_port, slave_id)
                        device_data['address'] = str(slave_id) + ' (' + str(selected_port) + ')'
                    except Connect_err:
                        self.show_connect_err_label()

                    break

            return device_data

    def show_connect_err_label(self):
        # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
        self.connect_err_label = AQLabel("<html>The connection to device could not be established.<br>Check the connection lines and network parameters and repeat the search.<html>", self)
        self.connect_err_label.setStyleSheet("background-color: #9d2d30; color: #D0D0D0; \n")
        self.connect_err_label.setFont(QFont("Verdana", 12))  # Задаем шрифт и размер
        self.connect_err_label.setAlignment(Qt.AlignCenter)
        self.connect_err_label.setFixedSize(self.width(), 50)
        self.connect_err_label.move(0, self.height())
        self.connect_err_label.show()
        # Создаем анимацию для перемещения плашки вверх и вниз
        self.animation = QPropertyAnimation(self.connect_err_label, b"geometry")
        # Показываем плашку с помощью анимации
        start_rect = self.connect_err_label.geometry()
        end_rect = QRect(start_rect.x(), start_rect.y() - 50, start_rect.width(), start_rect.height())
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.setDuration(800)  # Продолжительность анимации в миллисекундах
        self.animation.start()

        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.hide_connect_err_label)
        # Устанавливаем задержку в 2 секунды и затем удаляем метку
        # QTimer.singleShot(4000, self.connect_err_label.deleteLater)

    def hide_connect_err_label(self):
        # Скрываем плашку с помощью анимации
        start_rect = self.connect_err_label.geometry()
        end_rect = QRect(start_rect.x(), start_rect.y() + 50, start_rect.width(), start_rect.height())
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.setDuration(800)  # Продолжительность анимации в миллисекундах
        self.animation.start()


class ConnectDeviceThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result_signal = pyqtSignal(object)  # Сигнал для передачи данных в главное окно
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            # Здесь выполняем ваш код функции connect_to_device
            # self.parent.connect_to_device()
            result_data = self.parent.connect_to_device()  # Данные, которые нужно передать в главное окно
            self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
            # По завершении успешного выполнения
            self.finished.emit()
        except Exception as e:
            # В случае ошибки передаем текст ошибки обратно в главный поток
            self.error.emit(str(e))


class RotatingGear(QGraphicsPixmapItem):
    def __init__(self, pixmap, interval, angle_degree):
        super().__init__()
        self.setPixmap(pixmap)
        self.setTransformOriginPoint(self.boundingRect().center())
        self.angle = 0
        self.angle_rotate = angle_degree
        self.interval = interval
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate_gear)

    def rotate_gear(self):
        self.angle += self.angle_rotate  # Угол поворота в градусах
        self.setRotation(self.angle)

    def start(self):
        self.timer.start(self.interval)  # Установите интервал вращения в миллисекундах

    def stop(self):
        self.timer.stop()