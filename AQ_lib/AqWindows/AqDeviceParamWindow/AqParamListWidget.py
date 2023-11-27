from PySide6.QtWidgets import QWidget

from DeviceModels import AqDeviceParamListModel

class AqParamListWidget(QWidget):
    def __init__(self, dev_info: AqDeviceParamListModel = None):
        if dev_info is None:
            dev_info = generateTestData();








