import time
from functools import partial
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import QStackedWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QProgressBar, QWidget
from AQ_EventManager import AQ_EventManager
from AqCalibCreator import AqCalibCreator
from AqCalibrator import AqCalibrator
from AqInitCalibTread import InitCalibThread
from AqMessageManager import AqMessageManager
from AqSettingsFunc import AqSettingsManager
from AqTranslateManager import AqTranslateManager
from AqUpdateFinalWaitTread import UpdateFinalWaitTread


class AqUpdateFWViewManager(QStackedWidget):
    message_signal = Signal(str, str)

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
        self.waitWidget = self.findChild(QWidget, 'waitWidget')

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
            except Exception as e:
                self._message_manager.send_message('updateFW',
                                                   'Error',
                                                   AqTranslateManager.tr('Read file failed!'))

        self.setCurrentIndex(1)

        return

    def update_file_loaded_callback(self, status):
        if status == 'ok':
            self.start_final_wait()

    def set_update_device(self, device):
        self.update_device = device
        # self.start_init_calibrator()
        self.prepare_ui()

    def start_final_wait(self):
        self.setCurrentIndex(2)
        self.waitWidget.start_animation()
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
            time.sleep(2)
            wait_cnt += 1
            if wait_cnt > 10:
                return False

        return True

    def device_updated(self, result):
        try:
            if result:
                self.waitLabel.hide()
                self.errorLabel.hide()
                self.successLabel.show()
                self.waitWidget.stop_animation()
                self._message_manager.send_message('updateFW',
                                                   'Success',
                                                   AqTranslateManager.tr('The device successfully updated.'))
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

    def fw_update_error(self):
        self.waitLabel.hide()
        self.errorLabel.show()
        self.successLabel.hide()
        self.waitWidget.stop_animation()
        self._message_manager.send_message('updateFW',
                                           'Error',
                                           AqTranslateManager.tr(
                                               'Firmware update failed! Close update window and try again.'))




