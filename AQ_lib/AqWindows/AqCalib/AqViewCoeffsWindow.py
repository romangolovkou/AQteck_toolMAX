from functools import partial

from PySide6.QtCore import Signal, QTimer, QThread, QAbstractTableModel, Qt, QRect
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QHeaderView, QTableView, QStackedWidget

from AQ_EventManager import AQ_EventManager
from AqCalibCreator import AqCalibCreator
from AqCalibrator import AqCalibrator
from AqMessageManager import AqMessageManager
from AqTranslateManager import AqTranslateManager
from AqWatchListCore import AqWatchListCore
from AqWindowTemplate import AqDialogTemplate
from DeviceNotInitedWidget import DeviceInitWidget


class AqViewCoeffsWidget(AqDialogTemplate):
    message_signal = Signal(str, str)

    def __init__(self, _ui, calibrator, parent=None):
        super().__init__(parent)
        self._calibrator = calibrator
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.minimizeBtnEnable = False
        self.maximizeBtnEnable = False

        self.name = AqTranslateManager.tr('View coeffs')
        self.event_manager = AQ_EventManager.get_global_event_manager()

        self._message_manager = AqMessageManager.get_global_message_manager()

        self.message_signal.connect(partial(self._message_manager.show_message, self))
        self._message_manager.subscribe('View coeffs', self.message_signal.emit)

        self.read_coeffs_tread = ReadCoeffsTread(self.read_coeffs)
        self.read_coeffs_tread.result_signal.connect(self.prepare_coeffs)

        # викликати функцію одразу після відкриття віка
        QTimer.singleShot(0, self.start_reading_tread)

    def start_reading_tread(self):
        self.ui.stackedWidget.device_init_widget.start_animation()
        self.read_coeffs_tread.start()

    def read_coeffs(self):
        return self._calibrator.get_all_channel_in_dev_cur_coeffs()

    def prepare_coeffs(self, coeffs_model_dict):
        self.ui.stackedWidget.device_init_widget.stop_animation()
        model = CoeffsTableModel(coeffs_model_dict)

        view = self.ui.coeffsTableView

        view.setModel(model)

        header = MultiHeaderView(model, view)
        view.setHorizontalHeader(header)
        view.setCornerButtonEnabled(False)

        view.show()

        self.ui.stackedWidget.setCurrentIndex(1)

    def read_archive_error(self):
        self._message_manager.send_message('View coeffs', "Error", AqTranslateManager.tr('Read has been failed'))
        return None




class ReadCoeffsTread(QThread):
    finished = Signal()
    error = Signal(str)
    result_signal = Signal(object)  # Сигнал для передачи данных в главное окно
    progress_signal = Signal(int)

    def __init__(self, read_coeffs_func):
        super().__init__()
        self.read_coeffs_func = read_coeffs_func

    def run(self):
        try:
            result_data = self.read_coeffs_func()
            self.result_signal.emit(result_data)  # Отправка сигнала с данными обратно в главное окно
            # По завершении успешного выполнения
            self.finished.emit()
        except Exception as e:
            # В случае ошибки передаем текст ошибки обратно в главный поток
            self.error.emit(str(e))




def extract_columns(data):
    columns = set()

    for channel in data.values():
        for sensor, coeffs in channel.items():
            for coeff in coeffs:
                columns.add((sensor, coeff))

    return sorted(columns, key=lambda x: (x[0], x[1]))


def build_header_groups(columns):
    groups = {}
    order = []

    for sensor, coeff in columns:

        if sensor not in groups:
            groups[sensor] = []
            order.append(sensor)

        groups[sensor].append(coeff)

    return order, groups


class CoeffsTableModel(QAbstractTableModel):

    def __init__(self, data_dict):
        super().__init__()

        self.columns = extract_columns(data_dict)

        self.header_order, self.header_groups = build_header_groups(self.columns)

        self.channels = list(data_dict.keys())
        self.rows = []

        for channel in self.channels:

            sensors = data_dict[channel]
            row = []

            for sensor, coeff in self.columns:
                value = sensors.get(sensor, {}).get(coeff, None)
                row.append(value)

            self.rows.append(row)

    def rowCount(self, parent=None):
        return len(self.rows)

    def columnCount(self, parent=None):
        return len(self.columns)

    def data(self, index, role):

        if role == Qt.DisplayRole:
            return self.rows[index.row()][index.column()]

    def headerData(self, section, orientation, role):

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Vertical:
            return self.channels[section]

        if orientation == Qt.Horizontal:
            sensor, coeff = self.columns[section]
            return "\n" + coeff


class MultiHeaderView(QHeaderView):

    def __init__(self, model, parent=None):
        super().__init__(Qt.Horizontal, parent)

        self.model = model
        self.setFixedHeight(50)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self.viewport())

        top_height = self.height() // 2

        x = 0
        col = 0

        for sensor in self.model.header_order:

            coeffs = self.model.header_groups[sensor]
            span = len(coeffs)

            width = sum(self.sectionSize(col + i) for i in range(span))

            rect = QRect(x, 0, width, top_height)

            painter.drawRect(rect)
            painter.drawText(rect, Qt.AlignCenter, sensor)

            x += width
            col += span


class AqCalibViewCoeffsStackedWidget(QStackedWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.device_init_widget = DeviceInitWidget()
        self.addWidget(self.device_init_widget)
        self.setCurrentWidget(self.device_init_widget)
        self.show()

