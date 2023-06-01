from typing import Optional
import os
import socket

from . import argparse32c7050 as argparse
from . import socketserverd94b3a6 as socketserver
from . import argparsing

def writeall(fd: int, src: bytes) -> int:
    # this must be a do-while loop, not just a while loop
    # for correct error behaviour in the case len(src) == 0
    # man 2 write (Linux man-pages 6.04): "If count is zero and fd refers
    # to a regular file, then write() may return a failure status if
    # one of the errors below is detected"
    n_written_total = 0

    n_written = os.write(fd, src)
    n_written_total += n_written
    src = src[n_written:]
    while src:
        n_written = os.write(fd, src)
        n_written_total += n_written
        src = src[n_written:]

    return n_written_total

def stream_forwarder(fd_in: int, fd_out: int, chunk_size: int = 4096) -> None:
    "Perform chunked reads from `fd_in` until EOF and write the data to `fd_out`"
    while read := os.read(fd_in, chunk_size):
        writeall(fd_out, read)

class Tool:
    @classmethod
    def add_cli_args(cls, parser: argparse.ArgumentParser) -> None:
        argparsing.add_cli_args_bind_or_connect(parser)

    @classmethod
    def handler(cls, sock: socket.socket) -> None:
        raise NotImplementedError

    @classmethod
    def main(cls, args: argparse.Namespace) -> None:
        if args.bind_or_connect == "bind":
            cls._main_server(args.bind)
        elif args.bind_or_connect == "connect":
            cls._main_client(args.connect)

    @classmethod
    def _main_server(cls, args: argparse.Namespace) -> None:
        class RequestHandler(socketserver.StreamRequestHandler):
            def handle(self) -> None:
                cls.handler(self.request)

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

        with socketserver_class(socket_address, RequestHandler, bind_and_activate = False) as server:
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

    @classmethod
    def _main_client(cls, args: argparse.Namespace) -> None:
        socket_af = argparsing.af_const_from_args(args)
        socket_address = argparsing.socket_address_from_args(args)

        sock = socket.socket(family = socket_af)
        sock.connect(socket_address)

        cls.handler(sock)
