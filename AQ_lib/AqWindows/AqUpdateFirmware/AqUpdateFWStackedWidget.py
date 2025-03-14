import time
from functools import partial
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import QStackedWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QProgressBar, QWidget
from AQ_EventManager import AQ_EventManager
from AppCore import Core
from AqAddDeviceWindow import ReinitDeviceWithPassThread
from AqAutoDetectionDevice import AqAutoDetectionDevice
from AqConnectManager import AqConnectManager
from AqMessageManager import AqMessageManager
from AqSettingsFunc import AqSettingsManager
from AqTranslateManager import AqTranslateManager
from AqUpdateFinalWaitTread import UpdateFinalWaitTread


class AqUpdateFWViewManager(QStackedWidget):
    message_signal = Signal(str, str)
    anim_start_signal = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.event_manager = AQ_EventManager.get_global_event_manager()
        self._message_manager = AqMessageManager.get_global_message_manager()

        self.message_signal.connect(partial(self._message_manager.show_message, self))
        self._message_manager.subscribe('updateFW', self.message_signal.emit)

        self._update_device = None
        self.progress_bar_is_active = False
        #ui_elements
        #first page
        self.main_ui_elements = None
        self.devNameLabel = None
        self.devSnLabel = None
        self.filePathBtn = None
        self.filePathLineEdit = None
        self.updateRunBtn = None
        self.progressBar = None
        self.errorLabel = None
        self.successLabel = None
        self.waitLabel = None
        self.waitWidget = None


        self.event_manager.register_event_handler('set_update_device', self.set_update_device)

        # self.device_init_widget = DeviceInitWidget()
        # self.addWidget(self.device_init_widget)
        # self.setCurrentWidget(self.device_init_widget)
        self.show()

    def prepare_ui(self):
        self.devNameLabel = self.parent().findChild(QLabel, 'devNameLabel')
        self.devSnLabel = self.parent().findChild(QLabel, 'devSnLabel')
        self.filePathBtn = self.findChild(QPushButton, 'filePathBtn')
        self.filePathLineEdit = self.findChild(QLineEdit, 'filePathLineEdit')
        self.updateRunBtn = self.findChild(QPushButton, 'updateRunBtn')
        self.progressBar = self.findChild(QProgressBar, 'progressBar')
        self.errorLabel = self.findChild(QLabel, 'errorLabel')
        self.successLabel = self.findChild(QLabel, 'successLabel')
        self.waitLabel = self.findChild(QLabel, 'waitLabel')
        self.waitWidget = self.findChild(QLabel, 'waitWidget')

        self.main_ui_elements = [
            self.devNameLabel,
            self.devSnLabel,
            self.filePathBtn,
            self.filePathLineEdit,
            self.updateRunBtn,
            self.progressBar,
            self.errorLabel,
            self.successLabel,
            self.waitLabel,
            self.waitWidget
        ]

        for i in self.main_ui_elements:
            if i is None:
                raise Exception(self.objectName() + ' Error: lost UI element')

        self.devNameLabel.setText(self.update_device.name)
        self.devNameLabel.show()
        self.devSnLabel.setText(self.update_device.info('serial_num'))
        self.devSnLabel.show()

        self.filePathBtn.clicked.connect(self.open_file_btn_clicked)
        self.updateRunBtn.clicked.connect(self.update_btn_clicked)

        self.errorLabel.hide()
        self.successLabel.hide()
        self.waitLabel.hide()
        self.waitWidget.set_movie_size(self.waitWidget.width(), self.waitWidget.height())

        self.anim_start_signal.connect(self.waitWidget.start_animation)

        self.setCurrentIndex(0)

    @property
    def update_device(self):
        return self._update_device

    @update_device.setter
    def update_device(self, device):
        self._update_device = device
        self._update_device.connect_progress.connect(self.progress_update)

    def progress_update(self, value, servise_msg):
        if servise_msg == 'write_file' and self.progress_bar_is_active:
            self.progressBar.setValue(value)

    def open_file_btn_clicked(self):
        # Начальный путь для диалога
        initial_path = AqSettingsManager.get_last_path('updateFW_path')
        if initial_path == '':
            initial_path = "C:/"

        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', initial_path, '*.fw')
        if file_path:
            self.filePathLineEdit.setText(file_path)
            AqSettingsManager.save_last_path('updateFW_path', file_path)

    def update_btn_clicked(self):
        self.event_manager.emit_event('FW_update_close_btn_block', True)
        file_path = self.filePathLineEdit.text()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    byte_array = file.read()
                try:
                    self.progress_bar_is_active = True
                    self._update_device.write_update_file(byte_array, self.update_file_loaded_callback)
                except Exception as e:
                    self.progress_bar_is_active = False
                    self.event_manager.emit_event('FW_update_close_btn_block', False)
            except Exception as e:
                self._message_manager.send_message('updateFW',
                                                   'Error',
                                                   AqTranslateManager.tr('Read file failed!'))
                self.event_manager.emit_event('FW_update_close_btn_block', False)

        self.setCurrentIndex(1)

        return

    def update_file_loaded_callback(self, status):
        if status == 'ok':
            self.start_final_wait()

    def set_update_device(self, device):
        self.update_device = device
        self.prepare_ui()

    def start_final_wait(self):
        self.setCurrentIndex(2)
        self.anim_start_signal.emit()
        self.waitLabel.show()
        self.final_wait_thread = UpdateFinalWaitTread(self.final_wait)
        # self.init_calib_thread.finished.connect(self.search_finished)
        self.final_wait_thread.error.connect(self.fw_update_error)
        self.final_wait_thread.result_signal.connect(self.device_updated)
        self.final_wait_thread.start()

    def final_wait(self):
        wait_cnt = 0
        time.sleep(8)
        self._update_device.reboot()
        time.sleep(30)
        while not self._update_device.check_device_update_fw():
            print('wait check device name')
            time.sleep(10)
            wait_cnt += 1
            if wait_cnt > 10:
                return False

        return True

    def device_updated(self, result):
        try:
            if result:
                saved_connect = self._update_device.get_connect()
                saved_password = self._update_device.get_password()
                try:
                    # device = AqAutoDetectionDevice(self.event_manager, saved_connect, saved_password)
                    self.event_manager.emit_event('delete_device', self._update_device)
                    device = AqAutoDetectionDevice(self.event_manager, saved_connect, saved_password)
                    AqConnectManager.connect_list.append(device.get_connect())
                    device.init_parameters()
                    self.event_manager.emit_event('add_new_devices', [device])
                except Exception as e:
                    print(f"{str(e)}")
                    self.fw_update_error()

                self.waitLabel.hide()
                self.errorLabel.hide()
                self.successLabel.show()
                self.waitWidget.stop_animation()
                self._message_manager.send_message('updateFW',
                                                   'Success',
                                                   AqTranslateManager.tr('The device successfully updated.'))
                self.event_manager.emit_event('FW_update_close_btn_block', False)

            else:
                self.fw_update_error()

        except Exception as e:
            self.waitLabel.hide()
            self.errorLabel.show()
            self.successLabel.hide()
            self.waitWidget.stop_animation()
            self._message_manager.send_message('updateFW',
                                               'Error',
                                               AqTranslateManager.tr(
                                                   'Something failed! Close update window and try again.'))
            self.event_manager.emit_event('FW_update_close_btn_block', False)

    def fw_update_error(self):
        self.waitLabel.hide()
        self.errorLabel.show()
        self.successLabel.hide()
        self.waitWidget.stop_animation()
        self._message_manager.send_message('updateFW',
                                           'Error',
                                           AqTranslateManager.tr(
                                               'Firmware update failed! Close update window and try again.'))
        self.event_manager.emit_event('FW_update_close_btn_block', False)
