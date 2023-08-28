from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QFrame, QGraphicsView, QGraphicsScene, \
                            QGraphicsPixmapItem, QTableWidget, QTableWidgetItem, QCheckBox


class AQ_AddDevices_table_widget(QTableWidget):
    def __init__(self, event_manager, parent):
        super().__init__(parent)
        # Создаем QTableWidget с 4 столбцами
        self.setColumnCount(4)
        self.horizontalHeader().setMinimumSectionSize(8)

        # Добавляем заголовки столбцов
        self.setHorizontalHeaderLabels(["", "Name", "Address", "Version"])
        self.setFixedWidth(self.parent.width() // 2 + 20)
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



    def set_style_table_widget(self, row, err_flag=0):
        if err_flag == 0:
            for i in range(4):
                self.table_widget.item(row, i).setBackground(QColor("#429061"))
        else:
            for i in range(4):
                self.table_widget.item(row, i).setBackground(QColor("#9d4d4f"))

    def add_device_to_table_widget(self, index, device_data, err_flag=0):
        self.setRowCount(index + 1)
        # Создаем элементы таблицы для каждой строки
        checkbox_item = QTableWidgetItem()
        name_item = QTableWidgetItem(device_data.get('device_name') + ' S/N' + device_data.get('serial_number'))
        name_item.setFlags(self.name_item.flags() & ~Qt.ItemIsEditable)
        address_item = QTableWidgetItem(device_data.get('address'))
        address_item.setFlags(self.address_item.flags() & ~Qt.ItemIsEditable)
        version_item = QTableWidgetItem(device_data.get('version'))
        version_item.setFlags(self.version_item.flags() & ~Qt.ItemIsEditable)

        # Устанавливаем элементы таблицы
        self.setItem(index, 0, checkbox_item)
        self.setItem(index, 1, name_item)
        self.setItem(index, 2, address_item)
        self.setItem(index, 3, version_item)
        new_height = self.height() + self.rowHeight(index)
        if new_height > 420:
            new_height = 420
        self.setFixedHeight(new_height)

        # Устанавливаем чекбокс в первую колонку
        checkbox = QCheckBox()
        if err_flag == 0:
            checkbox.setChecked(True)
        else:
            checkbox.setChecked(False)
            checkbox.setEnabled(False)

        checkbox.setStyleSheet("QCheckBox { background-color: transparent; border: none;}")
        self.setCellWidget(index, 0, checkbox)
        item = self.item(index, 0)
        item.setTextAlignment(Qt.AlignCenter)

        self.set_style_table_widget(self.finded_dev_count, err_flag)

        bottom_right_corner_table_widget = self.table_widget.mapTo(self.main_window_frame,
                                                                   self.table_widget.rect().bottomRight())

        if hasattr(self, 'add_btn'):
            self.add_btn.deleteLater()
        # Создаем кнопку поиска
        self.add_btn = QPushButton("Add device", self.main_window_frame)
        self.add_btn.setFont(QFont("Verdana", 10))  # Задаем шрифт и размер
        self.add_btn.setFixedSize(100, 35)
        self.add_btn.move(bottom_right_corner_table_widget.x() - self.add_btn.width() - 3,
                          bottom_right_corner_table_widget.y() + 5)
        self.add_btn.clicked.connect(self.add_finded_devices)
        self.add_btn.setStyleSheet("""
                    QPushButton {
                        border-left: 1px solid #9ef1d3;
                        border-top: 1px solid #9ef1d3;
                        border-bottom: 1px solid #5bb192;
                        border-right: 1px solid #5bb192;
                        color: #D0D0D0;
                        background-color: #2b2d30;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #3c3e41;
                    }
                    QPushButton:pressed {
                        background-color: #429061;
                    }
                """)

        self.add_btn.show()