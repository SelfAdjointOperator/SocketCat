"""Simple echo server. send()s back what it recv()s"""

import socket

from .. import common

class Tool(common.Tool):
    @classmethod
    def handler(cls, sock: socket.socket) -> None:
        common.stream_forwarder(sock.fileno(), sock.fileno())
