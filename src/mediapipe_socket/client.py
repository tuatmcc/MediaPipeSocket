from pythonosc.osc_message import OscMessage
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import UDPClient

from args import HOST_ADDRESS


class Client:
    """
    OSC Client for sending pose data to the Unity side.
    """

    def __init__(self, addr: str = HOST_ADDRESS, port: int = 8080) -> None:
        self.address: str = "/pose"
        self.builder: OscMessageBuilder = OscMessageBuilder(self.address)
        self.client: UDPClient = UDPClient(addr, port)

    def Send(self, data: list[list[float]]) -> None:
        self.builder._args = []
        self.builder.add_arg(data)
        msg: OscMessage = self.builder.build()
        self.client.send(msg)


def CreateClient(addr: str = HOST_ADDRESS, port: int = 8080) -> Client:
    """
    Create a new OSC client.
    """
    return Client(addr, port)
