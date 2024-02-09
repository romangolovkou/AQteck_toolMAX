from datetime import datetime

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

    def get_pc_date_time(self):
        # Получаем текущую дату и время
        current_datetime = datetime.now()

        # Получаем отдельно дату и время
        self.date = current_datetime.date()
        self.time = current_datetime.time()

    def set_device_date_time(self, date_time: int):
        date_time += datetime(2000, 1, 1).timestamp()
        datetime_obj = datetime.fromtimestamp(date_time)
        self.time = datetime_obj.time()
