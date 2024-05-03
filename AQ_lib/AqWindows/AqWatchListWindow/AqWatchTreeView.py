from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu

from AqTranslateManager import AqTranslateManager
from AqTreeView import AqTreeView
from AqWatchListCore import AqWatchListCore


class AqWatchTreeView(AqTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid() and index.column() == 0:
            # Получаем элемент модели по индексу
            item = self.model().itemFromIndex(index)
            # cat_or_param_attributes = index.data(Qt.UserRole)
            if item:
                # Создаем контекстное меню
                context_menu = QMenu(self)
                context_menu.setStyleSheet("""
                                        QMenu {
                                            color: #D0D0D0;
                                            background-color: transparent;
                                        }

                                        QMenu::item:selected {
                                            background-color: #3a3a3a;
                                            color: #FFFFFF;
                                        }

                                        QMenu::item:disabled {
                                            color: #808080; /* Цвет для неактивных действий */
                                        }
                                    """)
                action_delete = context_menu.addAction(AqTranslateManager.tr("Remove"))
                # Подключаем обработчик события выбора действия
                action_delete.triggered.connect(lambda: self.removeItem(item))
                # # Показываем контекстное меню
                context_menu.exec(event.globalPos())

        else:
            # Если индекс недействителен, вызывается обработчик события контекстного меню по умолчанию
            super().contextMenuEvent(event)

    def removeItem(self, item):
        param_attributes = item.get_param_attributes()
        if param_attributes.get('is_catalog', 0) == 1:
            AqWatchListCore.removeItem(item.watchItem)
        else:
            AqWatchListCore.removeItem(item.get_sourse_item())

    def removeAllItems(self):
        row_count = self.model().invisibleRootItem().rowCount()
        for row in range(row_count):
            child_item = self.model().invisibleRootItem().child(0)
            self.removeItem(child_item)

    def writeWatchItemParameter(self, items_to_write):
        AqWatchListCore.writeWatchedItemParam(items_to_write)
