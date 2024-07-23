import os
import shutil
import sys

def get_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for file in files:
            if not file.startswith("__init__"):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

    return file_paths


def copy_files(source_directory):
    copied_files = []
    # destination_directory = os.getcwd()  # Получаем текущую директорию

    for root, directories, files in os.walk(source_directory):
        for file in files:
            if not file.startswith("__init__") and file.endswith(".py"):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_directory, file)
                shutil.copy2(source_path, destination_path)
                copied_files.append(file)

    return copied_files

def delete_copied_files(copied_files):
    for file_name in copied_files:
        file_path = os.path.join(destination_directory, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)

from cx_Freeze import setup, Executable

build_exe_options = {
    # "packages": ["AQ_EventManager"],
    # 'zip_includes': ["AQ_lib/AQ_session/AQ_EventManager.py"],
    # 'zip_includes': get_file_paths("AQ_lib"),
    # 'zip_include_packages': ['pymodbus', 'serial'],
    "include_files": [
        ("UI", "UI"),
        ("Icons", "Icons"),
        ("110_device_conf", "110_device_conf"),
        ("UI/icons", "UI/icons"),
        ("jsonstyles", "jsonstyles"),
        ("Version.txt", "Version.txt"),
        ("translate/ua.qm", "translate/ua.qm"),
    ],
    'build_exe': 'cx_Freeze_Result',  # Ім'я папки куди зберігається результат
}

base = "Win32GUI"  # Для использования Win32GUI на Windows
executables = [Executable("main.py", base=base,
                          icon='Icons/AQico_silver.ico',
                          target_name='AQteck tool MAX')]

optimize = 2

version_path = "version.txt"
try:
    with open(version_path, 'r') as file:
        version_str = file.read()
except:
    raise Exception('Unknown version')

destination_directory = os.getcwd()  # Получаем текущую директорию

files_list = copy_files('AQ_lib')
files_list += copy_files('UI')
files_list += copy_files('Custom_Widgets')

setup(
    name="AQteck tool MAX",
    version=version_str,
    description="AQteck tool MAX",
    options={"build_exe": build_exe_options},
    executables=executables,
)

delete_copied_files(files_list)
