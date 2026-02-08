from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QUdpSocket, QHostAddress


class DeviceDHCPButtonListener(QObject):
    deviceIpRequest = Signal(bytes, int, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.sock = QUdpSocket(self)

        ok = self.sock.bind(
            QHostAddress.Any,
            50067,
            QUdpSocket.ShareAddress | QUdpSocket.ReuseAddressHint
        )

        if not ok:
            raise RuntimeError("Cant connect with port 50067")

        self.sock.readyRead.connect(self.on_ready_read)

        self.busy = False
        self.active_request = None  # (mac, xid)

    def on_ready_read(self):
        while self.sock.hasPendingDatagrams():
            d = self.sock.receiveDatagram()
            data = d.data()

            self.process_packet(data)

    def process_packet(self, data: bytes):
        # If busy - ignore other packets
        if self.busy:
            return

        if len(data) < 240:
            return

        if data[236:240] != b'\x63\x82\x53\x63': #MAGIC FILTER DHCP REQUEST
            return

        xid = int.from_bytes(data[4:8], byteorder="big")

        mac = data[28:34]

        self.busy = True
        self.active_request = (mac, xid)

        self.deviceIpRequest.emit(mac, xid, '') #empty string - for future


