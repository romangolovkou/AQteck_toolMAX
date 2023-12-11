from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QFrame, QMenu

from AQ_EventManager import AQ_EventManager
from AqBaseDevice import AqBaseDevice
from ui_AqLeftDeviceWidget import Ui_AqLeftDeviceWidget


class AqLeftWidgetPanelFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.event_manager = self.event_manager = AQ_EventManager.get_global_event_manager()
        # self.event_manager.register_event_handler("new_devices_added", self.add_dev_widgets_to_left_panel)
        self.event_manager.register_event_handler("delete_device", self.remove_dev_widget_from_left_panel)

    # def add_dev_widgets_to_left_panel(self, new_devices):
    #     for i in range(len(new_devices)):
    #         dev_widget = AqLeftDeviceWidget(new_devices[i], self)
    #         self.left_panel_layout.insertWidget(dev_widget)

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

class AqLeftDeviceWidget(QWidget):
    def __init__(self, device: AqBaseDevice, parent=None):
        super().__init__(parent)
        self.ui = Ui_AqLeftDeviceWidget()
        self.ui.setupUi(self)
        self.device: AqBaseDevice = device
        self.event_manager = self.event_manager = AQ_EventManager.get_global_event_manager()
        self.is_active_now = 1

        # Наповпнюємо віджет текстовими мітками
        self.ui.deviceName.setText(self.device.info('name'))
        self.ui.deviceAddress.setText(self.device.info('address'))
        serial = self.device.info('serial_num')
        if serial is None:
            serial = ''
        self.ui.deviceSerial.setText('S/N' + serial)
        # Создаем палитру с фоновыми цветами
        self.normal_palette = self.palette()
        self.hover_palette = QPalette()
        self.hover_palette.setColor(QPalette.Window, QColor("#16191d"))
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
        child_widgets = self.parent().findChildren(AqLeftDeviceWidget)
        for child_widget in child_widgets:
            if not child_widget == self:
                # child_widget.background_field.setStyleSheet("background-color: transparent;")
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
        action_read.triggered.connect(lambda: self.device.read_parameters())
        action_write.triggered.connect(lambda: self.device.write_parameters())
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

class AqLeftPanelAddWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.event_manager = AQ_EventManager.get_global_event_manager()
        # Создаем палитру с фоновыми цветами
        self.normal_palette = self.palette()
        self.hover_palette = QPalette()
        self.hover_palette.setColor(QPalette.Window, QColor("#16191d"))
        self.setPalette(self.hover_palette)

    def enterEvent(self, event):
        # Применяем палитру при наведении
        self.setPalette(self.hover_palette)
        self.setAutoFillBackground(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Возвращаем обычную палитру при уходе курсора
        self.setPalette(self.normal_palette)
        self.setAutoFillBackground(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('widget "openAddDeviceWindow" was called')
            self.event_manager.emit_event('open_AddDevices')
        super().mousePressEvent(event)
