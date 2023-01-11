from typing import *
import socketserver

class ForkingUnixStreamServer(socketserver.ForkingMixIn, socketserver.UnixStreamServer):
    # this should really be part of socketserver no?
    pass
