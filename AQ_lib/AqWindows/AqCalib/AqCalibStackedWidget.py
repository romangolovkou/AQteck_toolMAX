import os
import random
import shutil
from collections import deque
from datetime import datetime
from functools import partial
from statistics import pstdev, mean

# import cairosvg
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QStandardItem, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QStackedWidget, QComboBox, QPushButton, QLabel, QLineEdit, QFrame

from AqBaseTreeItems import AqParamManagerItem
from AQ_EventManager import AQ_EventManager
from AqBaseDevice import AqBaseDevice
from AqCalibCoeffTable import AqCalibCoeffTable
from AqCalibCreator import AqCalibCreator
from AqCalibrator import AqCalibrator
from AqCurCalibValueTread import CurCalibValueThread
from AqInitCalibTread import InitCalibThread
from AqMessageManager import AqMessageManager
from AqTranslateManager import AqTranslateManager
from AqTreeView import AqTreeView
from AqTreeViewItemModel import AqTreeViewItemModel
from AqTypeValueWithErrCodeLib import check_err_code_in_value
from DeviceNotInitedWidget import DeviceInitWidget
from NoDevicesWidget import NoDeviceWidget

IMAGE_PREFIX = 'test_files/'

TOLERANCE_PERCENT = 0.01
WAIT_SAMPLES = 15

class AqCalibViewManager(QStackedWidget):
    message_signal = Signal(str, str)
    auto_next_step_signal = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        x = parent.parent()
        self.calibrator_is_ready = False
        self.event_manager = AQ_EventManager.get_global_event_manager()
        self.event_manager.register_event_handler('calib_close_steps', self.close_steps)
        self._message_manager = AqMessageManager.get_global_message_manager()

        self.message_signal.connect(partial(self._message_manager.show_message, self))
        self._message_manager.subscribe('calib', self.message_signal.emit)

        self.roaming_temp_folder = None

        self.samples = deque(maxlen=4)
        self.auto_next_step_signal.connect(self._step_run_btn_)
        self.auto_mode = False
        self.auto_mode_wait_count = 0

        self._calib_device = None
        self.calib_dev_mode = False
        self.calibrator = None
        self.user_settings = dict()
        #ui_elements
        #first page
        self.main_ui_elements = None
        self.pinTypeComboBox = None
        self.input_outputTypeComboBox = None
        self.channelsComboBox = None
        self.methodComboBox = None
        self.runCalibBtn = None
        # step page
        self.stepHeaderLabel = None
        self.stepStepsLabel = None
        self.stepDescrLabel_1 = None
        self.stepDescrLabel_2 = None
        self.stepDescrLabel_3 = None
        self.stepMeasureLabel = None
        self.stepMeasureLineEdit = None
        self.stepPicLabel = None
        self.stepPicture = None
        self.stepBackBtn = None
        self.stepRunBtn = None
        self.autoBtn = None
        self.tableWidget = None
        self.tableDescrLabel1 = None
        self.tableDescrLabel2 = None
        self.tableDescrLabel3 = None
        self.tableBackBtn = None
        self.tableWriteCoeffBtn = None
        self.devNameLabel = None
        self.devSnLabel = None
        self.currentCalibValueFrame = None
        self.currentCalibValueLabel = None
        self.currentCalibValueLineEdit = None
        self.cur_calib_value_thread = None

        self.event_manager.register_event_handler('set_calib_device', self.set_calib_device)
        self.event_manager.register_event_handler('calibrator_inited', self.calibrator_inited)
        self.event_manager.register_event_handler('set_calib_dev_mode', self.set_calib_dev_mode)

        self.device_init_widget = DeviceInitWidget()
        self.addWidget(self.device_init_widget)
        self.setCurrentWidget(self.device_init_widget)
        self.show()
        self.check_is_calibrator_ready()

    def prepare_ui(self):
        self.pinTypeComboBox = self.findChild(QComboBox, 'pinTypeComboBox')
        self.input_outputTypeComboBox = self.findChild(QComboBox, 'input_outputTypeComboBox')
        self.channelsComboBox = self.findChild(QComboBox, 'channelsComboBox')
        self.methodComboBox = self.findChild(QComboBox, 'methodComboBox')
        self.runCalibBtn = self.findChild(QPushButton, 'runCalibBtn')

        self.stepHeaderLabel = self.findChild(QLabel, 'headerLabel')
        self.stepStepsLabel = self.findChild(QLabel, 'stepsLabel')
        self.stepDescrLabel_1 = self.findChild(QLabel, 'descrLabel_1')
        self.stepDescrLabel_2 = self.findChild(QLabel, 'descrLabel_2')
        self.stepDescrLabel_3 = self.findChild(QLabel, 'descrLabel_3')
        self.stepMeasureLabel = self.findChild(QLabel, 'measureLabel')
        self.stepPicLabel = self.findChild(QLabel, 'picLabel')
        self.stepPicture = self.findChild(QLabel, 'picture')
        self.stepBackBtn = self.findChild(QPushButton, 'backBtn')
        self.stepRunBtn = self.findChild(QPushButton, 'runBtn')
        self.autoBtn = self.findChild(QPushButton, 'autoBtn')
        self.tableWidget = self.findChild(AqCalibCoeffTable, 'tableWidget')
        self.tableDescrLabel1 = self.findChild(QLabel, 'descrLabel2_1')
        self.tableDescrLabel2 = self.findChild(QLabel, 'descrLabel2_2')
        self.tableDescrLabel3 = self.findChild(QLabel, 'descrLabel2_3')
        self.tableBackBtn = self.findChild(QPushButton, 'backBtn2')
        self.tableWriteCoeffBtn = self.findChild(QPushButton, 'writeCoeffBtn')
        self.devNameLabel = self.parent().findChild(QLabel, 'devNameLabel')
        self.devSnLabel = self.parent().findChild(QLabel, 'devSnLabel')
        self.currentCalibValueFrame = self.findChild(QFrame, 'currentCalibValueFrame')
        self.currentCalibValueLabel = self.findChild(QLabel, 'currentCalibValueLabel')
        self.currentCalibValueLineEdit = self.findChild(QLineEdit, 'currentCalibValueLineEdit')
        stepMeasureIntLineEdit = self.stepMeasureLineEdit = self.findChild(QLineEdit, 'measureIntLineEdit')
        stepMeasureFloatLineEdit = self.findChild(QLineEdit, 'measureFloatLineEdit')

        self.main_ui_elements = [
            self.pinTypeComboBox,
            self.input_outputTypeComboBox,
            self.channelsComboBox,
            self.methodComboBox,
            self.runCalibBtn,
            self.stepHeaderLabel,
            self.stepStepsLabel,
            self.stepDescrLabel_1,
            self.stepDescrLabel_2,
            self.stepDescrLabel_3,
            self.stepMeasureLabel,
            self.stepPicLabel,
            self.stepPicture,
            self.stepBackBtn,
            self.stepRunBtn,
            self.autoBtn,
            self.tableWidget,
            self.tableDescrLabel1,
            self.tableDescrLabel2,
            self.tableDescrLabel3,
            self.tableBackBtn,
            self.tableWriteCoeffBtn,
            self.devNameLabel,
            self.devSnLabel,
            self.currentCalibValueFrame,
            self.currentCalibValueLabel,
            self.currentCalibValueLineEdit,
            stepMeasureIntLineEdit,
            stepMeasureFloatLineEdit
        ]

        for i in self.main_ui_elements:
            if i is None:
                raise Exception(self.objectName() + ' Error: lost UI element')

        self.devNameLabel.setText(self.calib_device.name)
        self.devNameLabel.show()
        self.devSnLabel.setText(self.calib_device.info('serial_num'))
        self.devSnLabel.show()
        stepMeasureIntLineEdit.hide()
        stepMeasureFloatLineEdit.hide()
        # self.currentCalibValueFrame.hide()

        self.pinTypeComboBox.currentIndexChanged.connect(self._load_input_output_type_combo_box_)
        self.input_outputTypeComboBox.currentIndexChanged.connect(self._load_channel_combo_box_)
        self.runCalibBtn.clicked.connect(self._run_calib_btn_clicked_)
        self.stepBackBtn.clicked.connect(self._back_btn_clicked_)
        self.tableBackBtn.clicked.connect(self._back_btn_clicked_)
        self.stepRunBtn.clicked.connect(self._step_run_btn_)
        self.autoBtn.clicked.connect(self._auto_btn_clicked_)
        self.tableWriteCoeffBtn.clicked.connect(self._write_coeffs_btn_clicked_)

        if self.calib_dev_mode is True:
            self.autoBtn.show()
        else:
            self.autoBtn.hide()

        self.ui_settings = self.calibrator.get_ui_settings()
        self.load_combo_boxes()

    @property
    def calib_device(self):
        return self._calib_device

    @calib_device.setter
    def calib_device(self, device):
        self._calib_device = device

    def load_combo_boxes(self):
        pinTypes = self.ui_settings['pinTypes']
        if self.pinTypeComboBox is not None:
            self.pinTypeComboBox.clear()
            for pinType in pinTypes:
                self.pinTypeComboBox.addItem(pinType)
        else:
            raise Exception(self.objectName() + ' Error: wrong UI settings')

        if self.methodComboBox is not None:
            self.methodComboBox.clear()
            _pin_type = self.calibrator.check_pin_type_by_name(self.pinTypeComboBox.currentText())
            if _pin_type == 'inputs':
                self.methodComboBox.addItems([AqTranslateManager.tr('Reference source'),
                                             AqTranslateManager.tr('Reference meter')])
            elif _pin_type == 'outputs':
                self.methodComboBox.addItems([AqTranslateManager.tr('Reference meter')])
        else:
            raise Exception(self.objectName() + ' Error: wrong UI settings')

    def _load_input_output_type_combo_box_(self):
        key = self.pinTypeComboBox.currentText()
        inputTypes = self.ui_settings[key]['sensors']
        if self.input_outputTypeComboBox is not None:
            self.input_outputTypeComboBox.clear()
            for inputType in inputTypes:
                self.input_outputTypeComboBox.addItem(inputType)
        else:
            raise Exception(self.objectName() + ' Error: wrong UI settings')

    def _load_channel_combo_box_(self):
        key = self.input_outputTypeComboBox.currentText()
        channels = self.ui_settings[self.pinTypeComboBox.currentText()][key]
        if self.channelsComboBox is not None:
            self.channelsComboBox.clear()
            self.channelsComboBox.addItem(AqTranslateManager.tr('All channels'))
            for channel in channels:
                self.channelsComboBox.addItem(channel)

        else:
            raise Exception(self.objectName() + ' Error: wrong UI settings')

    def _run_calib_btn_clicked_(self):
        self.samples.clear()
        self.return_default_auto_btn_style_sheet()
        self.user_settings['pinType'] = self.pinTypeComboBox.currentText()
        self.user_settings['_pinType'] = self.calibrator.check_pin_type_by_name(self.user_settings['pinType'])
        self.user_settings['input_outputType'] = self.input_outputTypeComboBox.currentText()
        if self.channelsComboBox.currentIndex() == 0:
            self.user_settings['channels'] = [self.channelsComboBox.itemText(i)
                                              for i in range(self.channelsComboBox.count())][1:]
        else:
            self.user_settings['channels'] = [self.channelsComboBox.currentText()]

        self.user_settings['method'] = self.methodComboBox.currentText()

        self.calibrator.create_calib_session(self.user_settings)

        if not self.calibrator.init_calib_device_config():
            self.setCurrentIndex(1)
            self._message_manager.send_message('calib',
                                               'Error',
                                               AqTranslateManager.tr(
                                                   'Start calibration failed! Check connections lines and try again.'))
            return

        if self.calibrator.pre_ch_calib_func(self.user_settings):
            self._load_step_page_(self.user_settings)
            self.setCurrentIndex(2)
        else:
            self.setCurrentIndex(1)
            self._message_manager.send_message('calib',
                                               'Error',
                                               AqTranslateManager.tr('Start calibration failed! Check connections lines and try again.'))

    def _load_step_page_(self, user_settings):
        if self.auto_mode is False:
            self.stepRunBtn.setEnabled(True)

        step_ui_settings = self.calibrator.calib_session.get_step_ui_settings()

        self.stepHeaderLabel.setText(user_settings['input_outputType'])
        self.stepStepsLabel.setText(AqTranslateManager.tr('Step') + ' ' +
                                     '<b>' + str(step_ui_settings['step']) + '</b>' + ' ' +
                                     AqTranslateManager.tr('from') + ' ' +
                                     '<b>' + str(step_ui_settings['steps_count']) + '</b>')
        self.stepDescrLabel_1.setText(AqTranslateManager.tr('Do next:'))
        self.stepDescrLabel_3.setText(AqTranslateManager.tr('2. Press Run.'))

        self.currentCalibValueLabel.setText(AqTranslateManager.tr('Current device value'))
        self.activate_cur_calib_value_scan(True)

        self.stepPicLabel.setText(AqTranslateManager.tr('Connection diagram'))
        if user_settings['method'] == AqTranslateManager.tr('Reference source'):
            key = 'referenceSignal'
            self.stepMeasureLabel.hide()
            self.stepMeasureLineEdit.hide()

            self.stepDescrLabel_2.setText(AqTranslateManager.tr('1. Connect to ') +
                                           '<b>' + step_ui_settings['name'] + '</b>' + ' ' +
                                           AqTranslateManager.tr('source of signal with value ') +
                                           '<b>' + str(step_ui_settings['point']) + '</b>' + ' ' +
                                           step_ui_settings['unit'] + ' ' +
                                           AqTranslateManager.tr('like show in diagram.'))
        elif user_settings['method'] == AqTranslateManager.tr('Reference meter'):
            self.stepMeasureLabel.setText(AqTranslateManager.tr('Measured value,') + ' ' +
                                           step_ui_settings['unit'] + ':')
            self.stepMeasureLabel.show()
            self.stepMeasureLineEdit.hide()
            line_edit_type = self.calibrator.calib_session.get_cur_channel().calib_param_value.value_type
            if line_edit_type == 'UInteger':
                self.stepMeasureLineEdit = self.findChild(QLineEdit, 'measureIntLineEdit')
            elif line_edit_type == 'FloatWithErrorCode' or line_edit_type == 'Float':
                self.stepMeasureLineEdit = self.findChild(QLineEdit, 'measureFloatLineEdit')

            self.stepMeasureLineEdit.show()
            self.stepDescrLabel_2.setText('1. ' + '<b>' + step_ui_settings['name'] + '</b>' + ' ' +
                                           AqTranslateManager.tr('produces a signal with the value') +
                                           ' ' + '<b>' + str(step_ui_settings['point']) + '</b>' + ' ' +
                                           step_ui_settings['unit'] + '. ' +
                                           AqTranslateManager.tr('Measure the output signal value as shown in the diagram and enter the value in the appropriate field below.'))
            key = 'measuringSignal'
        else:
            raise Exception('method error')

        # try:
        #     # Конвертируем SVG → PNG в память
        #     svg_path = self.roaming_temp_folder + '/calib/' + self.calibrator.calib_session.image[key]
        #     with open(svg_path, 'rb') as f:
        #         svg_data = f.read()
        #
        #     png_bytes = cairosvg.svg2png(bytestring=svg_data)
        #     pixmap = QPixmap()
        #     pixmap.loadFromData(png_bytes)
        #     self.stepPicture.setPixmap(pixmap)
        #     self.stepPicture.show()
        # except Exception as e:
        #     print(f'image not found. Error: {e}')

    def _load_table_page_(self, context):
        self.stepRunBtn.setEnabled(True)
        self.auto_mode = False
        sensor_type = self.user_settings['pinType']
        self.tableDescrLabel1.setText(AqTranslateManager.tr('Calibration coefficients were calculated successfully'))
        self.tableDescrLabel2.setText(AqTranslateManager.tr('Sensor type:') + f' {sensor_type}')
        self.tableDescrLabel3.setText(AqTranslateManager.tr('To record new calibration coefficients, click Write'))
        self.tableWidget.load_table(context)
        self.setCurrentIndex(3)

    def _back_btn_clicked_(self):
        self.calibrator.return_saved_coeffs()
        self.calibrator.clear_session_cash()
        self.activate_cur_calib_value_scan(False)
        self.stepRunBtn.setEnabled(True)
        self.auto_mode = False
        self.return_default_auto_btn_style_sheet()
        self.setCurrentIndex(1)
        self._message_manager.send_message('calib',
                                           'Warning',
                                           AqTranslateManager.tr('Calibration aborted. The previous calibration coefficients have been returned to the device.'))

    def _step_run_btn_(self):
        self.activate_cur_calib_value_scan(False)
        self.samples.clear()
        if self.stepMeasureLineEdit.text() == '' and self.user_settings['method'] == AqTranslateManager.tr('Reference meter'):
            self._message_manager.send_message('calib',
                                               'Warning',
                                               AqTranslateManager.tr('Empty field.'))
            return

        self.stepRunBtn.setEnabled(False)

        if self.user_settings['method'] not in (AqTranslateManager.tr('Reference meter'),
                                                AqTranslateManager.tr('Reference source')):
            raise Exception('Unknown calib method')

        if self.user_settings['method'] == (AqTranslateManager.tr('Reference meter')):
            self.calibrator.accept_measured_point(self.stepMeasureLineEdit.text())

        value = self.calibrator.get_cur_ch_value()
        if value is False:
            self._message_manager.send_message('calib',
                                               'Error',
                                               AqTranslateManager.tr('Read value from device failed.'))
            self._back_btn_clicked_()

        if not self.calibrator.accept_measured_value(value):
            self._message_manager.send_message('calib',
                                               'Error',
                                               AqTranslateManager.tr('The measured value is too different from the expected value. Try again.'))
            self.stepRunBtn.setEnabled(True)
            return False

        # перед активацією наступного кроку повертаємо конфіг каналу який був до калібрування
        self.calibrator.post_ch_calib_func()

        if not self.calibrator.calib_session.activate_next_step():
            self.calibrator.make_calculation()
            calib_result = self.calibrator.calib_session.get_calib_result()
            self._load_table_page_(calib_result)
            return False

        # self.calibrator.pre_calib_func(self.user_settings)
        # self._load_step_page_(self.user_settings)
        if self.calibrator.pre_ch_calib_func(self.user_settings):
            self._load_step_page_(self.user_settings)
        else:
            self._message_manager.send_message('calib',
                                               'Error',
                                               AqTranslateManager.tr('Calibration step failed! Check connections lines and try again.'))
            self._back_btn_clicked_()

        return False

    def _write_coeffs_btn_clicked_(self):
        if self.calibrator.write_new_coeffs():
            self._message_manager.send_message('calib',
                                               'Success',
                                               AqTranslateManager.tr('Calibration successfully!'))
        self.calibrator.clear_session_cash()
        self.setCurrentIndex(1)

    def set_calib_dev_mode(self, dev_mode):
        self.calib_dev_mode = dev_mode

    def set_calib_device(self, device):
        self.calib_device = device
        self.start_init_calibrator()

    def start_init_calibrator(self):
        self.init_calib_thread = InitCalibThread(self.init_calibrator)
        # self.init_calib_thread.finished.connect(self.search_finished)
        self.init_calib_thread.error.connect(self.calib_init_error)
        self.init_calib_thread.result_signal.connect(self.calibrator_inited)
        self.init_calib_thread.start()

    def init_calibrator(self):
        if self.calib_device.read_calib_file():
            self.roaming_temp_folder = os.path.join(os.getenv('APPDATA'), 'AQteck tool MAX', 'Roaming', 'temp')
            calib_path = self.roaming_temp_folder + '/calib/'
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

                calibrator = AqCalibrator(data, loc_data, self.calib_dev_mode)
            except Exception as e:
                self._message_manager.send_message('calib',
                                                   'Error',
                                                   AqTranslateManager.tr('Calibration file parsing failed!'))
                if self.roaming_temp_folder is not None and os.path.exists(self.roaming_temp_folder):
                    shutil.rmtree(self.roaming_temp_folder)

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

    def close_steps(self):
        self.activate_cur_calib_value_scan(False)
        self.stepRunBtn.setEnabled(True)
        self.auto_mode = False
        self.return_default_auto_btn_style_sheet()

        if self.roaming_temp_folder is not None and os.path.exists(self.roaming_temp_folder):
            shutil.rmtree(self.roaming_temp_folder)

    def activate_cur_calib_value_scan(self, state: bool):
        if state:
            self.cur_calib_value_thread = CurCalibValueThread(self.cur_calib_value_read)
            # self.init_calib_thread.finished.connect(self.search_finished)
            # self.init_calib_thread.error.connect(self.calib_init_error)
            # self.init_calib_thread.result_signal.connect(self.calibrator_inited)
            self.cur_calib_value_thread.start()
        else:
            if self.cur_calib_value_thread is not None:
                self.cur_calib_value_thread.requestInterruption()
                self.cur_calib_value_thread.wait()  # Дождаться завершения

    def cur_calib_value_read(self):
        value = self.calibrator.get_cur_ch_value()
        value = check_err_code_in_value(value)
        self.currentCalibValueLineEdit.setText(str(value))
        if self.auto_mode is True:
            self.value_is_stable(value)

    def value_is_stable(self, value):
        if isinstance(value, float) or isinstance(value, int):
            self.samples.append(value)
            if len(self.samples) >= self.samples.maxlen:
                devi = pstdev(self.samples)
                average = mean(self.samples)
                if average < 1.0:
                    average = 1.0
                tolerance = average * TOLERANCE_PERCENT
                if float(devi) < tolerance:
                    self.auto_next_step_signal.emit()
                else:
                    self.auto_mode_wait_count = self.auto_mode_wait_count + 1
                    if self.auto_mode_wait_count > WAIT_SAMPLES:
                        self.auto_mode_wait_count = 0
                        self._message_manager.send_message('calib',
                                                           'Warning',
                                                           AqTranslateManager.tr(
                                                               'The signal is not stable!'))

        else:
            self.samples.clear()

    def _auto_btn_clicked_(self):
        if self.auto_mode is False:
            self.auto_mode = True
            self.stepRunBtn.setEnabled(False)
            self.autoBtn.setStyleSheet("""QPushButton {
                                            border: 1px solid #637A7B;
                                        }
                                        
                                        QPushButton {
                                             border-left: 1px solid #9ef1d3;
                                            border-top: 1px solid #9ef1d3;
                                            border-bottom: 1px solid #5bb192;
                                            border-right: 1px solid #5bb192;
                                            color: #FFFFFF;
                                            background-color: #01bafa;
                                            border-radius: 4px;
                                            padding-left: 10px;
                                            padding-right: 10px;
                                        }
                                        
                                        QPushButton:hover {
                                            background-color: #3c3e41;
                                        }
                                        QPushButton:pressed {
                                             background-color: #429061;
                                        }""")
        else:
            self.auto_mode = False
            self.stepRunBtn.setEnabled(True)
            self.return_default_auto_btn_style_sheet()

    def return_default_auto_btn_style_sheet(self):
        self.autoBtn.setStyleSheet("""QPushButton {
                                                    border: 1px solid #637A7B;
                                                }

                                                QPushButton {
                                                     border-left: 1px solid #9ef1d3;
                                                    border-top: 1px solid #9ef1d3;
                                                    border-bottom: 1px solid #5bb192;
                                                    border-right: 1px solid #5bb192;
                                                    color: #FFFFFF;
                                                    background-color: #2b2d30;
                                                    border-radius: 4px;
                                                    padding-left: 10px;
                                                    padding-right: 10px;
                                                }

                                                QPushButton:hover {
                                                    background-color: #3c3e41;
                                                }
                                                QPushButton:pressed {
                                                     background-color: #429061;
                                                }""")
