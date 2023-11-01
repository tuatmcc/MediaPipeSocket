from pythonosc.osc_message import OscMessage
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import UDPClient

HOST_ADDRESS: str = "192.168.0.254"


class Client:
    def __init__(self, addr: str = HOST_ADDRESS, port: int = 8080) -> None:
        self.address: str = "/pose"
        self.client: UDPClient = UDPClient(addr, port)

    def Send(self, data: list[list[float]]) -> None:
        builder: OscMessageBuilder = OscMessageBuilder(self.address)
        builder.add_arg(data)
        msg: OscMessage = builder.build()
        self.client.send(msg)
