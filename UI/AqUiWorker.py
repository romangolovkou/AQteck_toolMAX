import AppCore
from AQ_AddDevicesWindow import AQ_DialogAddDevices
from AqAddDeviceWindow import AqAddDeviceWidget
from AqDeviceInfoWidget import AqDeviceInfoWidget
from AqDeviceParamListModel import AqDeviceParamListModel
from AqParamListWidget import AqParamListWidget
from DeviceModels import AqDeviceInfoModel
from ui_DeviceInfoDialog import Ui_DeviceInfoDialog
from ui_AqAddDeviceWindow import Ui_AqAddDeviceWindowWidget
from ui_DeviceParamListWindow import Ui_DeviceParamListWidget


def show_device_info_window(device_info: AqDeviceInfoModel):
    dialog = AqDeviceInfoWidget(Ui_DeviceInfoDialog)
    # dialog.ui.pushButton.clicked.connect()
    dialog.set_device_info_model()
    dialog.exec()

def show_add_device_window():
    dialog = AqAddDeviceWidget(Ui_AqAddDeviceWindowWidget)
    # dialog = AQ_DialogAddDevices(AppCore.Core.event_manager, None)
    dialog.exec()

def show_device_param_list(device_param_model: AqDeviceParamListModel):
    # widget = AqParamListWidget(Ui_DeviceParamListWidget, device_param_model)
    widget = AqParamListWidget(Ui_DeviceParamListWidget)
    widget.exec()


