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
        self.date = None
        self._time = None
        self.prepare_ui()

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

