import sys
import time
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QSplashScreen
from AQ_main_window_frame import AQ_main_window_frame
from AQ_tree_prapare_func import traverse_items
from AQ_session import AQ_CurrentSession
from AQ_EventManager import AQ_EventManager
# Defines
PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_name = 'AQteck Tool MAX'
        PROJ_DIR = 'D:/git/AQtech/AQtech Tool MAX/'
        self.AQicon = QIcon(PROJ_DIR + 'Icons/AQico_silver.png')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle(main_name)
        self.setWindowIcon(self.AQicon)
        self.setGeometry(100, 100, 600, 500)
        self.setMinimumSize(300, 400)
        self.resizeLineWidth = 4
        self.spacing_between_frame = 2
        self.not_titlebtn_zone = 0

        # Менеджер подій
        self.event_manager = AQ_EventManager()
        self.event_manager.register_event_handler('close_' + main_name, self.close)
        self.event_manager.register_event_handler('minimize_' + main_name, self.showMinimized)
        self.event_manager.register_event_handler('maximize_' + main_name, self.showMaximized)
        self.event_manager.register_event_handler('normalize_' + main_name, self.showNormal)
        self.event_manager.register_event_handler('dragging_' + main_name, self.move)
        self.event_manager.register_event_handler('resize_main_window', self.resize_MainWindow)
        # Поточна сессія
        self.current_session = AQ_CurrentSession(self.event_manager, self)

        #MainWindowFrame
        self.main_window_frame = AQ_main_window_frame(self.event_manager, main_name, self.AQicon, self)

    def resize_MainWindow(self, pos_x, pos_y, width, height):
        if pos_x == '%':
            pos_x = self.pos().x()
        if pos_y == '%':
            pos_y = self.pos().y()
        if width == '%':
            width = self.width()
        if height == '%':
            height = self.height()

        self.setGeometry(pos_x, pos_y, width, height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Переопределяем метод resizeEvent и вызываем resize для main_window_frame
        self.main_window_frame.resize(self.width(), self.height())
        event.accept()


    def add_tree_view(self):
        try:
            # device_tree = self.devices_trees[0]
            device_data = self.devices[-1]
            device_tree = device_data.get('device_tree')
            # Створення порожнього массиву параметрів
            self.parameter_list = []
            root = device_tree.invisibleRootItem()
            traverse_items(root, self.parameter_list)

            if isinstance(device_tree, QStandardItemModel):
                # Устанавливаем модель для QTreeView и отображаем его
                address = device_data.get('address')
                device_data['tree_view'] = AQ_TreeView(len(self.devices) - 1, device_tree, address, self.main_field_frame)
                device_data.get('tree_view').show()
                root = device_tree.invisibleRootItem()
                device_data.get('tree_view').traverse_items_show_delegate(root)
                device_data.get('tree_view').read_all_tree_by_modbus(root)
                self.add_dev_widget_to_left_panel(len(self.devices) - 1, device_data)

        # except:
            # print(f"Помилка парсінгу")
        except Exception as e:
            print(f"Error occurred: {str(e)}")

    def read_parameters(self):
        device_data = self.devices[self.current_active_dev_index]
        device_tree = device_data.get('device_tree')
        root = device_tree.invisibleRootItem()
        device_data.get('tree_view').read_all_tree_by_modbus(root)

    def write_parameters(self):
        device_data = self.devices[self.current_active_dev_index]
        device_tree = device_data.get('device_tree')
        root = device_tree.invisibleRootItem()
        device_tree_view = device_data.get('tree_view')
        have_error = device_tree_view.travers_all_tree_have_error_check(root)
        if have_error > 0:
            device_data.get('tree_view').show_have_error_label()
        else:
            device_data.get('tree_view').write_all_tree_by_modbus(root)

    def set_active_cur_device(self, index):
        # Ховаємо всі дерева девайсів
        for i in range(len(self.devices)):
            device_data = self.devices[i]
            tree_view = device_data.get('tree_view', '')
            if not tree_view == '':
                tree_view.hide()

        # Відображаємо поточний активний прилад
        device_data = self.devices[index]
        tree_view = device_data.get('tree_view', '')
        if not tree_view == '':
            tree_view.setGeometry(250, 2, self.main_field_frame.width() - 252, self.main_field_frame.height() - 4)
            tree_view.show()
            self.current_active_dev_index = index


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("D:/git/AQtech/AQtech Tool MAX/Icons/Splash3.png"))
    splash.show()

    # Имитация загрузки (можно заменить на вашу реализацию)
    time.sleep(2)  # Например, 2 секунды

    window = MainWindow()
    # window.showMaximized()
    window.show()
    splash.close()
    sys.exit(app.exec_())
