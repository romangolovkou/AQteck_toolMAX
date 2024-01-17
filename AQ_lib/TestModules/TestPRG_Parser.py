from unittest import TestCase
from unittest.mock import patch

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

import AqParser


key = b'superkey'

def read_def_prg(path):
    filename = path
    with open(filename, 'rb') as file:
        def_prg = file.read()

    return def_prg

def unpack(data):
    decrypt_file = None
    try:
        # Перевірка на кратність 8 байтам, потрібно для DES
        if (len(data) % 8) > 0:
            # padding = 8 - (len(data) % 8)
            # data = data + bytes([0x00] * padding)
            # Добавление паддинга к данным
            data = pad(data, DES.block_size)

        decrypt_file = __decrypt_data(data)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return 'decrypt_err'  # Помилка дешифрування

    return decrypt_file

def __decrypt_data(encrypted_data):
    # Используется стандарт шифроdания DES CBC(Cipher Block Chain)
    cipher = DES.new(__get_hash(), DES.MODE_CBC, key)
    decrypted_data = cipher.decrypt(encrypted_data)  # encrypted_data - зашифрованные данные

    return decrypted_data

def __get_hash():
    # Ключ это свапнутая версия EMPTY_HASH из исходников котейнерной, в ПО контейнерной оригинал 0x24556FA7FC46B223
    return b"\x23\xB2\x46\xFC\xA7\x6F\x55\x24"  # 0x23B246FCA76F5524"

def encrypt(record_data):
    # file_number = 0xDEAD
    # record_number = 0
    # record_length = 20
    # text = "I will restart the device now!"
    # record_data = text.encode('UTF-8')
    # Выравнивание длины исходных данных
    pad_length = 8 - (len(record_data) % 8)
    padded_data = record_data + bytes([0x00] * pad_length)
    # strange_tail = b'\x1e\x00\x00\x00Y\xdbZ^'
    record_data = padded_data# + strange_tail
    encrypted_record_data = encrypt_data(record_data)

    return encrypted_record_data

def encrypt_data(data):
    # Используется стандарт шифроdания DES CBC(Cipher Block Chain)
    cipher = DES.new(__get_hash(), DES.MODE_CBC, key)
    encrypted_data = cipher.encrypt(data)

    return encrypted_data



class TestConsole(TestCase):

    def test_pars_defprg(self):
        enc_default_prg = read_def_prg('E:/git_new/AQteck_toolMAX/test_files/encrypted_default.prg')

        # encr = encrypt(enc_default_prg)
        # filename = 'E:/git_new/AQteck_toolMAX/test_files/enc_test_1.prg'
        # with open(filename, 'wb') as file:
        #     file.write(encr)

        default_prg = unpack(enc_default_prg)
        # Ця вставка робить файл default.prg у корні проекту (було необхідно для відладки)
        filename = 'E:/git_new/AQteck_toolMAX/test_files/decrypted_default.prg'
        with open(filename, 'wb') as file:
            file.write(default_prg)

        device_tree = AqParser.parse_default_prg(default_prg)
        self.assertNotEqual(device_tree, 'parsing_err')

    def test_decrypt_size(self):
        enc_default_prg = read_def_prg('E:/git_new/AQteck_toolMAX/test_files/deflt.prg')
        enc_default_prg_ = read_def_prg('E:/git_new/AQteck_toolMAX/test_files/encrypted_default_.prg')

        # encr = encrypt(enc_default_prg)
        # filename = 'E:/git_new/AQteck_toolMAX/test_files/enc_test_1.prg'
        # with open(filename, 'wb') as file:
        #     file.write(encr)

        default_prg = unpack(enc_default_prg)
        default_prg_ = unpack(enc_default_prg_)

        size = int.from_bytes((default_prg[4:8][::-1]), byteorder='big')
        size_ = int.from_bytes((default_prg_[4:8][::-1]), byteorder='big')
        # # Ця вставка робить файл default.prg у корні проекту (було необхідно для відладки)
        # filename = 'E:/git_new/AQteck_toolMAX/test_files/decrypted_default.prg'
        # with open(filename, 'wb') as file:
        #     file.write(default_prg)
        #
        # device_tree = AqParser.parse_default_prg(default_prg)
        self.assertEqual(size, size_)

    # @patch('console_app.get_input', return_value="connect")
    # def test_connect_called(self, input):
    #     with patch.object(console_app, 'connect') as mock:
    #         proceed_command()
    #
    #     mock.assert_called()
    #
    # @patch('console_app.get_input', return_value="help")
    # def test_help_called(self, input):
    #     with patch.object(console_help_functions, 'print_command_help') as mock:
    #         proceed_command()
    #
    #     mock.assert_called()
    #
    # @patch('console_app.get_input', return_value="-help")
    # def test_command_error1(self, input):
    #     self.assertEqual(proceed_command(), 'Unknown command: -help')
    #
    # @patch('console_app.get_input', return_value="he")
    # def test_command_error1(self, input):
    #     self.assertEqual(proceed_command(), 'Unknown command: he')
    #
    # @patch('console_app.get_input', return_value="connect -ip 192.168.0.10")
    # def test_connect_string1(self, input):
    #     with patch.object(DeviceCreator, 'from_param_dict') as mock:
    #         proceed_command()
    #     mock.assert_called()
    #
    # @patch('console_app.get_input', return_value="connect -ip 192.168.0.10 -d auto")
    # def test_connect_string2(self, input):
    #     with patch.object(DeviceCreator, 'from_param_dict') as mock:
    #         proceed_command()
    #     mock.assert_called()
    #
    # @patch('console_app.get_input', return_value="connect -ip 192.168.0.10 -f auto")
    # def test_connect_string3(self, input):
    #     self.assertEqual(proceed_command(), 'Unknown parameter -f auto')



