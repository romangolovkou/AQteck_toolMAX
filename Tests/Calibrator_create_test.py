import os
import unittest

from AqCalibCreator import AqCalibCreator
from AqCalibWindow import AqCalibWidget
from AqCalibrator import AqCalibrator
from AqTranslateManager import AqTranslateManager
from ui_AqCalibrationWidget import Ui_AqCalibrationWidget


class TestAqCalibrator(unittest.TestCase):
    def test_object_creation(self):

        AqCalibCreator.prepare_json_file('../test_files/МВ210-101_calibr.json',
                                         '../test_files/current_calibr.json')
        data = AqCalibCreator.load_json('../test_files/current_calibr.json')

        AqCalibCreator.prepare_json_file('../test_files/МВ210-101.json',
                                         '../test_files/current_loc.json')
        loc_data = AqCalibCreator.load_json('../test_files/current_loc.json')
        loc_data = loc_data['en']

        # Создаем объект AqCalibrator
        calibrator = AqCalibrator(data, loc_data)

        #тест отримання налаштувань UI
        ui_settings = calibrator.get_ui_settings()


        # Проверяем корректность инициализации
        self.assertEqual(calibrator.protocol, 'Auto Detection Protocol')
        self.assertEqual(calibrator.DevName.value, 'MB210-101')
        self.assertEqual(calibrator.DevName.valueType, 'String')
        self.assertTrue(calibrator.DevName.com.isLittleEndianWords)
        self.assertEqual(calibrator.DevName.com.length, 1)
        self.assertEqual(calibrator.DevName.com.readCommand, 3)
        self.assertEqual(calibrator.DevName.com.register, 61440)
        self.assertEqual(calibrator.timeout, 5000)

    def test_object_creation_2(self):
        self.name = 'FI210-8T'
        self.calib_dev_mode = False
        self.roaming_temp_folder = os.path.join(os.getenv('APPDATA'), 'AQteck tool MAX', 'Roaming', 'temp')
        calib_path = self.roaming_temp_folder + '/calib/'

        AqCalibCreator.prepare_json_file(calib_path + self.name + '_calibr.json',
                                         calib_path + 'current_calibr.json')
        # AqCalibCreator.prepare_json_file('test_files/FI210-8T_calibr.json', calib_path + 'current_calibr.json')
        data = AqCalibCreator.load_json(calib_path + 'current_calibr.json')

        AqCalibCreator.prepare_json_file(calib_path + self.name + '.json',
                                         calib_path + 'current_loc.json')
        # AqCalibCreator.prepare_json_file('test_files/FI210-8T.json', calib_path + 'current_loc.json')
        loc_data = AqCalibCreator.load_json(calib_path + 'current_loc.json')

        current_lang = 'ua'
        if current_lang == 'ua':
            current_lang = 'uk'
        loc_data = loc_data[current_lang]

        calibrator = AqCalibrator(data, loc_data, self.calib_dev_mode)

        # Создаем объект AqCalibrator
        return calibrator


if __name__ == '__main__':
    unittest.main()