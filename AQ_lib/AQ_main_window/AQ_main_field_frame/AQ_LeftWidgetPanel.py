from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont, QPalette, QColor
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QLabel, QMenu

from AQ_Devices import AQ_Device
from AQ_CustomWindowTemplates import AQ_Label


class AQ_left_widget_panel_frame(QFrame):
    def __init__(self, event_manager, parent=None):
        super().__init__(parent)
        self.event_manager = event_manager
        self.event_manager.register_event_handler("new_devices_added", self.add_dev_widgets_to_left_panel)
        self.event_manager.register_event_handler("delete_device", self.remove_dev_widget_from_left_panel)
        self.setStyleSheet("background-color: transparent;")
        self.left_panel_layout = QVBoxLayout(self)
        self.left_panel_layout.setAlignment(Qt.AlignTop)  # Установка выравнивания вверху макета
        self.left_panel_layout.setContentsMargins(4, 4, 4, 4)

    def add_dev_widgets_to_left_panel(self, new_devices):
        for i in range(len(new_devices)):
            dev_widget = AQ_left_device_widget(new_devices[i], self.event_manager, self)
            self.left_panel_layout.addWidget(dev_widget)

    def remove_dev_widget_from_left_panel(self, device):
        delete_pos = None
        for i in range(self.left_panel_layout.count()):
            widget = self.left_panel_layout.itemAt(i).widget()
            if widget.device == device:
                self.left_panel_layout.removeWidget(widget)
                widget.deleteLater()
                delete_pos = i
                break

        if delete_pos is not None:
            try:
                widget = self.left_panel_layout.itemAt(delete_pos).widget()
                widget.set_active_cur_widget()
            except:
                try:
                    widget = self.left_panel_layout.itemAt(delete_pos - 1).widget()
                    widget.set_active_cur_widget()
                except Exception as e:
                    print(f"Error occurred: {str(e)}")
                    print(f"Немає жодного пристрою")




class AQ_left_device_widget(QWidget):
    def __init__(self, device: AQ_Device, event_manager, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.device: AQ_Device = device
        self.event_manager = event_manager
        self.is_active_now = 1
        self.setFixedHeight(70)
        self.setMinimumWidth(240)
        # Створюємо фонове поле для відображення підсвітки активного приладу в момент додавання нового девайсу
        # поле використовується тільки один раз для підсвітки одразу після додавання нового приладу, оскільки
        # стандартні палітри чомусь не працюють на момент створення віджету.
        self.background_field = QFrame(self)
        self.background_field.setGeometry(0, 0, 240, 70)
        self.background_field.setStyleSheet("background-color: #429061;")
        self.ico_label = QLabel(self)
        pixmap = QPixmap('Icons/test_Button.png')
        self.ico_label.setGeometry(0, 0, 40, 70)
        new_pixmap = pixmap.scaled(self.ico_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ico_label.setPixmap(new_pixmap)
        self.ico_label.setStyleSheet("background-color: transparent;")
        self.ico_label.show()
        # Наповпнюємо віджет текстовими мітками
        device_data = self.device.get_device_data()
        name = device_data.get('device_name', 'err_name')
        self.name_label = AQ_Label(name, self)
        font = QFont("Segoe UI", 14)
        self.name_label.setFont(font)
        self.name_label.move(50, 5)
        self.name_label.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent;")
        address = device_data.get('address', 'err_address')
        self.address_label = AQ_Label('address:' + address, self)
        self.address_label.move(50, 27)
        self.address_label.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent")
        serial = device_data.get('serial_number', 'err_serial_number')
        # self.serial_label = AQ_Label('S/N' + serial, self)
        # self.serial_label.move(50, 47)
        # self.serial_label.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent")

        # Создаем палитру с фоновыми цветами
        self.normal_palette = self.palette()
        self.hover_palette = QPalette()
        self.hover_palette.setColor(QPalette.Window, QColor("#429061"))
        self.setPalette(self.hover_palette)
        self.setAutoFillBackground(True)
        self.set_active_cur_widget()

    def enterEvent(self, event):
        # Применяем палитру при наведении
        if self.is_active_now == 0:
            self.setPalette(self.hover_palette)
            self.setAutoFillBackground(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Возвращаем обычную палитру при уходе курсора
        if self.is_active_now == 0:
            self.setPalette(self.normal_palette)
            self.setAutoFillBackground(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.set_active_cur_widget()

            # Эта функция будет вызвана при нажатии левой кнопки мыши на виджет
            print("Левая кнопка мыши нажата на виджет!")
        super().mousePressEvent(event)

    def set_active_cur_widget(self):
        child_widgets = self.parent.findChildren(AQ_left_device_widget)
        for child_widget in child_widgets:
            if not child_widget == self:
                child_widget.background_field.setStyleSheet("background-color: transparent;")
                child_widget.setPalette(self.normal_palette)
                child_widget.setAutoFillBackground(False)
                child_widget.is_active_now = 0

        self.setPalette(self.hover_palette)
        self.setAutoFillBackground(True)
        self.is_active_now = 1

        self.event_manager.emit_event('set_active_device', self.device)

    def contextMenuEvent(self, event):
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
        action_write = context_menu.addAction("Write parameters")
        action_delete = context_menu.addAction("Delete device")
        action_save_config = context_menu.addAction("Save configuration")
        action_load_config = context_menu.addAction("Load configuration")
        # Подключаем обработчик события выбора действия
        action_read.triggered.connect(lambda: self.device.read_all_parameters())
        action_write.triggered.connect(lambda: self.device.write_all_parameters())
        action_delete.triggered.connect(lambda: self.event_manager.emit_event('delete_device', self.device))
        action_save_config.triggered.connect(lambda: self.event_manager.emit_event('save_device_configuration', self.device))
        action_load_config.triggered.connect(lambda: self.event_manager.emit_event('load_device_configuration', self.device))
        # if self.traverse_items_R_Only_catalog_check(item) > 0:
        #     action_write = context_menu.addAction("Write parameters")
        #     have_error = self.travers_have_error_check(index)
        #     if have_error > 0:
        #         action_write.setDisabled(True)
        #     # Подключаем обработчик события выбора действия
        #     action_write.triggered.connect(lambda: self.write_catalog_by_modbus(index, 1))
        # # Показываем контекстное меню
        context_menu.exec(event.globalPos())

