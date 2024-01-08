from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu

from AqTreeView import AqTreeView


class AqWatchTreeView(AqTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid() and index.column() == 0:
            # Получаем элемент модели по индексу
            item = self.model().itemFromIndex(index)
            cat_or_param_attributes = index.data(Qt.UserRole)
            if item:
                # if cat_or_param_attributes.get('is_catalog', 0) == 1:
                    # Создаем контекстное меню
                    context_menu = QMenu(self)
                    context_menu.setStyleSheet("""
                                            QMenu {
                                                color: #D0D0D0;
                                            }

                                            QMenu::item:selected {
                                                background-color: #3a3a3a;
                                                color: #FFFFFF;
                                            }

                                            QMenu::item:disabled {
                                                color: #808080; /* Цвет для неактивных действий */
                                            }
                                        """)
                    # # Добавляем действие в контекстное меню
                    # action_watch = context_menu.addAction("Add parameters to Watch list")
                    # # Подключаем обработчик события выбора действия
                    # action_watch.triggered.connect(lambda: self.model().add_parameter_to_watch_list(index))
                    # Добавляем действие в контекстное меню
                    # action_read = context_menu.addAction("Read parameters")
                    # # Подключаем обработчик события выбора действия
                    # action_read.triggered.connect(lambda: self.model().read_parameter(index))
                    # if self.traverse_items_R_Only_catalog_check(item) > 0:
                    #     action_write = context_menu.addAction("Write parameters")
                    #     # Подключаем обработчик события выбора действия
                    #     action_write.triggered.connect(lambda: self.model().write_parameter(index))
                    # action_add_to_watch_list = context_menu.addAction("Add to watch list")
                    # action_add_to_watch_list.triggered.connect(lambda: self.model().add_parameter_to_watch_list(index))
                    action_delete = context_menu.addAction("Delete")
                    # Подключаем обработчик события выбора действия
                    action_delete.triggered.connect(lambda: self.model().read_parameter(index))
                    # # Показываем контекстное меню
                    context_menu.exec(event.globalPos())
                # else:
                #     # Создаем контекстное меню
                #     context_menu = QMenu(self)
                #     context_menu.setStyleSheet("""
                #                             QMenu {
                #                                 color: #D0D0D0;
                #                             }
                #
                #                             QMenu::item:selected {
                #                                 background-color: #3a3a3a;
                #                                 color: #FFFFFF;
                #                             }
                #
                #                             QMenu::item:disabled {
                #                                 color: #808080; /* Цвет для неактивных действий */
                #                             }
                #                         """)
                #     # # Добавляем действие в контекстное меню
                #     # action_watch = context_menu.addAction("Add parameter to Watch list")
                #     # # Подключаем обработчик события выбора действия
                #     # action_watch.triggered.connect(lambda: self.model().add_parameter_to_watch_list(index))
                #     # Добавляем действие в контекстное меню
                #     action_read = context_menu.addAction("Read parameter")
                #     # Подключаем обработчик события выбора действия
                #     action_read.triggered.connect(lambda: self.model().read_parameter(index))
                #     if not (cat_or_param_attributes.get("R_Only", 0) == 1 and cat_or_param_attributes.get("W_Only", 0) == 0):
                #         action_write = context_menu.addAction("Write parameter")
                #         # Подключаем обработчик события выбора действия
                #         action_write.triggered.connect(lambda: self.model().write_parameter(index))
                #     action_add_to_watch_list = context_menu.addAction("Add to watch list")
                #     action_add_to_watch_list.triggered.connect(lambda: self.model().add_parameter_to_watch_list(index))
                #
                #     # Показываем контекстное меню
                #     context_menu.exec(event.globalPos())
        else:
            # Если индекс недействителен, вызывается обработчик события контекстного меню по умолчанию
            super().contextMenuEvent(event)
