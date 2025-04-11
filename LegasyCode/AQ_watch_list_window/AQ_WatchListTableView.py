from PySide2.QtWidgets import QTableView, QHeaderView, QAbstractItemView


class AQ_WatchListTableView(QTableView):
    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.setModel(model)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2b2d30; color: #D0D0D0; border: 1px solid #1e1f22; }")
        self.horizontalHeader().setSectionResizeMode(model.columnCount() - 1, QHeaderView.Stretch)
        self.setStyleSheet("""QTableView {color: #D0D0D0;}
                           QTableView::item { padding-left: 3px; }
                           QTableView:item:!focus { background-color: transparent; color: #D0D0D0}""")
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
