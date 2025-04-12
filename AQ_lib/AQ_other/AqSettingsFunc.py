import os

from PySide2.QtCore import QSettings, QObject


class AqSettingsManager(QObject):
    _auto_load_settings = None

    @classmethod
    def init(cls):
        cls._auto_load_settings = cls.get_auto_load_settings()

    @classmethod
    def get_auto_load_settings(cls):
        try:
            # Получаем текущий рабочий каталог (папку проекта)
            roaming_path = os.path.join(os.getenv('APPDATA'), 'AQteck tool MAX', 'Roaming')
            # Проверяем наличие папки Roaming, если её нет - создаем
            if not os.path.exists(roaming_path):
                os.makedirs(roaming_path)
            # Объединяем путь к папке проекта с именем файла настроек
            settings_path = os.path.join(roaming_path, "auto_load_settings.ini")
            # Используем полученный путь в QSettings
            auto_load_settings = QSettings(settings_path, QSettings.IniFormat)
            return auto_load_settings
        except Exception as e:
            print(e)
            print('File "auto_load_settings.ini" not found')
            return None

    @classmethod
    def load_last_combobox_state(cls, combobox):
        if cls._auto_load_settings:
            key = combobox.objectName()
            index = cls._auto_load_settings.value(key, 0, type=int)
            try:
                combobox.setCurrentIndex(index)
                while combobox.currentText() == '' and index > 0:
                    index -= 1
                    combobox.setCurrentIndex(index)

            except:
                combobox.setCurrentIndex(0)

    @classmethod
    def save_combobox_current_state(cls, combobox):
        if cls._auto_load_settings:
            key = combobox.objectName()
            index = combobox.currentIndex()
            if index < 0:
                return

            cls._auto_load_settings.setValue(key, index)
            cls._auto_load_settings.sync()

    @classmethod
    def load_last_text_value(cls, edit_line):
        if cls._auto_load_settings:
            key = edit_line.objectName()
            text = cls._auto_load_settings.value(key, "", type=str)
            edit_line.setText(text)

    @classmethod
    def save_current_text_value(cls, edit_line):
        if cls._auto_load_settings:
            key = edit_line.objectName()
            text = edit_line.text()
            cls._auto_load_settings.setValue(key, text)
            cls._auto_load_settings.sync()

    @classmethod
    def load_last_ip_list(cls, edit_line):
        if cls._auto_load_settings:
            key = edit_line.objectName()
            ips_string = cls._auto_load_settings.value(key, "", type=str)
            ip_list = ips_string.split(';')
            edit_line.setText(ip_list[0])
            edit_line.set_last_ip_list(ip_list)

    @classmethod
    def save_current_ip_to_list(cls, edit_line):
        MAX_SAVED_IP = 10
        if cls._auto_load_settings:
            key = edit_line.objectName()
            text = edit_line.text()
            ips_string = cls._auto_load_settings.value(key, "", type=str)
            ip_list = ips_string.split(';')
            if len(ip_list) > (MAX_SAVED_IP - 1):
                ip_list = ip_list[0:(MAX_SAVED_IP - 1)]

            if text in ip_list:
                ip_list.remove(text)

            ip_list.insert(0, text)

            ips_string = ';'.join(ip_list)

            cls._auto_load_settings.setValue(key, ips_string)
            cls._auto_load_settings.sync()

    @classmethod
    def get_last_path(cls, key):
        if cls._auto_load_settings:
            path = cls._auto_load_settings.value(key, "", type=str)
            return path

    @classmethod
    def save_last_path(cls, key, path):
        if cls._auto_load_settings:
            cls._auto_load_settings.setValue(key, path)
            cls._auto_load_settings.sync()
