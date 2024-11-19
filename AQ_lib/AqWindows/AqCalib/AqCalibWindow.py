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

    def set_calib_device(self, device):
        # if device.read_calib_file():
        #     calib_path = 'temp/calib/'
        #     AqCalibCreator.prepare_json_file(calib_path + device.name + '_calibr.json',
        #                                      calib_path + 'current_calibr.json')
        #     data = AqCalibCreator.load_json(calib_path + 'current_calibr.json')
        #
        #     AqCalibCreator.prepare_json_file(calib_path + device.name + '.json',
        #                                      calib_path + 'current_loc.json')
        #     loc_data = AqCalibCreator.load_json(calib_path + 'current_loc.json')
        #
        #     current_lang = AqTranslateManager.get_current_lang().lower()
        #     if current_lang == 'ua':
        #         current_lang = 'uk'
        #     loc_data = loc_data[current_lang]
        #
        #     # Создаем объект AqCalibrator
        #
        #     calibrator = AqCalibrator(data, loc_data)

            self.event_manager.emit_event('set_calib_device', device)
            # self.event_manager.emit_event('calibrator_inited', calibrator)
        # else:

