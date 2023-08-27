from PyQt5.QtCore import QObject

class AQ_Device(QObject):
    def __init__(self, event_manager, client, parent=None):
        super().__init__()
        self.name = None
        self.serial = None
        self.address = None
        self.client = None
        self.device_tree = None

