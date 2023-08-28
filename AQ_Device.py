from PyQt5.QtCore import QObject

class AQ_Device(QObject):
    def __init__(self, event_manager, address_tuple, parent=None):
        super().__init__()
        self.name = None
        self.serial = None
        self.address = None
        self.client = None
        self.device_tree = None
        self.address_tuple = address_tuple


    def create_client(self, address_tuple):
        interface = address_tuple[0]
        address = address_tuple[1]
        if interface == "Ethernet":
            try:
                ip = self.ip_line_edit.text()
            except:
                return 'empty_field_ip'
            if not is_valid_ip(ip):
                return 'invalid_ip'

            try:
                device_data = self.parent.connect_to_device_IP(ip)
                device_data['address'] = str(ip)
            except Connect_err:
                self.show_connect_err_label()

            return device_data
        else:
            try:
                slave_id = int(self.slave_id_line_edit.text())
            except:
                return 'empty_field_slave_id'
            for port in self.com_ports:
                if port.description == selected_item:
                    selected_port = port.device
                    try:
                        device_data = self.parent.connect_to_device_COM(selected_port, slave_id)
                        device_data['address'] = str(slave_id) + ' (' + str(selected_port) + ')'
                    except Connect_err:
                        self.show_connect_err_label()

                    break

            return device_data


