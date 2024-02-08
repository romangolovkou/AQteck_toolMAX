import AppCore
from AqAddDeviceWindow import AqAddDeviceWidget
from AqDeviceInfoWidget import AqDeviceInfoWidget
from AqParamListWidget import AqParamListWidget
from AqSetSlaveIdWindow import AqSetSlaveIdWindow
from AqWatchListWindow import AqWatchListWidget
from ui_AqSetSlaveIdWinWidget import Ui_AqSetSlaveIdWidget
from ui_AqWatchListWidget import Ui_AqWatchListWidget
from ui_DeviceInfoDialog import Ui_DeviceInfoDialog
from ui_AqAddDeviceWindow import Ui_AqAddDeviceWindowWidget
from ui_DeviceParamListWindow import Ui_DeviceParamListWidget


def show_device_info_window():
    if AppCore.Core.session.cur_active_device is not None:
        # device_info = AppCore.Core.session.get_current_device_info
        dialog = AqDeviceInfoWidget(Ui_DeviceInfoDialog)
        info_model = AppCore.Core.session.cur_active_device.device_info_model
        dialog.set_device_info_model(info_model)
        dialog.exec()


def show_add_device_window():
    dialog = AqAddDeviceWidget(Ui_AqAddDeviceWindowWidget)
    # dialog = AQ_DialogAddDevices(AppCore.Core.event_manager, None)
    dialog.exec()


def show_device_param_list():
    if AppCore.Core.session.cur_active_device is not None:
        device_model = AppCore.Core.session.cur_active_device.get_device_param_list_model()
        widget = AqParamListWidget(Ui_DeviceParamListWidget, device_model)
        widget.exec()


def show_watch_list_window():
    dialog = AqWatchListWidget(Ui_AqWatchListWidget)
    # Потрібно show замість exec, для немодального вікна
    dialog.show()


def show_set_slave_id_window():
    dialog = AqSetSlaveIdWindow(Ui_AqSetSlaveIdWidget)
    dialog.exec()


