from typing import *
import os
import socket
import socketserver

from . import argparse32c705 as argparse
from . import argparsing

def stream_forwarder(fd_in: int, fd_out: int, chunk_size: int = 4096) -> None:
    "Perform chunked reads from `fd_in` until EOF and write the data to `fd_out`"
    while read := os.read(fd_in, chunk_size):
        os.write(fd_out, read) # TODO is write guaranteed to write all of `read`?

class ForkingUnixStreamServer(socketserver.ForkingMixIn, socketserver.UnixStreamServer):
    # this should really be part of socketserver no?
    pass

def run_socket_handler_from_args(args: argparse.Namespace, handler: Callable[[socket.socket], None]):
    if args.bind_or_connect == "bind":
        run_socket_handler_from_args_server(args.bind, handler)
    elif args.bind_or_connect == "connect":
        run_socket_handler_from_args_client(args.connect, handler)

def run_socket_handler_from_args_client(args: argparse.Namespace, handler: Callable[[socket.socket], None]) -> None:
    socket_af = argparsing.af_const_from_args(args)
    socket_address = argparsing.socket_address_from_args(args)

    sock = socket.socket(family = socket_af)
    sock.connect(socket_address)

    handler(sock)

def run_socket_handler_from_args_server(args: argparse.Namespace, handler: Callable[[socket.socket], None]) -> None:
    class RequestHandler(socketserver.StreamRequestHandler):
        def handle(self) -> None:
            handler(self.request)

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
