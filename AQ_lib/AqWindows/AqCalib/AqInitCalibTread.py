import threading

from PySide6.QtCore import QThread, Signal


class InitCalibThread(QThread):
    finished = Signal()
    error = Signal(str)
    result_signal = Signal(object)  # Сигнал для передачи данных в главное окно

    def __init__(self, init_calib_func):
        super().__init__()
        self.init_calib_func = init_calib_func

    def run(self):
        try:
            result_data = self.init_calib_func()
            self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
            # По завершении успешного выполнения
            self.finished.emit()
        except Exception as e:
            # В случае ошибки передаем текст ошибки обратно в главный поток
            self.error.emit(str(e))
