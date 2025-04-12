from dataclasses import dataclass
from datetime import datetime, time, timedelta

from PySide2.QtCore import QTimer, Signal
from PySide2.QtWidgets import QWidget

from AqTimeCellWidget import AqTimeCellWidget


@dataclass
class CellWidgets:
    t_hour: AqTimeCellWidget
    hour: AqTimeCellWidget
    t_min: AqTimeCellWidget
    min: AqTimeCellWidget
    t_sec: AqTimeCellWidget
    sec: AqTimeCellWidget


class AqTimeWidget(QWidget):
    time_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._time = None
        self.cell_widgets = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_time(1))
        self.timer.start(1000)  # Запуск таймера каждую секунду (1000 миллисекунд)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, new_time: datetime.time):
        self.cell_widgets.t_hour.set_state(new_time.hour // 10)
        self.cell_widgets.hour.set_state(new_time.hour % 10)
        self.cell_widgets.t_min.set_state(new_time.minute // 10)
        self.cell_widgets.min.set_state(new_time.minute % 10)
        self.cell_widgets.t_sec.set_state(new_time.second // 10)
        self.cell_widgets.sec.set_state(new_time.second % 10)

        self._time = new_time
        self.time_changed.emit()

    def prepare_ui(self):
        self.cell_widgets = CellWidgets(self.findChildren(AqTimeCellWidget, 't_hourWidget')[0],
                                        self.findChildren(AqTimeCellWidget, 'hourWidget')[0],
                                        self.findChildren(AqTimeCellWidget, 't_minWidget')[0],
                                        self.findChildren(AqTimeCellWidget, 'minWidget')[0],
                                        self.findChildren(AqTimeCellWidget, 't_secWidget')[0],
                                        self.findChildren(AqTimeCellWidget, 'secWidget')[0])

        self.cell_widgets.t_hour.prepare_ui()
        if self.cell_widgets.t_hour.plusBtn is not None:
            self.cell_widgets.t_hour.plusBtn.clicked.connect(lambda: self.update_time(36000))
        if self.cell_widgets.t_hour.minusBtn is not None:
            self.cell_widgets.t_hour.minusBtn.clicked.connect(lambda: self.update_time(-36000))
        self.cell_widgets.hour.prepare_ui()
        if self.cell_widgets.hour.plusBtn is not None:
            self.cell_widgets.hour.plusBtn.clicked.connect(lambda: self.update_time(3600))
        if self.cell_widgets.hour.minusBtn is not None:
            self.cell_widgets.hour.minusBtn.clicked.connect(lambda: self.update_time(-3600))
        self.cell_widgets.t_min.prepare_ui()
        if self.cell_widgets.t_min.plusBtn is not None:
            self.cell_widgets.t_min.plusBtn.clicked.connect(lambda: self.update_time(600))
        if self.cell_widgets.t_min.minusBtn is not None:
            self.cell_widgets.t_min.minusBtn.clicked.connect(lambda: self.update_time(-600))
        self.cell_widgets.min.prepare_ui()
        if self.cell_widgets.min.plusBtn is not None:
            self.cell_widgets.min.plusBtn.clicked.connect(lambda: self.update_time(60))
        if self.cell_widgets.min.minusBtn is not None:
            self.cell_widgets.min.minusBtn.clicked.connect(lambda: self.update_time(-60))
        self.cell_widgets.t_sec.prepare_ui()
        if self.cell_widgets.t_sec.plusBtn is not None:
            self.cell_widgets.t_sec.plusBtn.clicked.connect(lambda: self.update_time(10))
        if self.cell_widgets.t_sec.minusBtn is not None:
            self.cell_widgets.t_sec.minusBtn.clicked.connect(lambda: self.update_time(-10))
        self.cell_widgets.sec.prepare_ui()
        if self.cell_widgets.sec.plusBtn is not None:
            self.cell_widgets.sec.plusBtn.clicked.connect(lambda: self.update_time(1))
        if self.cell_widgets.sec.minusBtn is not None:
            self.cell_widgets.sec.minusBtn.clicked.connect(lambda: self.update_time(-1))

    def update_time(self, seconds):
        current_time = self.time
        if current_time is not None:
            # max_lim кількіст секунд у добі
            max_limit = 86399
            min_limit = 0
            # Преобразуем время в количество секунд
            total_seconds = current_time.hour * 3600 + current_time.minute * 60 + current_time.second
            total_seconds += seconds
            if total_seconds > max_limit:
                total_seconds = total_seconds - max_limit - 1

            if total_seconds < min_limit:
                total_seconds = max_limit + 1 + total_seconds
            # Вычисляем часы, минуты и секунды
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            # Создаем объект datetime.time
            result_time = time(hours, minutes, seconds)
            self.time = result_time
