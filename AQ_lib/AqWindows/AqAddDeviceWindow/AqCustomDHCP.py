from enum import Enum, IntEnum

from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QUdpSocket, QHostAddress, QAbstractSocket
import struct
import socket


class DhcpTYPE(IntEnum):
    DISCOVER = 1
    REQUEST = 3


class State(Enum):
    IDLE = 0
    WAIT_REQUEST = 1
    DONE = 2


class DeviceDHCPButtonListener(QObject):
    deviceIpRequest = Signal()  # (bytes, object, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.sock = QUdpSocket(self)

        ok = self.sock.bind(
            QHostAddress.AnyIPv4,
            50067,
            QUdpSocket.ShareAddress | QUdpSocket.ReuseAddressHint
        )

        if not ok:
            raise RuntimeError("Cant connect with port 50067")

        self.sock.readyRead.connect(self.on_ready_read)

        self.state = State.IDLE

        # Active DHCP context
        self.active_request = {
            "mac": None,
            "xid": None,
            "ip": None,
        }

    def on_ready_read(self):
        while self.sock.hasPendingDatagrams():
            d = self.sock.receiveDatagram()
            data = bytes(d.data())

            self.process_packet(data)

    def get_dhcp_message_type(self, data: bytes) -> DhcpTYPE | None:
        i = 240  # после magic cookie
        while i < len(data):
            opt = data[i]
            if opt == 0xff:
                return None
            if opt == 0x35:  # Message Type
                return data[i + 2]
            length = data[i + 1]
            i += 2 + length
        return None

    def process_packet(self, data: bytes):
        if len(data) < 240:
            return

        if data[236:240] != b'\x63\x82\x53\x63':  # MAGIC FILTER DHCP REQUEST
            return

        msg_type: DhcpTYPE = self.get_dhcp_message_type(data)
        if msg_type is None:
            return

        xid = int.from_bytes(data[4:8], "big")
        mac = data[28:34]

        # ---------- DISCOVER ----------
        if msg_type == DhcpTYPE.DISCOVER and self.state == State.IDLE:
            self.state = State.WAIT_REQUEST

            self.active_request["mac"] = mac
            self.active_request["xid"] = xid

            # уведомляем UI: найден прибор
            self.deviceIpRequest.emit()  # (mac, xid, "")

            return

        # ---------- REQUEST ----------
        if msg_type == DhcpTYPE.REQUEST and self.state == State.WAIT_REQUEST:
            if mac != self.active_request["mac"]:
                return
            if xid != self.active_request["xid"]:
                return

            ip = self.active_request["ip"]
            if not ip:
                return  # UI ещё не дал IP

            self.send_ack(xid, mac, ip)
            self.state = "DONE"

            return

    def set_ip_and_send_offer(self, ip: str):
        if self.state != State.WAIT_REQUEST:
            return

        self.active_request["ip"] = ip

        data = build_dhcp_offer(
            self.active_request["xid"],
            self.active_request["mac"],
            self.active_request["ip"]
        )

        sent = self.sock.writeDatagram(
            data,
            QHostAddress.Broadcast,
            50068
        )

        if sent == -1:
            print("Send offer error:", self.sock.errorString())
        else:
            print("Sent offer bytes:", sent)

    def send_ack(self, xid: bytes, mac: bytes, ip: str):
        data = build_dhcp_ack(xid, mac, ip)

        sent = self.sock.writeDatagram(
            data,
            QHostAddress.Broadcast,
            50068
        )

        if sent == -1:
            print("Send ack error:", self.sock.errorString())
        else:
            print("Sent ack bytes:", sent)

    def stop(self):
        if self.sock:
            self.sock.close()
            self.sock = None


def build_dhcp_offer(xid: bytes, mac: bytes, ip: str) -> bytes:
    pkt = bytearray(240)

    pkt[0] = 2      # BOOTREPLY
    pkt[1] = 1      # Ethernet
    pkt[2] = 6
    pkt[3] = 0

    struct.pack_into("!I", pkt, 4, xid)
    struct.pack_into("!H", pkt, 10, 0x8000)  # broadcast flag

    pkt[16:20] = socket.inet_aton(ip)  # yiaddr
    pkt[28:34] = mac

    pkt[236:240] = b"\x63\x82\x53\x63"

    opts = bytearray()

    # DHCP Message Type = OFFER
    opts += b"\x35\x01\x02"

    # Server Identifier
    opts += b"\x36\x04" + socket.inet_aton("192.168.0.1")

    # Subnet Mask
    opts += b"\x01\x04" + socket.inet_aton("255.255.255.0")

    # Router
    opts += b"\x03\x04" + socket.inet_aton("192.168.0.1")

    # Lease Time (опционально, но желательно)
    opts += b"\x33\x04\x00\x01\x51\x80"  # ~1 день

    opts += b"\xff"

    return bytes(pkt + opts)


def build_dhcp_ack(xid: bytes, mac: bytes, ip: str) -> bytes:
    pkt = bytearray(240)  # BOOTP + cookie

    # BOOTP fixed header
    pkt[0] = 2          # op = BOOTREPLY
    pkt[1] = 1          # htype = Ethernet
    pkt[2] = 6          # hlen
    pkt[3] = 0          # hops

    # вставляем XID напрямую
    # pkt[4:8] = xid

    struct.pack_into("!I", pkt, 4, xid)     # xid
    struct.pack_into("!H", pkt, 10, 0x8000) # flags (broadcast)

    pkt[16:20] = socket.inet_aton(ip)       # yiaddr
    pkt[28:34] = mac                        # chaddr

    # Magic cookie
    pkt[236:240] = b"\x63\x82\x53\x63"

    # DHCP options
    opts = bytearray()

    # DHCP Message Type = ACK
    opts += b"\x35\x01\x05"

    # Server Identifier (любой, но логично IP компа)
    opts += b"\x36\x04" + socket.inet_aton("192.168.0.1")

    # Subnet mask
    opts += b"\x01\x04" + socket.inet_aton("255.255.255.0")

    # Router (gateway)
    opts += b"\x03\x04" + socket.inet_aton("192.168.0.1")

    # Lease Time (опционально, но желательно)
    opts += b"\x33\x04\x00\x01\x51\x80"  # ~1 день

    # END
    opts += b"\xff"

    return bytes(pkt + opts)



