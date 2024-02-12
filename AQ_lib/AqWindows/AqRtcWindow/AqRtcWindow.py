from datetime import datetime

from PySide6.QtCore import QDate, QObject, QModelIndex, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QPalette
from PySide6.QtWidgets import QWidget, QCalendarWidget, QTableView, QHeaderView, QTableWidget

from AqWindowTemplate import AqDialogTemplate


class AqRtcWindow(AqDialogTemplate):
    """
    Widget require ui.generalInfoFrame and ui.operatingInfoFrame for work
    Check names at your generated Ui
    """

    def __init__(self, _ui, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.maximizeBtnEnable = False

        self.name = 'Set Date Time'
        self._date = None
        self._time = None
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
        self.ui.timeWidget.time = time
        self._time = time

    def prepare_ui(self):
        self.ui.timeWidget.prepare_ui()
        self.ui.syncroPcBtn.clicked.connect(self.get_pc_date_time)

        # Получаем виджет календаря
        daysLabelHeader = self.findChildren(QTableView, 'daysLabelHeader')[0]
        daysLabelHeader.horizontalHeader().setStyleSheet("background-color: #2c313c;")
        daysLabelHeader.setEditTriggers(QTableWidget.NoEditTriggers)
        # Запрещаем изменение размера колонок
        daysLabelHeader.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        daysLabelHeader.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2c313c; color: #FFFFFF; border: none }")
        # calendar_model = calendar_view.model() #self.findChild(QStandardItemModel)

        # calendar_view.hideRow(0)
        # calendar_view.hideColumn(0)

        self.ui.calendarWidget.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.ui.calendarWidget.setHorizontalHeaderFormat(QCalendarWidget.NoHorizontalHeader)

        height = self.ui.calendarWidget.height()

        self.adjustSize()

    def get_pc_date_time(self):
        # Получаем текущую дату и время
        current_datetime = datetime.now()

        # Получаем отдельно дату и время
        self.date = current_datetime.date()
        self.time = current_datetime.time()

        # Получаем список всех дочерних элементов
        child_widgets = self.ui.calendarWidget.findChildren(QObject)

        # Выводим информацию о каждом дочернем элементе
        for child in child_widgets:
            print(f"Type: {child.metaObject().className()}, Name: {child.objectName()}")

    def set_device_date_time(self, date_time: int):
        if date_time is None:
            # TODO: Переделать на норм
            date_time = 0
        date_time += datetime(2000, 1, 1).timestamp()
        datetime_obj = datetime.fromtimestamp(date_time)
        self.date = datetime_obj.date()
        self.time = datetime_obj.time()
