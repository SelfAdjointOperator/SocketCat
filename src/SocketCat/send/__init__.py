"""Connect to a socket and send data to it from stdin"""

import sys
import socket

from .. import common

class Tool(common.Tool):
    @classmethod
    def handler(cls, sock: socket.socket) -> None:
        common.stream_forwarder(sys.stdin.buffer.fileno(), sock.fileno())
