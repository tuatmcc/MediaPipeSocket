import socket

HOST_ADDRESS: str = "192.168.0.254"


class UDPClient:
    def __init__(self, host: str, port: int):
        self.address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __del__(self):
        self.sock.close()

    def send(self, packet: bytes) -> bool:
        try:
            result = self.sock.sendto(packet, self.address)
            return bool(result)
        except Exception as e:
            print(e)
            return False
