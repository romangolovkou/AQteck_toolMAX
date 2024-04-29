from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMenu, QTreeView, QHeaderView

from AqTranslateManager import AqTranslateManager
from AqTreeViewDelegates import AqNameTreeDelegate, AqValueTreeDelegate
from AQ_CustomWindowTemplates import AQ_have_error_widget



class AqTreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        name_delegate = AqNameTreeDelegate(self)
        self.setItemDelegateForColumn(0, name_delegate)
        value_delegate = AqValueTreeDelegate(self)
        self.setItemDelegateForColumn(1, value_delegate)
        # Разрешаем отображение скроллбаров
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # border: 1px solid #9ef1d3;
        self.setStyleSheet("""
                            QTreeView {
                                
                                color: #D0D0D0;
                            }
                            QTreeView::item {
                                border: 1px solid #2b2d30;
                            }
                            QTreeView:item:!focus { 
                                background-color: transparent; color: #D0D0D0
                            }
                            QHeaderView::section {
                                border: 1px solid #1e1f22;
                                color: #D0D0D0;
                                background-color: #2b2d30;
                                padding-left: 6px;
                            }
                            QScrollBar:vertical {
                                background: #1e1f22;
                                width: 10px;  /* Ширина вертикального скроллбара */
                            }
                            QScrollBar:horizontal {
                                background: #1e1f22;
                                height: 10px;  /* Высота горизонтального скроллбара */
                            }
                        """)

    def setModel(self, model):
        super().setModel(model)
        first_col_width = 180
        # Получение количества колонок в модели
        column_count = model.columnCount()
        for column in range(column_count):
            col_width = first_col_width if column == 0 else (self.width() - first_col_width)//(column_count - 1)
            self.setColumnWidth(column, col_width)

        root = model.invisibleRootItem()
        self.traverse_items_show_delegate(root)

    def traverse_items_show_delegate(self, item):
        for row in range(item.rowCount()):
            child_item = item.child(row)
            parameter_attributes = child_item.data(Qt.UserRole)
            if parameter_attributes is not None:
                if parameter_attributes.get('is_catalog', 0) == 1:
                    self.traverse_items_show_delegate(child_item)
                else:
                    index = self.model().index(row, 1, item.index())
                    self.openPersistentEditor(index)

    def traverse_items_R_Only_catalog_check(self, item):
        write_flag = 0
        for row in range(item.rowCount()):
            child_item = item.child(row)
            parameter_attributes = child_item.data(Qt.UserRole)
            if parameter_attributes is not None:
                if not (parameter_attributes.get('R_Only', 0) == 1 and parameter_attributes.get('W_Only', 0) == 0):
                    write_flag += 1
            if child_item is not None:
                write_flag += self.traverse_items_R_Only_catalog_check(child_item)

        return write_flag

    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid() and index.column() == 0:
            # Получаем элемент модели по индексу
            item = self.model().itemFromIndex(index)
            cat_or_param_attributes = index.data(Qt.UserRole)
            if item:
                if cat_or_param_attributes.get('is_catalog', 0) == 1:
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
                    action_read = context_menu.addAction(AqTranslateManager.tr("Read parameters"))
                    # Подключаем обработчик события выбора действия
                    action_read.triggered.connect(lambda: self.model().read_parameter(index))
                    if self.traverse_items_R_Only_catalog_check(item) > 0:
                        action_write = context_menu.addAction(AqTranslateManager.tr("Write parameters"))
                        # Подключаем обработчик события выбора действия
                        action_write.triggered.connect(lambda: self.model().write_parameter(index))
                    action_add_to_watch_list = context_menu.addAction(AqTranslateManager.tr("Add to watch list"))
                    action_add_to_watch_list.triggered.connect(lambda: self.model().add_parameter_to_watch_list(index))
                    # # Показываем контекстное меню
                    context_menu.exec(event.globalPos())
                else:
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
                    # action_watch = context_menu.addAction("Add parameter to Watch list")
                    # # Подключаем обработчик события выбора действия
                    # action_watch.triggered.connect(lambda: self.model().add_parameter_to_watch_list(index))
                    # Добавляем действие в контекстное меню
                    action_read = context_menu.addAction(AqTranslateManager.tr("Read parameter"))
                    # Подключаем обработчик события выбора действия
                    action_read.triggered.connect(lambda: self.model().read_parameter(index))
                    if not (cat_or_param_attributes.get("R_Only", 0) == 1 and cat_or_param_attributes.get("W_Only", 0) == 0):
                        action_write = context_menu.addAction(AqTranslateManager.tr("Write parameter"))
                        # Подключаем обработчик события выбора действия
                        action_write.triggered.connect(lambda: self.model().write_parameter(index))
                    action_add_to_watch_list = context_menu.addAction(AqTranslateManager.tr("Add to watch list"))
                    action_add_to_watch_list.triggered.connect(lambda: self.model().add_parameter_to_watch_list(index))

                    # Показываем контекстное меню
                    context_menu.exec(event.globalPos())
        else:
            # Если индекс недействителен, вызывается обработчик события контекстного меню по умолчанию
            super().contextMenuEvent(event)
