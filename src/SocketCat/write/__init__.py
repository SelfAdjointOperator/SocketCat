"""Connect to a socket and read+write data with it. sends stdin to the socket and recvs the socket to stdout"""

from typing import *
import os
import sys
import socket
import select

from .. import argparse32c705 as argparse
from .. import argparsing

def add_cli_args(parser: argparse.ArgumentParser) -> None:
    argparsing.add_cli_args_af(parser)

def main(args: argparse.Namespace) -> None:
    socket_af = argparsing.af_const_from_args(args)
    socket_address = argparsing.socket_address_from_args(args)

    s = socket.socket(family = socket_af)
    s.connect(socket_address)

    eof_stdin: bool = False
    eof_s: bool = False

    fd_stdin = sys.stdin.buffer.fileno()
    fd_s = s.fileno()

    poller = select.poll()
    poller.register(fd_stdin, select.POLLIN)
    poller.register(fd_s, select.POLLIN)

    while any([not eof_stdin, not eof_s]):
        for fd, revents in poller.poll():
            if fd == fd_stdin:
                if revents & select.POLLERR:
                    print("poll(): POLLERR from stdin, exiting", file = sys.stderr)
                    raise SystemExit(1)

                if read := os.read(sys.stdin.buffer.fileno(), 4096):
                    s.sendall(read)
                else:
                    print("read(): 0 from stdin, calling shutdown(SHUT_WR)", file = sys.stderr)
                    eof_stdin = True
                    poller.unregister(fd_stdin)
                    s.shutdown(socket.SHUT_WR)

            elif fd == fd_s:
                if revents & select.POLLERR:
                    print("poll(): POLLERR from socket, exiting", file = sys.stderr)
                    raise SystemExit(1)

                recved = s.recv(4096)

                if recved:
                    sys.stdout.buffer.write(recved)
                    sys.stdout.buffer.flush()
                else:
                    print("recv(): 0 from socket; remote end called shutdown(SHUT_WR)", file = sys.stderr)
                    eof_s = True
                    poller.unregister(fd_s)
