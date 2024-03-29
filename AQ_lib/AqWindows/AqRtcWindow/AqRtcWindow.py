from datetime import datetime, timedelta, timezone, date, time
from functools import partial

from PySide6.QtCore import QDate, QObject, QModelIndex, Qt, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QPalette
from PySide6.QtWidgets import QWidget, QCalendarWidget, QTableView, QHeaderView, QTableWidget

from AqMessageManager import AqMessageManager
from AqWindowTemplate import AqDialogTemplate


class AqRtcWindow(AqDialogTemplate):
    message_signal = Signal(str, str)

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.maximizeBtnEnable = False

        self.name = 'Set Date Time'
        self._date = None
        self._time = None
        self._time_zone = None
        self.__write_handler = None

        self._message_manager = AqMessageManager.get_global_message_manager()
        self.prepare_ui()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date: datetime.date):
        self.ui.calendarWidget.setSelectedDate(QDate(date.year,
                                                     date.month,
                                                     date.day))
        self._date = date

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time: datetime.time):
        # Создаем объект datetime с использованием текущей даты, вашего времени и часового пояса
        combined_datetime = datetime.combine(datetime.now().date(), time, self._time_zone)
        self.ui.timeWidget.time = self._time_zone.fromutc(combined_datetime)
        self._time = time

    def set_pc_time(self, time: datetime.time):
        self.ui.timeWidget.time = time

    @property
    def time_zone(self):
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_shift: timezone):
        self.ui.timeZoneComboBox.set_item_text_by_shift(time_shift)
        self._time_zone = time_shift

    def prepare_ui(self):
        self.ui.timeWidget.prepare_ui()
        self.ui.timeWidget.time_changed.connect(self.time_changed)
        self.ui.syncroPcBtn.clicked.connect(self.get_pc_date_time)
        self.ui.writeBtn.clicked.connect(self.write_new_date_time)
        self.ui.cancelBtn.clicked.connect(self.close)

        # Получаем виджет календаря
        daysLabelHeader = self.findChildren(QTableView, 'daysLabelHeader')[0]
        daysLabelHeader.horizontalHeader().setStyleSheet("background-color: #2c313c;")
        daysLabelHeader.setEditTriggers(QTableWidget.NoEditTriggers)
        # Запрещаем изменение размера колонок
        daysLabelHeader.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        daysLabelHeader.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2c313c; color: #FFFFFF; border: none }")

        self.ui.calendarWidget.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.ui.calendarWidget.setHorizontalHeaderFormat(QCalendarWidget.NoHorizontalHeader)
        self.ui.calendarWidget.selectionChanged.connect(self.selected_date_changed)

        self.ui.timeZoneComboBox.currentIndexChanged.connect(self.time_zone_changed)

        self.message_signal.connect(partial(self._message_manager.show_message, self))
        self._message_manager.subscribe(self.message_signal.emit)

    def get_pc_date_time(self):
        # Получаем текущую дату и время
        current_datetime = datetime.now()

        # Получаем отдельно дату и время
        self.date = current_datetime.date()
        self.set_pc_time(current_datetime.time())

        # # Получаем список всех дочерних элементов
        # child_widgets = self.ui.calendarWidget.findChildren(QObject)
        #
        # # Выводим информацию о каждом дочернем элементе
        # for child in child_widgets:
        #     print(f"Type: {child.metaObject().className()}, Name: {child.objectName()}")

    def set_device_date_time(self, date_time_dict: dict):
        date_time = date_time_dict['date_time']
        time_zone = date_time_dict['time_zone']
        if date_time is None:
            # TODO: Переделать на норм
            date_time = 0
        date_time += datetime(2000, 1, 1).timestamp()
        datetime_obj = datetime.fromtimestamp(date_time)
        device_timezone = timezone(timedelta(hours=(time_zone // 60)))
        self.time_zone = device_timezone
        self.date = datetime_obj.date()
        self.time = datetime_obj.time()


    def selected_date_changed(self):
        # Получение выбранной даты
        selected_date = self.ui.calendarWidget.selectedDate()
        # Преобразуем QDate в datetime.date
        self._date = date(selected_date.year(), selected_date.month(), selected_date.day())

    def time_changed(self):
        if self._time_zone is not None:
            max_limit = 86399
            min_limit = 0
            time_delta = int(self._time_zone.utcoffset(None).total_seconds())
            new_time = self.ui.timeWidget.time
            if new_time is not None:
                time_seconds = new_time.hour * 3600 + new_time.minute * 60 + new_time.second
                total_seconds = time_seconds + (time_delta * -1)
                if total_seconds > max_limit:
                    total_seconds = total_seconds - max_limit - 1

                if total_seconds < min_limit:
                    total_seconds = max_limit + 1 + total_seconds
                # Вычисляем часы, минуты и секунды
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                # Создаем объект datetime.time
                result_time = time(hours, minutes, seconds)
                self._time = result_time

    def time_zone_changed(self):
        shift_str = self.ui.timeZoneComboBox.currentText()[4:10]
        sign = shift_str[:1]
        if sign == '+':
            multiply = 1
        elif sign == '-':
            multiply = -1
        else:
            multiply = 1

        hour = shift_str[1:3]
        hour = int(hour) * multiply
        minutes = shift_str[4:]
        minutes = int(minutes) * multiply
        new_timezone = timezone(timedelta(hours=hour, minutes=minutes))
        self._time_zone = new_timezone
        self.time_changed()

    def set_write_handler(self, handler):
        self.__write_handler = handler

    def write_new_date_time(self):
        self.ui.writeBtn.setEnabled(False)
        date_time = datetime.combine(self._date, self._time)
        date_dime_dict = {'date_time': date_time,
                          'time_zone': self._time_zone}
        if self.__write_handler is not None:
            if self.__write_handler(date_dime_dict) == 'ok':
                self.show_success_label()
            else:
                self.show_error_label()

        self.ui.writeBtn.setEnabled(True)

    def show_error_label(self):
        # self.ui.messageLabel.setText('Write error. Try again.')
        # self.ui.messageLabel.setStyleSheet("color: #fe2d2d; \n")
        self._message_manager.send_main_message('Error', 'Write error. Try again.')

    def show_success_label(self):
        # self.ui.messageLabel.setText('Successfully! Response: OK')
        # self.ui.messageLabel.setStyleSheet("color: #429061; \n")
        self._message_manager.send_main_message('Success', 'Successfully! Response: OK')

    def hide_message(self):
        self.ui.messageLabel.setText('')

    def close(self):
        self._message_manager.de_subscribe(self.message_signal.emit)
        super().close()
