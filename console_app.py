
import console_help_functions
from AppCore import Core
from AqDeviceFabrica import DeviceCreator


def get_input():
    return input()

def run():
    Core.init()
    print("""Welcome to AQteckToolMAX console application
    Programm working by entering commands with argument
    To see available commands type "help"
    To get info about command type "command_name -h"
    """)
    while True:
        proceed_command()


def proceed_command():
    user_cmd = get_input()
    cmd_list = user_cmd.split(' -')
    prg_cmd = cmd_list[0]
    if prg_cmd == 'connect':
        return_value = connect(cmd_list[1:])
    elif prg_cmd == 'help':
        return_value = console_help_functions.print_command_help()
    else:
        return_value = 'Unknown command: ' + str(prg_cmd)
        print(return_value)

    return return_value


def connect(args_list):
    parse_result = connect_parse_user_input(args_list)
    if isinstance(parse_result, dict):
        try:
            device = DeviceCreator.from_param_dict(parse_result)
        except Exception as e:
            print(str(e))
            return str(e)
    else:
        print(parse_result)
        return parse_result


def connect_parse_user_input(args_list):
    network_settings_dict = dict()
    for cmd in args_list:
        cmd_list = cmd.split()
        if len(cmd_list) < 2:
            return "No value for parameter -" + str(cmd_list[0])
        if cmd_list[0] == 'ip':
            network_settings_dict['interface_type'] = 'ip'
            network_settings_dict['ip'] = cmd_list[1]
        elif cmd_list[0] in ('o', '-offline'):
            network_settings_dict['interface_type'] = 'Offline'
        elif cmd_list[0] in ('d', '-device'):
            selected_dev_type = None
            if cmd_list[1] == 'auto':
                selected_dev_type = 'AqAutoDetectionDevice'
            else:
                selected_dev_type = 'AqFileDescriptionDevice'
            network_settings_dict['device'] = cmd_list[1]
            network_settings_dict['device_type'] = selected_dev_type
        elif cmd_list[0] in '-id':
            network_settings_dict['address'] = cmd_list[1]
        elif cmd_list[0] == 'com':
            network_settings_dict['interface_type'] = 'com'
            network_settings_dict['interface'] = 'COM'+str(cmd_list[1])
        elif cmd_list[0] in ('b', '-boudrate'):
            network_settings_dict['boudrate'] = cmd_list[1]
        elif cmd_list[0] in ('p', '-parity'):
            network_settings_dict['parity'] = cmd_list[1]
        elif cmd_list[0] in ('sb', '-stopbits'):
            network_settings_dict['stopbits'] = cmd_list[1]
        else:
            return 'Unknown parameter -'+str(cmd)

    if len(network_settings_dict) == 0:
        return "Enter correct parameters list. Type connect -h to see all parameters"

    return network_settings_dict
