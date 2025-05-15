import time

from PySide6.QtCore import QThread, Signal


class CurCalibValueThread(QThread):
    finished = Signal()
    error = Signal(str)
    result_signal = Signal(object)  # Сигнал для передачи данных в главное окно

    def __init__(self, scan_calib_value_func):
        super().__init__()
        self.scan_calib_value_func = scan_calib_value_func

    def run(self):
        while not self.isInterruptionRequested():
            try:
                result_data = self.scan_calib_value_func()
                time.sleep(1)
                self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
                # По завершении успешного выполнения
                self.finished.emit()
            except Exception as e:
                # В случае ошибки передаем текст ошибки обратно в главный поток
                self.error.emit(str(e))
