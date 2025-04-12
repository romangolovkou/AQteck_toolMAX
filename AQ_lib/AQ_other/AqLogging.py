import inspect
import os
import sys
import logging
import traceback
from pathlib import Path

from PySide2.QtCore import QObject


# class AqLogging(QObject):

    # @classmethod
def init():
    roaming_folder = os.path.join(os.getenv('APPDATA'), 'AQteck tool MAX', 'Roaming')
    # Проверяем наличие папки Roaming, если её нет - создаем
    if not os.path.exists(roaming_folder):
        os.makedirs(roaming_folder)

    file_path = roaming_folder + '/traceback.log'

    if not os.path.exists(file_path):  # Проверяем, существует ли файл
        with open(file_path, "w") as file:  # Создаём файл
            file.write("")  # Можно записать что-то при необходимости
        print(f"Файл '{file_path}' создан.")
    else:
        print(f"Файл '{file_path}' уже существует.")

    logging.basicConfig(filename=file_path)


# @classmethod
def exception_hook(exc_type, exc_value, exc_traceback):
    logging.error('************************************')
    logging.error(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )

    # """Обработчик необработанных исключений, записывает стек вызовов, аргументы и переменные"""

    # logging.error('------------------------------------')
    #
    # log_msg = f"Uncaught exception: {exc_type.__name__}: {exc_value}\n"
    #
    # # Проходим по всем уровням стека вызовов
    # for frame_info in inspect.trace():
    #     frame = frame_info.frame
    #     function_name = frame_info.function  # Имя функции
    #     filename = frame_info.filename  # Имя файла
    #     lineno = frame_info.lineno  # Номер строки
    #
    #     # Получаем аргументы функции
    #     args, _, _, values = inspect.getargvalues(frame)
    #     args_repr = {arg: values[arg] for arg in args}  # Формируем словарь аргументов
    #
    #     # Получаем локальные переменные
    #     local_vars = frame.f_locals.copy()
    #
    #     log_msg += f"\nFunction: {function_name} in {filename}:{lineno}"
    #     log_msg += f"\n  Arguments: {args_repr}"
    #     log_msg += f"\n  Local Variables: {local_vars}"
    #
    # log_msg += "\nTraceback:\n" + "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    #
    # logging.error(log_msg)
    logging.error('************************************')
