from datetime import datetime

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QStandardItem, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QStackedWidget, QComboBox, QPushButton, QLabel

from AqBaseTreeItems import AqParamManagerItem
from AQ_EventManager import AQ_EventManager
from AqBaseDevice import AqBaseDevice
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
        #start page
        self.startHeaderLabel = None
        self.startDescrLabel_1 = None
        self.startDescrLabel_2 = None
        self.startDescrLabel_3 = None
        self.startPicLabel = None
        self.startPicture = None
        self.startBackBtn = None
        self.startRunBtn = None

        self.event_manager.register_event_handler('set_calib_device', self.set_calib_device)
        self.event_manager.register_event_handler('calibrator_inited', self.calibrator_inited)

        self.device_init_widget = DeviceInitWidget()
        self.addWidget(self.device_init_widget)
        self.active_device = None
        self.setCurrentWidget(self.device_init_widget)
        self.show()
        self.check_is_calibrator_ready()

    def prepare_ui(self):
        self.pinTypeComboBox = self.findChild(QComboBox, 'pinTypeComboBox')
        self.input_outputTypeComboBox = self.findChild(QComboBox, 'input_outputTypeComboBox')
        self.channelsComboBox = self.findChild(QComboBox, 'channelsComboBox')
        self.methodComboBox = self.findChild(QComboBox, 'methodComboBox')
        self.runCalibBtn = self.findChild(QPushButton, 'runCalibBtn')

        self.startHeaderLabel = self.findChild(QLabel, 'headerLabel')
        self.startDescrLabel_1 = self.findChild(QLabel, 'descrLabel_1')
        self.startDescrLabel_2 = self.findChild(QLabel, 'descrLabel_2')
        self.startDescrLabel_3 = self.findChild(QLabel, 'descrLabel_3')
        self.startPicLabel = self.findChild(QLabel, 'picLabel')
        self.startPicture = self.findChild(QSvgWidget, 'picture')
        self.startBackBtn = self.findChild(QPushButton, 'backBtn')
        self.startRunBtn = self.findChild(QPushButton, 'runBtn')

        self.main_ui_elements = [
            self.pinTypeComboBox,
            self.input_outputTypeComboBox,
            self.channelsComboBox,
            self.methodComboBox,
            self.runCalibBtn,
            self.startHeaderLabel,
            self.startDescrLabel_1,
            self.startDescrLabel_2,
            self.startDescrLabel_3,
            self.startPicLabel,
            self.startPicture,
            self.startBackBtn,
            self.startRunBtn
        ]

        for i in self.main_ui_elements:
            if i is None:
                raise Exception(self.objectName() + ' Error: lost UI element')

        self.pinTypeComboBox.currentIndexChanged.connect(self._load_input_output_type_combo_box_)
        self.input_outputTypeComboBox.currentIndexChanged.connect(self._load_channel_combo_box_)
        self.runCalibBtn.clicked.connect(self._run_calib_btn_clicked_)
        self.startBackBtn.clicked.connect(self._start_back_btn_clicked_)

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
                self.methodComboBox.addItems(AqTranslateManager.tr('Reference meter'))
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

        self._load_start_page_(self.user_settings)

        self.setCurrentIndex(2)

    def _load_start_page_(self, user_settings):
        cur_channel = self.calibrator.calib_session.get_cur_channel()
        self.startHeaderLabel.setText(user_settings['input_outputType'])
        self.startDescrLabel_1.setText(AqTranslateManager.tr('Do next:'))
        self.startDescrLabel_2.setText(AqTranslateManager.tr('1. Connect to ') +
                                       cur_channel.name + ' ' +
                                       AqTranslateManager.tr('source of signal with value ') +
                                       str(cur_channel.points[0]) + ' V ' +
                                       AqTranslateManager.tr('like show in diagram.'))
        self.startDescrLabel_3.setText(AqTranslateManager.tr('2. Press "Run".'))
        self.startPicLabel.setText(AqTranslateManager.tr('Connection diagram'))
        if user_settings['method'] == 'Reference source':
            key = 'referenceSignal'
        elif user_settings['method'] == 'Reference meter':
            key = 'measuringSignal'
        else:
            raise Exception('method error')

        self.startPicture.load(IMAGE_PREFIX + self.calibrator.calib_session.image[key])

    def _start_back_btn_clicked_(self):
        self.setCurrentIndex(1)

    def set_calib_device(self, device):
        self.calib_device = device
        if self.calibrator is not None:
            self.calibrator.set_calib_device(device)

    def calibrator_inited(self, calibrator):
        self.calibrator = calibrator
        self.calibrator.set_calib_device(self.calib_device)
        self.prepare_ui()
        self.calibrator_is_ready = True

    def check_is_calibrator_ready(self):
        if self.calibrator_is_ready:
            # if self.active_device == device:
            #     self.show_current_device_widget(device)
            self.setCurrentIndex(1)
            self.device_init_widget.stop_animation()
        else:
            # if self.active_device == device:
                self.device_init_widget.start_animation()
                self.setCurrentWidget(self.device_init_widget)
                # Устанавливаем задержку в 50 м.сек и затем повторяем
                QTimer.singleShot(50, lambda: self.check_is_calibrator_ready())

    # def _run_btn_clicked_(self):


    # def show_current_device_widget(self, device):
    #     widget = self.devices_views.get(device, None)
    #     if widget is not None:
    #         self.update_device_values(device)
    #         self.setCurrentWidget(widget)
    #     else:
    #         self.setCurrentWidget(self.no_device_widget)

    # def no_devices_action(self):
    #     self.setCurrentWidget(self.no_device_widget)

    # def delete_device_view(self, device: AqBaseDevice):
    #     tree_view = self.devices_views.get(device, None)
    #     if tree_view is not None:
    #         self.removeWidget(tree_view)
    #         tree_view.model().de_init()
    #         tree_view.deleteLater()

    # def update_device_values(self, device: AqBaseDevice):
    #     tree_view = self.devices_views.get(device, None)
    #     if tree_view is not None:
    #         tree_view.model().update_params_values(device)

    # def update_device_param_statuses(self, device: AqBaseDevice):
    #     tree_view = self.devices_views.get(device, None)
    #     if tree_view is not None:
    #         tree_view.model().update_all_params_statuses()

    # def create_device_tree_for_view(self, device: AqBaseDevice):
    #     device_tree = device.device_tree
    #     if device_tree is not None:
    #         tree_model_for_view = AqTreeViewItemModel(device, self.event_manager)
    #         donor_root_item = device_tree.invisibleRootItem()
    #         new_root_item = tree_model_for_view.invisibleRootItem()
    #         self.traverse_items_create_new_tree_for_view(donor_root_item, new_root_item)
    #         return tree_model_for_view

    # def traverse_items_create_new_tree_for_view(self, item, new_item):
    #     for row in range(item.rowCount()):
    #         child_item = item.child(row)
    #         if child_item is not None:
    #             parameter_attributes = child_item.data(Qt.UserRole)
    #             if parameter_attributes is not None:
    #                 if parameter_attributes.get('is_catalog', 0) == 1:
    #                     name = parameter_attributes.get('name', 'err_name')
    #                     catalog = AqParamManagerItem(child_item)
    #                     catalog.setData(parameter_attributes, Qt.UserRole)
    #                     catalog.setFlags(catalog.flags() & ~Qt.ItemIsEditable)
    #                     self.traverse_items_create_new_tree_for_view(child_item, catalog)
    #                     new_item.appendRow(catalog)
    #                 else:
    #                     new_item.appendRow(self.create_new_row_for_tree_view(child_item))

    # def create_new_row_for_tree_view(self, item):
    #     parameter_attributes = item.data(Qt.UserRole)
    #     name = parameter_attributes.get('name', 'err_name')
    #
    #     parameter_item = AqParamManagerItem(item)
    #     parameter_item.setData(parameter_attributes, Qt.UserRole)
    #     value_item = QStandardItem()
    #     min_limit_item = self.get_min_limit_item(parameter_attributes)
    #     max_limit_item = self.get_max_limit_item(parameter_attributes)
    #     unit_item = self.get_unit_item(parameter_attributes)
    #     default_item = self.get_default_value_item(parameter_attributes)
    #     # Встановлюємо флаг не редагуємого ітему, всім ітемам у строці окрім ітема value
    #     parameter_item.setFlags(parameter_item.flags() & ~Qt.ItemIsEditable)
    #     value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)
    #     min_limit_item.setFlags(min_limit_item.flags() & ~Qt.ItemIsEditable)
    #     max_limit_item.setFlags(max_limit_item.flags() & ~Qt.ItemIsEditable)
    #     unit_item.setFlags(unit_item.flags() & ~Qt.ItemIsEditable)
    #     default_item.setFlags(default_item.flags() & ~Qt.ItemIsEditable)
    #
    #     return [parameter_item, value_item, min_limit_item, max_limit_item, unit_item, default_item]

    # def get_min_limit_item(self, param_attributes):
    #     param_type = param_attributes.get('type', '')
    #     visual_type = param_attributes.get('visual_type', '')
    #     if param_type == 'enum' \
    #             or visual_type == 'ip_format' \
    #             or param_type == 'string' \
    #             or visual_type == 'hex':
    #
    #         min_limit_item = QStandardItem('')
    #
    #     elif param_type == 'date_time':
    #         start_time = datetime(2000, 1, 1).timestamp()
    #         min_lim_value = param_attributes.get('min_limit', None)
    #         if min_lim_value is not None:
    #             min_time_limit_obj = datetime.fromtimestamp(start_time + min_lim_value)
    #             min_time_limit_str = min_time_limit_obj.strftime('%d.%m.%Y %H:%M:%S')
    #         else:
    #             min_time_limit_str = ''
    #
    #         min_limit_item = QStandardItem(str(min_time_limit_str))
    #     elif param_attributes.get('multiply', None) is not None:
    #         min_lim = param_attributes.get('min_limit', '')
    #         if min_lim != '':
    #             min_lim = min_lim * param_attributes.get('multiply', 1)
    #
    #         min_limit_item = QStandardItem(str(round(float(min_lim), 7)))
    #     else:
    #         min_limit_item = QStandardItem(str(param_attributes.get('min_limit', '')))
    #
    #     return min_limit_item

    # def get_max_limit_item(self, param_attributes):
    #     param_type = param_attributes.get('type', '')
    #     visual_type = param_attributes.get('visual_type', '')
    #     if param_type == 'enum' or visual_type == 'ip_format' or param_type == 'string'\
    #        or visual_type == 'hex':
    #         max_limit_item = QStandardItem('')
    #     elif param_type == 'date_time':
    #         start_time = datetime(2000, 1, 1).timestamp()
    #         max_lim_value = param_attributes.get('max_limit', None)
    #         if max_lim_value is not None:
    #             max_time_limit_obj = datetime.fromtimestamp(start_time + max_lim_value)
    #             max_time_limit_str = max_time_limit_obj.strftime('%d.%m.%Y %H:%M:%S')
    #         else:
    #             max_time_limit_str = ''
    #
    #         max_limit_item = QStandardItem(str(max_time_limit_str))
    #     elif param_attributes.get('multiply', None) is not None:
    #         max_lim = param_attributes.get('max_limit', '')
    #         if max_lim != '':
    #             max_lim = max_lim * param_attributes.get('multiply', 1)
    #
    #         max_limit_item = QStandardItem(str(round(float(max_lim), 7)))
    #     else:
    #         max_limit_item = QStandardItem(str(param_attributes.get('max_limit', '')))
    #
    #     return max_limit_item

    # def get_unit_item(self, param_attributes):
    #     param_type = param_attributes.get('type', '')
    #     visual_type = param_attributes.get('visual_type', '')
    #     if param_type == 'enum' or visual_type == 'ip_format':
    #         unit_item = QStandardItem('')
    #     else:
    #         unit_item = QStandardItem(str(param_attributes.get('unit', '')))
    #
    #     return unit_item

    # def get_default_value_item(self, param_attributes):
    #     cur_par_default = ''
    #     if param_attributes.get('type', '') == 'enum':
    #         def_value = param_attributes.get('def_value', '')
    #         r_only = param_attributes.get('R_Only', 0)
    #         w_only = param_attributes.get('W_Only', 0)
    #         if def_value == '' or (r_only == 1 and w_only == 0):
    #             cur_par_default = ''
    #         else:
    #             enum_strings = param_attributes.get('enum_strings', [])
    #             if len(enum_strings) > 0:
    #                 def_str = enum_strings[def_value]
    #                 cur_par_default = def_str
    #     elif param_attributes.get('visual_type', '') == 'ip_format':
    #         cur_par_default = ''
    #     elif param_attributes.get('multiply', None) is not None:
    #         cur_par_default = param_attributes.get('def_value', '')
    #         if cur_par_default != '':
    #             cur_par_default = cur_par_default * param_attributes.get('multiply', 1)
    #
    #         cur_par_default = round(float(cur_par_default), 7)
    #     else:
    #         cur_par_default = param_attributes.get('def_value', '')
    #
    #     default_value_item = QStandardItem(str(cur_par_default))
    #
    #     return default_value_item
