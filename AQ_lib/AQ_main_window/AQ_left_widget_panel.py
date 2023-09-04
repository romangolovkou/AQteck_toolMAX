from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QLabel, QScrollArea

from custom_window_templates import AQLabel


class AQ_left_widget_panel_frame(QFrame):
    def __init__(self, event_manager, parent=None):
        super().__init__(parent)
        self.event_manager = event_manager
        self.event_manager.register_event_handler("add_new_devices", self.add_dev_widgets_to_left_panel)
        self.setStyleSheet("background-color: transparent;")
        self.left_panel_layout = QVBoxLayout(self)
        self.left_panel_layout.setAlignment(Qt.AlignTop)  # Установка выравнивания вверху макета
        self.left_panel_layout.setContentsMargins(4, 4, 4, 4)

    def add_dev_widgets_to_left_panel(self, new_devices):
        for i in range(len(new_devices)):
            dev_widget = AQ_left_device_widget(new_devices[i], self.event_manager, self)
            self.left_panel_layout.addWidget(dev_widget)


class AQ_left_device_widget(QWidget):
    def __init__(self, device, event_manager, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.device = device
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
        self.name_label = AQLabel(name, self)
        font = QFont("Segoe UI", 14)
        self.name_label.setFont(font)
        self.name_label.move(50, 5)
        self.name_label.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent;")
        address = device_data.get('address', 'err_address')
        self.address_label = AQLabel('address:' + address, self)
        self.address_label.move(50, 27)
        self.address_label.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent")
        serial = device_data.get('serial_number', 'err_serial_number')
        self.serial_label = AQLabel('S/N' + serial, self)
        self.serial_label.move(50, 47)
        self.serial_label.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent")

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

