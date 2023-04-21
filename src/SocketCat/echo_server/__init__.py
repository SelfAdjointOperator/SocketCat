"""Simple echo server. send()s back what it recv()s"""

from typing import *
import os
import socket
import socketserver

from .. import argparse32c705 as argparse
from .. import argparsing

class EchoRequestHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        while recved := os.read(self.rfile.fileno(), 4096):
            self.wfile.write(recved)

def add_cli_args(parser: argparse.ArgumentParser) -> None:
    argparsing.add_cli_args_bind(parser)

def main(args: argparse.Namespace) -> None:
    socket_af = argparsing.af_const_from_args(args)
    socket_address = argparsing.socket_address_from_args(args)
    fork: bool = args.fork

    if socket_af == socket.AF_UNIX:
        chmod: Optional[int] = args.unix.chmod
        try:
            os.unlink(socket_address)
        except FileNotFoundError:
            pass

    socketserver_class = argparsing.socketserver_class_from_args(args)

    with socketserver_class(socket_address, EchoRequestHandler, bind_and_activate = False) as server:
        if socket_af == socket.AF_UNIX and chmod is not None:
            umask_old = os.umask(0o777)

        server.server_bind()

        if socket_af == socket.AF_UNIX and chmod is not None:
            os.umask(umask_old)
            os.chmod(socket_address, chmod)

        server.server_activate()

        if fork and os.fork():
            # parent exits
            os._exit(0)

        try:
            server.serve_forever()
        except KeyboardInterrupt as e:
            print(f"{e.__class__.__name__}: shutting down")
