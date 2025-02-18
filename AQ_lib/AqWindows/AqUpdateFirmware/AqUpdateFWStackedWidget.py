from functools import partial
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import QStackedWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QProgressBar
from AQ_EventManager import AQ_EventManager
from AqCalibCreator import AqCalibCreator
from AqCalibrator import AqCalibrator
from AqInitCalibTread import InitCalibThread
from AqMessageManager import AqMessageManager
from AqTranslateManager import AqTranslateManager


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

        self.main_ui_elements = [
            self.devNameLabel,
            self.devSnLabel,
            self.filePathBtn,
            self.filePathLineEdit,
            self.updateRunBtn,
            self.progressBar
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
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', '', '*.fw')
        if file_path:
            self.filePathLineEdit.setText(file_path)

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
            self._update_device.reboot()

    def set_update_device(self, device):
        self.update_device = device
        # self.start_init_calibrator()
        self.prepare_ui()

    def start_init_calibrator(self):
        self.init_calib_thread = InitCalibThread(self.init_calibrator)
        # self.init_calib_thread.finished.connect(self.search_finished)
        self.init_calib_thread.error.connect(self.calib_init_error)
        self.init_calib_thread.result_signal.connect(self.calibrator_inited)
        self.init_calib_thread.start()

    def init_calibrator(self):
        if self.calib_device.read_calib_file():
            calib_path = 'temp/calib/'
            try:
                AqCalibCreator.prepare_json_file(calib_path + self.calib_device.name + '_calibr.json',
                                                 calib_path + 'current_calibr.json')
                # AqCalibCreator.prepare_json_file('test_files/FI210-8T_calibr.json', calib_path + 'current_calibr.json')
                data = AqCalibCreator.load_json(calib_path + 'current_calibr.json')

                AqCalibCreator.prepare_json_file(calib_path + self.calib_device.name + '.json',
                                                 calib_path + 'current_loc.json')
                # AqCalibCreator.prepare_json_file('test_files/FI210-8T.json', calib_path + 'current_loc.json')
                loc_data = AqCalibCreator.load_json(calib_path + 'current_loc.json')

                current_lang = AqTranslateManager.get_current_lang().lower()
                if current_lang == 'ua':
                    current_lang = 'uk'
                loc_data = loc_data[current_lang]

                calibrator = AqCalibrator(data, loc_data)
            except:
                self._message_manager.send_message('calib',
                                                   'Error',
                                                   AqTranslateManager.tr('Calibration file parsing failed!'))
                raise Exception('Calibration file parsing failed!')

            # Создаем объект AqCalibrator

            return calibrator
        else:
            self._message_manager.send_message('calib',
                                               'Error',
                                               AqTranslateManager.tr('Read calibration file failed! Close calibration window and try again.'))

    def calibrator_inited(self, calibrator):
        try:
            self.calibrator = calibrator
            self.calibrator.set_calib_device(self.calib_device)
            self.prepare_ui()
            self.calibrator_is_ready = True
        except:
            self.device_init_widget.stop_animation()
            self._message_manager.send_message('calib',
                                               'Error',
                                               AqTranslateManager.tr('Read calibration file failed! Close calibration window and try again.'))

    def calib_init_error(self):
        self._message_manager.send_message('calib',
                                           'Error',
                                           AqTranslateManager.tr('Calibrator init failed!'))

    def check_is_calibrator_ready(self):
        if self.calibrator_is_ready:
            self.setCurrentIndex(1)
            self.device_init_widget.stop_animation()
        else:
            self.device_init_widget.start_animation()
            self.setCurrentWidget(self.device_init_widget)
            # Устанавливаем задержку в 50 м.сек и затем повторяем
            QTimer.singleShot(50, lambda: self.check_is_calibrator_ready())




