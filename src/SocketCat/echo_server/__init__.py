from typing import *
import os
import socket
import socketserver
import argparse

from .. import argparsing

class EchoRequestHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        while recved := os.read(self.rfile.fileno(), 4096):
            self.wfile.write(recved)

def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "Simple echo server. send()s back what it recv()s"
    )

    argparsing.add_server_arguments(parser)

    args = parser.parse_args()

    return args

def main():
    args = get_cli_args()

    socket_af = argparsing.af_const_from_args(args)
    socket_address = argparsing.socket_address_from_args(args)
    fork: bool = getattr(args, "fork")

    if socket_af == socket.AF_UNIX:
        chmod: Optional[int] = getattr(args, "address_family_unix_chmod")
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

if __name__ == "__main__":
    main()
