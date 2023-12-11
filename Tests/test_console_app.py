from unittest import TestCase
from unittest.mock import patch

import console_app
import console_help_functions
from AqDeviceFabrica import DeviceCreator
from console_app import get_input, proceed_command

class TestConsole(TestCase):
    @patch('console_app.get_input', return_value="connect")
    def test_connect_called(self, input):
        with patch.object(console_app, 'connect') as mock:
            proceed_command()

        mock.assert_called()

    @patch('console_app.get_input', return_value="help")
    def test_help_called(self, input):
        with patch.object(console_help_functions, 'print_command_help') as mock:
            proceed_command()

        mock.assert_called()

    @patch('console_app.get_input', return_value="-help")
    def test_command_error1(self, input):
        self.assertEqual(proceed_command(), 'Unknown command: -help')

    @patch('console_app.get_input', return_value="he")
    def test_command_error1(self, input):
        self.assertEqual(proceed_command(), 'Unknown command: he')

    @patch('console_app.get_input', return_value="connect -ip 192.168.0.10")
    def test_connect_string1(self, input):
        with patch.object(DeviceCreator, 'from_param_dict') as mock:
            proceed_command()
        mock.assert_called()

    @patch('console_app.get_input', return_value="connect -ip 192.168.0.10 -d auto")
    def test_connect_string2(self, input):
        with patch.object(DeviceCreator, 'from_param_dict') as mock:
            proceed_command()
        mock.assert_called()

    @patch('console_app.get_input', return_value="connect -ip 192.168.0.10 -f auto")
    def test_connect_string3(self, input):
        self.assertEqual(proceed_command(), 'Unknown parameter -f auto')



