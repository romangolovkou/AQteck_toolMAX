from PyQt5.QtWidgets import QTableView, QHeaderView, QAbstractItemView


class AQ_ParamListTableView(QTableView):
    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.setModel(model)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        self.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.setStyleSheet("""QTableView {color: #D0D0D0;}
                           QTableView::item { padding-left: 3px; }""")
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)

