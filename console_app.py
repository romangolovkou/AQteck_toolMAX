
import console_help_functions
from AppCore import Core


def run():
    Core.init()
    print("""Welcome to AQteckToolMAX console application
    Programm working by entering commands with argument
    To see available commands type "help"
    To get info about command type "command_name -h"
    """)
    while True:
        user_cmd = input()
        cmd_list = user_cmd.split()
        prg_cmd = cmd_list[0]
        if prg_cmd == 'connect':
            connect(user_cmd[1:])
        elif prg_cmd == 'help':
            console_help_functions.print_command_help()

def connect(args_list):
    network_settings_list = []
    ip_index = args_list.index('-ip')
    if ip_index is not None:
        _ip = args_list[ip_index+1]

        network_settings_list.append({''})
    com_index