from PySide6.QtCore import QSettings


def load_last_combobox_state(settings: QSettings, combobox):
    key = combobox.objectName()
    index = settings.value(key, 0, type=int)
    try:
        combobox.setCurrentIndex(index)
    except:
        combobox.setCurrentIndex(0)


def save_combobox_current_state(settings: QSettings, combobox):
    key = combobox.objectName()
    index = combobox.currentIndex()
    if index < 0:
        return

    settings.setValue(key, index)
    settings.sync()


def load_last_text_value(settings: QSettings, edit_line):
    key = edit_line.objectName()
    text = settings.value(key, "", type=str)
    edit_line.setText(text)


def save_current_text_value(settings: QSettings, edit_line):
    key = edit_line.objectName()
    text = edit_line.text()
    settings.setValue(key, text)
    settings.sync()


def get_last_path(settings: QSettings, key):
    path = settings.value(key, "", type=str)
    return path


def save_last_path(settings: QSettings, key, path):
    settings.setValue(key, path)
    settings.sync()
