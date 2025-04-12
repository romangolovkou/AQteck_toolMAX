from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QColor
from PySide2.QtWidgets import QWidget, QFrame, QMenu

import AqUiWorker
from AQ_EventManager import AQ_EventManager
from AqBaseDevice import AqBaseDevice
from AqTranslateManager import AqTranslateManager
from ui_AqLeftDeviceWidget import Ui_AqLeftDeviceWidget

from PySide2.QtCore import Qt, Signal

class AqLeftWidgetPanelFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.event_manager = AQ_EventManager.get_global_event_manager()
        self.active_style = """* {background-color: #16191d; 
                                border-top-left-radius: 5px;
	                            border-bottom-left-radius: 5px;}"""
        self.not_active_style = """* {background-color: #2c313c;
                                border-top-left-radius: 5px;
                                border-bottom-left-radius: 5px;}"""
        self.hover_style = """* {background-color: #202339; 
                                border-top-left-radius: 5px;
	                            border-bottom-left-radius: 5px;}"""
        self.group = list()

        self.event_manager.register_event_handler("new_devices_added", self.addDevice)
        self.event_manager.register_event_handler("delete_device", self.deleteDevice)

    def addDevice(self, new_devices):
        for device in new_devices:
            widget = AqLeftDeviceWidget(device, self)
            widget.cstm_clicked.connect(self.onWidgetClicked)
            self.group.append(widget)
            self.onWidgetClicked(widget)
            self.layout().insertWidget(0, widget)

    def deleteDevice(self, device):
        delete_pos = None
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget.device == device:
                self.layout().removeWidget(widget)
                self.group.remove(widget)
                widget.deleteLater()
                delete_pos = i
                break

        if delete_pos is not None:
            try:
                widget = self.layout().itemAt(delete_pos).widget()
                self.onWidgetClicked(widget)
            except:
                try:
                    widget = self.layout().itemAt(delete_pos - 1).widget()
                    self.onWidgetClicked(widget)
                except Exception as e:
                    print(f"Error occurred: {str(e)}")
                    print(f"Немає жодного пристрою")

    def onWidgetClicked(self, pressed_widget):
        for widget in self.group:
            widget.setStyleSheet(self.not_active_style)
            widget.is_active_now = False

        pressed_widget.setStyleSheet(self.active_style)
        pressed_widget.is_active_now = True
        self.setActiveDevice(pressed_widget.device)

    def setActiveStyleSheet(self, style):
        self.active_style = style

    def setNotActiveStyleSheet(self, style):
        self.not_active_style = style

    def setActiveDevice(self, device):
        self.event_manager.emit_event('set_active_device', device)

class AqLeftDeviceWidget(QWidget):
    cstm_clicked = Signal(object)
    def __init__(self, device: AqBaseDevice, parent=None):
        super().__init__(parent)
        self.ui = Ui_AqLeftDeviceWidget()
        self.ui.setupUi(self)
        self.event_manager = AQ_EventManager.get_global_event_manager()
        self.device: AqBaseDevice = device
        self.hide()
        self.setStyleSheet(self.parent().active_style)
        # self.setAutoFillBackground(True)
        self._is_active_now = True
        self.show()
        # Наповпнюємо віджет текстовими мітками
        self.ui.deviceName.setText(self.device.info('name'))
        self.ui.deviceAddress.setText(self.device.info('address'))
        serial = self.device.info('serial_num')
        if serial is None:
            serial = ''
        self.ui.deviceSerial.setText('S/N' + serial)

    @property
    def is_active_now(self):
        return self._is_active_now

    @is_active_now.setter
    def is_active_now(self, state: bool):
        self._is_active_now = state

    def enterEvent(self, event):
        # Применяем палитру при наведении
        if self.is_active_now is False:
            self.setStyleSheet(self.parent().hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Возвращаем обычную палитру при уходе курсора
        if self.is_active_now is False:
            self.setStyleSheet(self.parent().not_active_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.cstm_clicked.emit(self)
            # Эта функция будет вызвана при нажатии левой кнопки мыши на виджет
            print("Левая кнопка мыши нажата на виджет!")
        super().mousePressEvent(event)

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
        action_read = context_menu.addAction(AqTranslateManager.tr("Read parameters"))
        action_write = context_menu.addAction(AqTranslateManager.tr("Write parameters"))
        action_delete = context_menu.addAction(AqTranslateManager.tr("Delete device"))
        action_save_config = context_menu.addAction(AqTranslateManager.tr("Save configuration"))
        action_load_config = context_menu.addAction(AqTranslateManager.tr("Load configuration"))
        # Подключаем обработчик события выбора действия
        action_read.triggered.connect(lambda: self.device.read_parameters(message_feedback_address='main'))
        action_write.triggered.connect(lambda: self.device.write_parameters(message_feedback_address='main'))
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

    def enterEvent(self, event):
        self.setStyleSheet(self.parent().hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.parent().not_active_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('widget "openAddDeviceWindow" was called')
            AqUiWorker.show_add_device_window()
        super().mousePressEvent(event)
