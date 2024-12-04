from PySide6.QtWidgets import QTableWidget, QLineEdit

from AqLineEditTemplates import AqFloatLineEdit
from AqTranslateManager import AqTranslateManager


class AqCalibCoeffTable(QTableWidget):

    ch_name_col = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setMinimumSectionSize(8)
        self.setRowCount(0)
        self.setFixedWidth(420)
        self.setMaximumHeight(420)
        self.verticalHeader().hide()
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        # Убираем рамку таблицы
        self.setStyleSheet("""QTableWidget { border: none; color: #D0D0D0; background-color: #16191d;}
                            QTableWidget::item { padding-left: 3px; }
                            QTableWidget::item:!focus {
                            background-color: transparent;}
                            QScrollBar:vertical {
                                background: #1e1f22;
                                width: 10px;  /* Ширина вертикального скроллбара */
                            }
                            QScrollBar:horizontal {
                                background: #1e1f22;
                                height: 10px;  /* Высота горизонтального скроллбара */
                            }
                            """)

    def load_table(self, ch_list):
        self.setRowCount(0)
        col_count = 0
        col_name_list = list()
        for channel in ch_list:
            coeffs = channel['coeff']
            keys = list(coeffs.keys())
            if len(keys) > col_count:
                col_count = len(keys)
                col_name_list = keys

        col_name_list.sort()
        col_name_list = [AqTranslateManager.tr('Channel')] + col_name_list
        col_count += 1
        self.setColumnCount(col_count)

        for i in range(len(col_name_list)):
            self.horizontalHeaderItem(i).setText(col_name_list[i])

        for channel in ch_list:
            self.append_row(channel)

    def append_row(self, context: dict):
        # if new_row_index is None:
        new_row_index = self.rowCount()
        if new_row_index == 31:
            return
        self.setRowCount(self.rowCount() + 1)
        # Создаем элементы таблицы для каждой строки
        ch_name_item = QLineEdit(str(context['name']))
        ch_name_item.setReadOnly(True)
        ch_name_item.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent; padding-left: 10px;\n")
        self.setCellWidget(new_row_index, self.ch_name_col, ch_name_item)

        keys = list(context['coeff'].keys())
        keys.sort()
        coeff_col_num = dict()

        for i in range(len(keys)):
            coeff_col_num[keys[i]] = i + 1

        if 'a' in keys:
            a_coeff_item = AqCalibTableFloatLineEdit(self)
            a_coeff_item.setText(str(context['coeff']['a']['value']))
            a_coeff_item.set_error(context['coeff']['a']['coeff_error'])
            self.setCellWidget(new_row_index, coeff_col_num['a'], a_coeff_item)
        if 'b' in keys:
            b_coeff_item = AqCalibTableFloatLineEdit(self)
            b_coeff_item.setText(str(context['coeff']['b']['value']))
            b_coeff_item.set_error(context['coeff']['b']['coeff_error'])
            self.setCellWidget(new_row_index, coeff_col_num['b'], b_coeff_item)
        if 'c' in keys:
            c_coeff_item = AqCalibTableFloatLineEdit(self)
            c_coeff_item.setText(str(context['coeff']['c']['value']))
            c_coeff_item.set_error(context['coeff']['c']['coeff_error'])
            self.setCellWidget(new_row_index, coeff_col_num['c'], c_coeff_item)
        if 'k' in keys:
            k_coeff_item = AqCalibTableFloatLineEdit(self)
            k_coeff_item.setText(str(context['coeff']['k']['value']))
            k_coeff_item.set_error(context['coeff']['k']['coeff_error'])
            self.setCellWidget(new_row_index, coeff_col_num['k'], k_coeff_item)


class AqCalibTableFloatLineEdit(AqFloatLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)

    def set_error(self, error):
        if error is True:
            self.setStyleSheet("""
                QToolTip {
                    font-size: 14px;  /* Размер шрифта */
                    color: white;     /* Цвет текста */
                    background-color: #2b2d30;  /* Цвет фона */
                    border: 1px solid red;  /* Граница */
                    border-radius: 4px;  /* Радиус закругления */
                }

                QWidget {
                    border: none; 
                    color: #D0D0D0; 
                    background-color: #df2d30;
                }
            """)
            self.setToolTip(AqTranslateManager.tr('The coefficients for this channel will not be applied!\n'
                                                  '\n'
                                                  'The coefficient is outside the acceptable range.\n'
                                                  'This channel needs to be recalibrated.\n'))
        else:
            self.setStyleSheet("border: none; color: #D0D0D0; background-color: transparent;\n")


