import os
import shutil
import sys
import fnmatch
import shutil

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


def create_custom_exclude_list_by_keywords(directory, keywords: list):
    matched_files = []
    matched_paths = []

    for root, dirs, files in os.walk(directory):
        for keyword in keywords:
            for filename in fnmatch.filter(dirs, f'*{keyword}*'):
                matched_paths.append(os.path.join(root, filename))

            for filename in fnmatch.filter(files, f'*{keyword}*'):
                matched_files.append(os.path.join(root, filename))

    return matched_paths, matched_files


def custom_hard_delete_exludes(custom_exclude_list: list, delete_dirs: bool=False):
    if delete_dirs:
        for dir_path in custom_exclude_list:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                print(f'Removed {dir_path}')
            else:
                print(f'{dir_path} not exist.')
    else:
        for file_path in custom_exclude_list:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f'Removed {file_path}')
            else:
                print(f'{file_path} not exist.')


custom_excludes = [
    'Qt6Web',
    'Qt3D',
    'Qt6Qml',
    'linguist',
    'lrelease',
    'lupdate',
    'Qt6Quick',
    'translations',
]


def custom_hard_exludes():
    directory = destination_directory + '/' + build_exe_options['build_exe']
    directory += '/lib'

    matched_paths, matched_files = create_custom_exclude_list_by_keywords(directory, custom_excludes)
    print(f'matched_files: {matched_files}')
    print(f'matched_paths: {matched_paths}')
    custom_hard_delete_exludes(matched_files)
    custom_hard_delete_exludes(matched_paths, delete_dirs=True)



from cx_Freeze import setup, Executable

try:
    from cx_Freeze.hooks import get_qt_plugins_paths
except ImportError:
    get_qt_plugins_paths = None

include_files = []
if get_qt_plugins_paths:
    # Inclusion of extra plugins (since cx_Freeze 6.8b2)
    # cx_Freeze automatically imports the following plugins depending on the
    # module used, but suppose we need the following:
    include_files += get_qt_plugins_paths("PySide6", "multimedia")
    print('cx_Freeze_get_dependencies: ')
    print(include_files)

build_exe_options = {
    # "packages": ["AQ_EventManager"],
    # 'zip_includes': ["AQ_lib/AQ_session/AQ_EventManager.py"],
    # 'zip_includes': get_file_paths("AQ_lib"),
    # 'zip_include_packages': ['pymodbus', 'serial'],
    "include_files": [
        # ("UI", "UI"),
        # ("Icons", "Icons"),
        # ("110_device_conf", "110_device_conf"),
        ("UI/icons", "UI/icons"),
        ("jsonstyles", "jsonstyles"),
        ("Version.txt", "Version.txt"),
        ("translate/ua.qm", "translate/ua.qm"),
    ],
    "excludes": [
        "tkinter", "unittest", "email", "http", "xml", "pydoc",
    ],
    'build_exe': 'cx_Freeze_Result',  # Ім'я папки куди зберігається результат
}

base = "Win32GUI"  # Для использования Win32GUI на Windows
executables = [Executable("main.py", base=base,
                          icon='UI/icons/AQico_silver.ico',
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
custom_hard_exludes()
