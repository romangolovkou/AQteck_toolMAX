from PySide2.QtCore import QThread, Signal


class UpdateFinalWaitTread(QThread):
    finished = Signal()
    error = Signal(str)
    result_signal = Signal(object)  # Сигнал для передачи данных в главное окно

    def __init__(self, final_wait_func):
        super().__init__()
        self.final_wait_func = final_wait_func

    def run(self):
        try:
            result_data = self.final_wait_func()
            self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
            # По завершении успешного выполнения
            self.finished.emit()
        except Exception as e:
            # В случае ошибки передаем текст ошибки обратно в главный поток
            self.error.emit(str(e))
