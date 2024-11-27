from datetime import datetime

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QStandardItem, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QStackedWidget, QComboBox, QPushButton, QLabel, QLineEdit

from AqBaseTreeItems import AqParamManagerItem
from AQ_EventManager import AQ_EventManager
from AqBaseDevice import AqBaseDevice
from AqCalibCreator import AqCalibCreator
from AqCalibrator import AqCalibrator
from AqInitCalibTread import InitCalibThread
from AqTranslateManager import AqTranslateManager
from AqTreeView import AqTreeView
from AqTreeViewItemModel import AqTreeViewItemModel
from DeviceNotInitedWifget import DeviceInitWidget
from NoDevicesWidget import NoDeviceWidget

IMAGE_PREFIX = 'test_files/'


class AqCalibViewManager(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.calibrator_is_ready = False
        self.event_manager = AQ_EventManager.get_global_event_manager()
        # self.event_manager.register_event_handler("new_devices_added", self.add_new_devices_trees)
        # self.event_manager.register_event_handler('set_active_device', self.set_active_device_tree)
        # self.event_manager.register_event_handler("current_device_data_updated", self.update_device_values)
        # self.event_manager.register_event_handler("current_device_data_written", self.update_device_param_statuses)
        # self.event_manager.register_event_handler("delete_device", self.delete_device_view)
        # self.event_manager.register_event_handler('no_devices', self.no_devices_action)
        # self.devices_views = {}
        # self.active_device = None
        # self.no_device_widget = NoDeviceWidget()
        # self.addWidget(self.no_device_widget)
        self.calib_device = None
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

        self.event_manager.register_event_handler('set_calib_device', self.set_calib_device)
        self.event_manager.register_event_handler('calibrator_inited', self.calibrator_inited)

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
        self.stepMeasureLineEdit = self.findChild(QLineEdit, 'measureLineEdit')
        self.stepPicLabel = self.findChild(QLabel, 'picLabel')
        self.stepPicture = self.findChild(QSvgWidget, 'picture')
        self.stepBackBtn = self.findChild(QPushButton, 'backBtn')
        self.stepRunBtn = self.findChild(QPushButton, 'runBtn')

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
            self.stepMeasureLineEdit,
            self.stepPicLabel,
            self.stepPicture,
            self.stepBackBtn,
            self.stepRunBtn
        ]

        for i in self.main_ui_elements:
            if i is None:
                raise Exception(self.objectName() + ' Error: lost UI element')

        self.pinTypeComboBox.currentIndexChanged.connect(self._load_input_output_type_combo_box_)
        self.input_outputTypeComboBox.currentIndexChanged.connect(self._load_channel_combo_box_)
        self.runCalibBtn.clicked.connect(self._run_calib_btn_clicked_)
        self.stepBackBtn.clicked.connect(self._step_back_btn_clicked_)
        self.stepRunBtn.clicked.connect(self._step_run_btn_)

        self.ui_settings = self.calibrator.get_ui_settings()
        self.load_combo_boxes()

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

        self.calibrator.pre_calib_func(self.user_settings)

        self._load_step_page_(self.user_settings)

        self.setCurrentIndex(2)

    def _load_step_page_(self, user_settings):
        step_ui_settings = self.calibrator.calib_session.get_step_ui_settings()

        self.stepHeaderLabel.setText(user_settings['input_outputType'])
        self.stepStepsLabel.setText(AqTranslateManager.tr('Step') + ' ' +
                                     str(step_ui_settings['step']) + ' ' +
                                     AqTranslateManager.tr('from') + ' ' +
                                     str(step_ui_settings['steps_count']))
        self.stepDescrLabel_1.setText(AqTranslateManager.tr('Do next:'))
        self.stepDescrLabel_3.setText(AqTranslateManager.tr('2. Press "Run".'))

        self.stepPicLabel.setText(AqTranslateManager.tr('Connection diagram'))
        if user_settings['method'] == 'Reference source':
            key = 'referenceSignal'
            self.stepMeasureLabel.hide()
            self.stepMeasureLineEdit.hide()
            self.stepDescrLabel_2.setText(AqTranslateManager.tr('1. Connect to ') +
                                           step_ui_settings['name'] + ' ' +
                                           AqTranslateManager.tr('source of signal with value ') +
                                           str(step_ui_settings['point']) + ' ' +
                                           step_ui_settings['unit'] + ' ' +
                                           AqTranslateManager.tr('like show in diagram.'))
        elif user_settings['method'] == 'Reference meter':
            self.stepMeasureLabel.setText(AqTranslateManager.tr('Measured value,') + ' ' +
                                           step_ui_settings['unit'] + ':')
            self.stepMeasureLabel.show()
            self.stepMeasureLineEdit.show()
            self.stepDescrLabel_2.setText('1. ' + step_ui_settings['name'] + ' ' +
                                           AqTranslateManager.tr('produces a signal with the value') +
                                           ' ' + str(step_ui_settings['point']) + ' ' +
                                           step_ui_settings['unit'] + '. ' +
                                           AqTranslateManager.tr('Measure the output signal value as shown in the diagram and enter the value in the appropriate field below.'))
            key = 'measuringSignal'
        else:
            raise Exception('method error')

        self.stepPicture.load(IMAGE_PREFIX + self.calibrator.calib_session.image[key])

    def _step_back_btn_clicked_(self):
        self.setCurrentIndex(1)

    def _step_run_btn_(self):
        self.calibrator.accept_measured_point(self.stepMeasureLineEdit.text())
        if not self.calibrator.calib_session.activate_next_step():
            self.calibrator.make_calculation()

        self._load_step_page_(self.user_settings)
        return False

    def set_calib_device(self, device):
        self.calib_device = device
        self.start_init_calibrator()

    def start_init_calibrator(self):
        self.init_calib_thread = InitCalibThread(self.init_calibrator)
        # self.init_calib_thread.finished.connect(self.search_finished)
        # self.init_calib_thread.error.connect(self.search_error)
        self.init_calib_thread.result_signal.connect(self.calibrator_inited)
        self.init_calib_thread.start()

    def init_calibrator(self):
        if self.calib_device.read_calib_file():
            calib_path = 'temp/calib/'
            AqCalibCreator.prepare_json_file(calib_path + self.calib_device.name + '_calibr.json',
                                             calib_path + 'current_calibr.json')
            data = AqCalibCreator.load_json(calib_path + 'current_calibr.json')

            AqCalibCreator.prepare_json_file(calib_path + self.calib_device.name + '.json',
                                             calib_path + 'current_loc.json')
            loc_data = AqCalibCreator.load_json(calib_path + 'current_loc.json')

            current_lang = AqTranslateManager.get_current_lang().lower()
            if current_lang == 'ua':
                current_lang = 'uk'
            loc_data = loc_data[current_lang]

            # Создаем объект AqCalibrator

            return AqCalibrator(data, loc_data)

    def calibrator_inited(self, calibrator):
        self.calibrator = calibrator
        self.calibrator.set_calib_device(self.calib_device)
        self.prepare_ui()
        self.calibrator_is_ready = True

    def check_is_calibrator_ready(self):
        if self.calibrator_is_ready:
            self.setCurrentIndex(1)
            self.device_init_widget.stop_animation()
        else:
            self.device_init_widget.start_animation()
            self.setCurrentWidget(self.device_init_widget)
            # Устанавливаем задержку в 50 м.сек и затем повторяем
            QTimer.singleShot(50, lambda: self.check_is_calibrator_ready())




