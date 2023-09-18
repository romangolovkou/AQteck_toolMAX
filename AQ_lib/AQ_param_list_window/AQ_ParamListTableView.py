from PyQt5.QtWidgets import QTableView, QHeaderView


class AQ_ParamListTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        # Убираем рамку таблицы
        self.setStyleSheet("""QTableView {color: #D0D0D0;}
                           QTableView::item { padding-left: 3px; }""")
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
