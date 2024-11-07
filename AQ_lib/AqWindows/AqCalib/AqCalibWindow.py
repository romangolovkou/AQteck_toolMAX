from AQ_EventManager import AQ_EventManager
from AqCalibCreator import AqCalibCreator
from AqCalibrator import AqCalibrator
from AqTranslateManager import AqTranslateManager
from AqWindowTemplate import AqDialogTemplate


class AqCalibWidget(AqDialogTemplate):
    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.minimizeBtnEnable = False
        self.maximizeBtnEnable = False

        self.name = 'Calibration'
        self.event_manager = AQ_EventManager.get_global_event_manager()

        # Підготовка необхідних полів UI
        # self.prepare_ui_objects()

        #TODO: Delete after test
        AqCalibCreator.prepare_json_file('test_files/МВ210-101_calibr.json',
                                         'test_files/current_calibr.json')
        data = AqCalibCreator.load_json('test_files/current_calibr.json')

        AqCalibCreator.prepare_json_file('test_files/МВ210-101.json',
                                         'test_files/current_loc.json')
        loc_data = AqCalibCreator.load_json('test_files/current_loc.json')

        current_lang = AqTranslateManager.get_current_lang().lower()
        if current_lang == 'ua':
            current_lang = 'uk'
        loc_data = loc_data[current_lang]

        # Создаем объект AqCalibrator

        calibrator = AqCalibrator(data, loc_data)
        self.event_manager.emit_event('calibrator_inited', calibrator)


