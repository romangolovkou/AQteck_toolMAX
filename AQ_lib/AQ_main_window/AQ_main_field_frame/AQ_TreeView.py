from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMenu, QTreeView

from AQ_TreeViewDelegates import AQ_NameTreeDelegate, AQ_ValueTreeDelegate
from AQ_CustomWindowTemplates import AQ_wait_progress_bar_widget, AQ_have_error_widget



class AQ_TreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        name_delegate = AQ_NameTreeDelegate(self)
        self.setItemDelegateForColumn(0, name_delegate)
        value_delegate = AQ_ValueTreeDelegate(self)
        self.setItemDelegateForColumn(1, value_delegate)
        # Разрешаем отображение скроллбаров
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setStyleSheet("""
                            QTreeView {
                                border: 1px solid #9ef1d3;
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
        # Получение количества колонок в модели
        column_count = model.columnCount()
        for column in range(column_count):
            self.setColumnWidth(column, 200)

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
                    action_read = context_menu.addAction("Read parameters")
                    # Подключаем обработчик события выбора действия
                    action_read.triggered.connect(lambda: self.model().read_parameter(index))
                    if self.traverse_items_R_Only_catalog_check(item) > 0:
                        action_write = context_menu.addAction("Write parameters")
                        # Подключаем обработчик события выбора действия
                        action_write.triggered.connect(lambda: self.model().write_parameter(index))
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
                    action_read = context_menu.addAction("Read parameter")
                    # Подключаем обработчик события выбора действия
                    action_read.triggered.connect(lambda: self.model().read_parameter(index))
                    if not (cat_or_param_attributes.get("R_Only", 0) == 1 and cat_or_param_attributes.get("W_Only", 0) == 0):
                        action_write = context_menu.addAction("Write parameter")
                        # Подключаем обработчик события выбора действия
                        action_write.triggered.connect(lambda: self.model().write_parameter(index))

                    # Показываем контекстное меню
                    context_menu.exec(event.globalPos())
        else:
            # Если индекс недействителен, вызывается обработчик события контекстного меню по умолчанию
            super().contextMenuEvent(event)

    def show_have_error_label(self):
        # Получаем координаты поля ввода относительно диалогового окна
        self.have_err_widget = AQ_have_error_widget("<html>Writing is not possible.<br>One or more parameters<br>\
                                                        have incorrect values<html>", self.parent)
        self.have_err_widget.move(self.parent.width() // 2 - self.have_err_widget.width() // 2,
                                  self.parent.height() // 3 - self.have_err_widget.height() // 2)
        self.have_err_widget.show()
        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.have_err_widget.deleteLater)

    def show_read_error_label(self):
        # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
        self.read_err_widget = AQ_have_error_widget("<html>Failed to read value.<br>The device is offline, connect<br>\
                                                        the device and try again<html>", self.parent)
        self.read_err_widget.move(self.parent.width() // 2 - self.read_err_widget.width() // 2,
                                  self.parent.height() // 3 - self.read_err_widget.height() // 2)
        self.read_err_widget.show()
        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.read_err_widget.deleteLater)

    def show_write_error_label(self):
        # Получаем координаты поля ввода относительно диалогового окна #9d4d4f
        self.write_err_widget = AQ_have_error_widget("<html>Failed to write value.<br>The device is offline, connect<br>\
                                                        the device and try again<html>", self.parent)
        self.write_err_widget.move(self.parent.width() // 2 - self.write_err_widget.width() // 2,
                                   self.parent.height() // 3 - self.write_err_widget.height() // 2)
        self.write_err_widget.show()
        # Запускаем таймер на 4 секунды, чтобы скрыть плашку
        QTimer.singleShot(4000, self.write_err_widget.deleteLater)
