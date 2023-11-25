from AqDeviceInfoWidget import AqDeviceInfoWidget
from DeviceModels import AqDeviceInfoModel
from ui_DeviceInfoDialog import Ui_DeviceInfoDialog


def show_device_info_window(device_info: AqDeviceInfoModel):
    dialog = AqDeviceInfoWidget(Ui_DeviceInfoDialog)
    # dialog.ui.pushButton.clicked.connect()
    dialog.set_device_info_model()
    dialog.exec()


