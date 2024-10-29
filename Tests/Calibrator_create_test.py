import unittest

from AqCalibCreator import AqCalibCreator
from AqCalibrator import AqCalibrator


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


if __name__ == '__main__':
    unittest.main()