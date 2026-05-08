from PySide2.QtCore import QThread, Signal


class ReadArchiveTread(QThread):
    finished = Signal()
    error = Signal(str)
    result_signal = Signal(object)  # Сигнал для передачи данных в главное окно
    progress_signal = Signal(int)

    def __init__(self, read_archive_func):
        super().__init__()
        self.read_archive_func = read_archive_func

    def run(self):
        try:
            result_data = self.read_archive_func()
            self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
            # По завершении успешного выполнения
            self.finished.emit()
        except Exception as e:
            # В случае ошибки передаем текст ошибки обратно в главный поток
            self.error.emit(str(e))
