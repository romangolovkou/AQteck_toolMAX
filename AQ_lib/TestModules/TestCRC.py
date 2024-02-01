import struct
from unittest import TestCase

from AqCRC32 import Crc32


class TestCRC(TestCase):
    def test_CRC32(self):
        text = "I will restart the device now!"
        record_data = text.encode('UTF-8')
        # item = self.system_params_dict.get('reboot', None)

        crc = Crc32().calculate(record_data)
        length = len(record_data)
        # Выравнивание длины исходных данных
        pad_length = 8 - (len(record_data) % 8)
        padded_data = record_data + bytes([0x00] * pad_length)

        bit_len = crc.bit_length()
        data_to_write = padded_data + length.to_bytes(4, byteorder='little')
        data_to_write = data_to_write + crc.to_bytes(4, byteorder='little', signed=True)
        # data_to_write = data_to_write + struct.pack('<I', crc)
        strange_tail = b'\x1e\x00\x00\x00Y\xdbZ^'
        record_data = padded_data + strange_tail
        self.assertEqual(True, False)  # add assertion here
        self.assertIsInstance(data_to_write, bytes)
