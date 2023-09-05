from PyQt5.QtGui import QStandardItem


class AQ_param_item(QStandardItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if (new_value < 18):
            raise ValueError("Sorry you age is below eligibility criteria")
        print("setter method called")
        self._value = new_value

class AQ_catalog_item(QStandardItem):
    def __init__(self, name):
        super().__init__(name)
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if (new_value < 18):
            raise ValueError("Sorry you age is below eligibility criteria")
        print("setter method called")
        self._value = new_value

class AQ_param_manager_item(QStandardItem):
    def __init__(self, sourse_item, event_manager, device):
        sourse_item
        super().__init__(name)
        self._value = None