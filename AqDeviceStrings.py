from PySide6.QtCore import QCoreApplication

protocol_modbus_str = QCoreApplication.translate("AqDeviceStrings", "Protocol: Modbus", None)
byte_order_ms_str = QCoreApplication.translate("AqDeviceStrings", "Byte order: Most significant byte first", None)
byte_order_ls_str = QCoreApplication.translate("AqDeviceStrings", "Byte order: Least significant byte first", None)
register_order_ms_str = QCoreApplication.translate("AqDeviceStrings", "Register order: Most significant register first", None)
register_order_ls_str = QCoreApplication.translate("AqDeviceStrings", "Register order: Least significant register first", None)


def get_translated_string(string_id):
    return eval(string_id)

