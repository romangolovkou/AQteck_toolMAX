from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import Qt


class AQ_addDevice_TableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаем QTableWidget с 4 столбцами
        self.setColumnCount(4)
        self.horizontalHeader().setMinimumSectionSize(8)
        self.setRowCount(0)

        # Добавляем заголовки столбцов
        self.setHorizontalHeaderLabels(["", "Name", "Address", "Version"])
        self.setFixedWidth(420)
        self.setMaximumHeight(420)
        # Устанавливаем ширину столбцов
        cur_width = self.width()
        self.setColumnWidth(0, int(cur_width * 0.05))
        self.setColumnWidth(1, int(cur_width * 0.48))
        self.setColumnWidth(2, int(cur_width * 0.27))
        self.setColumnWidth(3, int(cur_width * 0.20))
        # Установите высоту строк по умолчанию
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        # Убираем рамку таблицы
        self.setStyleSheet("""QTableWidget { border: none; color: #D0D0D0;}
                                                   QTableWidget::item { padding-left: 3px; }""")

    def set_style_table_widget_item(self, row, err_flag=0):
        if err_flag == 0:
            for i in range(4):
                self.item(row, i).setBackground(QColor("#429061"))
        else:
            for i in range(4):
                self.item(row, i).setBackground(QColor("#9d4d4f"))

    def append_device_row(self, device_data):
        if device_data.get('status', 'data_error') == 'ok':
            err_flag = 0
        else:
            err_flag = 1

        new_row_index = self.rowCount()
        self.setRowCount(self.rowCount() + 1)
        # Создаем элементы таблицы для каждой строки
        checkbox_item = QTableWidgetItem()
        name_item = QTableWidgetItem(device_data.get('device_name') + ' S/N' + device_data.get('serial_number'))
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        address_item = QTableWidgetItem(device_data.get('address'))
        address_item.setFlags(address_item.flags() & ~Qt.ItemIsEditable)
        version_item = QTableWidgetItem(device_data.get('version'))
        version_item.setFlags(version_item.flags() & ~Qt.ItemIsEditable)

        # Устанавливаем элементы таблицы
        self.setItem(new_row_index, 0, checkbox_item)
        self.setItem(new_row_index, 1, name_item)
        self.setItem(new_row_index, 2, address_item)
        self.setItem(new_row_index, 3, version_item)

        # Устанавливаем чекбокс в первую колонку
        checkbox = QCheckBox()
        if err_flag == 0:
            checkbox.setChecked(True)
        else:
            checkbox.setChecked(False)
            checkbox.setEnabled(False)

        checkbox.setStyleSheet("QCheckBox { background-color: transparent; border: none;}")
        self.setCellWidget(new_row_index, 0, checkbox)
        item = self.item(new_row_index, 0)
        item.setTextAlignment(Qt.AlignCenter)

        self.set_style_table_widget_item(new_row_index, err_flag)

    def get_sum_of_rows_height(self):
        sum_height = 0
        for i in range(self.rowCount()):
            sum_height += self.rowHeight(i)

        return sum_height