import AppCore
from AqAddDeviceWindow import AqAddDeviceWidget
from AqDeviceInfoWidget import AqDeviceInfoWidget
from AqGatewayWindow import AqGatewayWindow
from AqMessageManager import AqMessageManager
from AqParamListWidget import AqParamListWidget
from AqRtcWindow import AqRtcWindow
from AqSetPasswordWidget import AqSetPasswordWindow
from AqSetSlaveIdWindow import AqSetSlaveIdWindow
from AqTranslateManager import AqTranslateManager
from AqWatchListWindow import AqWatchListWidget
from ui_AqGatewayWindow import Ui_AqGatewayWidget
from ui_AqSetPasswordWidget import Ui_AqSetPasswordWidget
from ui_AqSetRtcWidget import Ui_AqRtcWidget
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
        if info_model is not None:
            dialog.set_device_info_model(info_model)
            dialog.exec()
        else:
            AqMessageManager.get_global_message_manager().send_message('main', 'Error', AqTranslateManager.tr('Can`t read device info'))


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


def show_set_rtc():
    if AppCore.Core.session.cur_active_device is not None:
        widget = AqRtcWindow(Ui_AqRtcWidget)
        widget.set_device_date_time(AppCore.Core.session.cur_active_device.get_device_date_time())
        widget.set_write_handler(AppCore.Core.session.cur_active_device.write_device_date_time)
        widget.exec()


def show_set_password():
    if AppCore.Core.session.cur_active_device is not None:
        widget = AqSetPasswordWindow(Ui_AqSetPasswordWidget)
        widget.set_working_device(AppCore.Core.session.cur_active_device)
        widget.exec()


def show_gateway():
    if AppCore.Core.session.cur_active_device is not None:
        widget = AqGatewayWindow(Ui_AqGatewayWidget)
        widget.set_working_device(AppCore.Core.session.cur_active_device)
        widget.exec()
