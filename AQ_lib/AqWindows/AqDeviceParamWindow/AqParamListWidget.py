import csv
import os

from PySide2.QtCore import Qt, QSettings
from PySide2.QtGui import QScreen
from PySide2.QtWidgets import QWidget, QFrame, QTableWidget, QDialog, QTableWidgetItem, QLineEdit, QFileDialog

import ModbusTableDataFiller
from AqSettingsFunc import AqSettingsManager
from AqTranslateManager import AqTranslateManager
from AqWindowTemplate import AqDialogTemplate
from AqDeviceParamListModel import AqDeviceParamListModel


class AqParamListWidget(AqDialogTemplate):
    def __init__(self, _ui, dev_info: AqDeviceParamListModel = None, parent=None):
        super().__init__(parent)
        self.ui = _ui()
        self.ui.setupUi(self.content_widget)
        self.minimizeBtnEnable = False
        self.maximizeBtnEnable = False

        self.name = AqTranslateManager.tr('Parameters list')
        self.auto_load_settings = None
        self.loadLastPath()

        self.ui.saveBtn.clicked.connect(self.saveToFile)

        self.device_str = ''.join((dev_info.name, ' S/N: ', dev_info.serial))
        self.ui.deviceInfoLabel.setText(self.device_str)

        self.ui.tableView.clear()
        self.ui.tableView.fillModbusData(dev_info.param_list)
        self.ui.infoFrame.setData(dev_info.network_info)

        self.ui.tableView.horizontalHeader().sectionResized.connect(self.customAdjustSize)
        self.customAdjustSize()

    def customAdjustSize(self, *args):
        self.ui.tableView.adjustSize()
        self.adjustSize()
        super().adjustSize()

    #TODO: сделать отдельной бибкой, доступ через CORE
    def loadLastPath(self):
        try:
            # Получаем текущий рабочий каталог (папку проекта)
            project_path = os.getcwd()
            roaming_path = os.path.join(os.getenv('APPDATA'), 'AQteck tool MAX', 'Roaming')
            # Проверяем наличие папки Roaming, если её нет - создаем
            if not os.path.exists(roaming_path):
                os.makedirs(roaming_path)
            # Объединяем путь к папке проекта с именем файла настроек
            settings_path = os.path.join(roaming_path, "auto_load_settings.ini")
            # Используем полученный путь в QSettings
            self.auto_load_settings = QSettings(settings_path, QSettings.IniFormat)
        except:
            self.auto_load_settings = None

    def saveToFile(self):
        # Сохраняем данные в файл CSV
        def_name = self.device_str.replace('S/N:','').replace(' ', '_') + '.csv'
        # Начальный путь для диалога
        initial_path = AqSettingsManager.get_last_path('param_list_csv_path')
        if initial_path == '':
            initial_path = "C:/"
        self.file_dialog = QFileDialog(self)
        options = self.file_dialog.options()
        # options |= self.file_dialog.DontUseNativeDialog

        path = initial_path + '/' + def_name

        # Открываем диалог для выбора файла и места сохранения
        filename, _ = self.file_dialog.getSaveFileName(self, "Save parameters as CSV", path, "CSV Files (*.csv);;All Files (*)", options=options)
        if filename != '':
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')

                # Записываем заголовки (названия колонок)
                headers = [self.ui.tableView.horizontalHeaderItem(col).text()
                           for col in range(self.ui.tableView.columnCount())]
                writer.writerow(headers)

                # Записуємо дані з моделі з параметрами
                for row in range(self.ui.tableView.rowCount()):
                    row_data = [self.ui.tableView.item(row, col).text()
                                for col in range(self.ui.tableView.columnCount())]
                    writer.writerow(row_data)
            # Извлекаем путь к каталогу
            directory_path = os.path.dirname(filename)
            AqSettingsManager.save_last_path('param_list_csv_path', directory_path)


class AqParamListInfoFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setData(self, str_list: list):
        self.clear()
        for i in str_list:
            row = QLineEdit(self)
            row.setReadOnly(True)
            row.setText(str(i))
            self.layout().addWidget(row)

    def clear(self):
        while self.layout().count() > 0:
            w_item = self.layout().takeAt(0)
            w_item.widget().setParent(None)
            del w_item


class AqParamListTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def fillModbusData(self, param_list: list):
        self.clear()
        ModbusTableDataFiller.fill_table_with_modbus_items(self, param_list)



    """Base item list class
    provide functionality by add data to table, set size, resize, etc"""

    def adjustSize(self):
        content_height = self.horizontalHeader().height()
        content_width = self.verticalHeader().width()
        for i in range(self.rowCount()):
            content_height += self.rowHeight(i)

        for i in range(self.columnCount()):
            content_width += self.columnWidth(i)

        if content_height > self.parent().maximumHeight():
            content_height = self.parent().maximumHeight()

        self.setFixedSize(content_width, content_height)

        self.parent().adjustSize()









