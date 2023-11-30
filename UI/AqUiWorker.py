from AqAddDeviceWindow import AqAddDeviceWidget
from AqDeviceInfoWidget import AqDeviceInfoWidget
from DeviceModels import AqDeviceInfoModel
from ui_DeviceInfoDialog import Ui_DeviceInfoDialog
from ui_AqAddDeviceWindow import Ui_AqAddDeviceWindowWidget


def show_device_info_window(device_info: AqDeviceInfoModel):
    dialog = AqDeviceInfoWidget(Ui_DeviceInfoDialog)
    # dialog.ui.pushButton.clicked.connect()
    dialog.set_device_info_model()
    dialog.exec()

def show_add_device_window():
    dialog = AqAddDeviceWidget(Ui_AqAddDeviceWindowWidget)
    dialog.exec()
