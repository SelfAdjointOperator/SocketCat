"""Connect to a socket and recv data from it to stdout"""

import sys
import socket

from .. import common

class Tool(common.Tool):
    @classmethod
    def handler(cls, sock: socket.socket) -> None:
        common.stream_forwarder(sock.fileno(), sys.stdout.buffer.fileno())
