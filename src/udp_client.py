import socket


class UdpClient:
    def __init__(self, port: int):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", port))

    def __del__(self):
        self.sock.close()

    def send(self, packet: bytes, remote_addr: tuple[str, int]) -> bool:
        try:
            result = self.sock.sendto(packet, remote_addr)
            return result > 0
        except Exception as e:
            print(e)
            return False

    def broadcast(self, packet: bytes, remote_port: int) -> bool:
        try:
            result = self.sock.sendto(packet, ("<broadcast>", remote_port))
            return result > 0
        except Exception as e:
            print(e)
            return False

    def recv(self, bufsize: int = 1024) -> tuple[bytes, tuple[str, int]]:
        try:
            return self.sock.recvfrom(bufsize)
        except Exception as e:
            print(e)
            return b"", ("", 0)
