#!/usr/bin/env python3

from typing import *
import os
import sys
import socket
import select
import argparse

from .. import argparsing

class StdinReader:
    def __init__(self) -> None:
        self.stream: BinaryIO = None

        if sys.stdin.buffer.isatty():
            self.stream = sys.stdin.buffer
            self.read = self.read_interactive
        else:
            # Change stdin to unbuffered BinaryIO, don't wait for "\n"
            sys.stdin = os.fdopen(sys.stdin.fileno(), "rb", buffering = 0)
            self.stream = sys.stdin
            self.read = self.read_noninteractive

    def read(self, count: int):
        # set in __init__
        raise NotImplementedError

    def read_interactive(self, count: int):
        return self.stream.readline()

    def read_noninteractive(self, count: int):
        return self.stream.read(count)

def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "Connect to a socket and read+write data with it. sends stdin to the socket and recvs the socket to stdout"
    )

    argparsing.add_socket_address_subparsers(parser)

    args = parser.parse_args()

    return args

def main():
    args = get_cli_args()

    socket_af = argparsing.af_const_from_args(args)
    socket_address = argparsing.socket_address_from_args(args)

    s = socket.socket(family = socket_af)
    s.connect(socket_address)

    eof_stdin: bool = False
    eof_s: bool = False

    fd_stdin = sys.stdin.buffer.fileno()
    fd_s = s.fileno()

    stdin_reader = StdinReader()

    poller = select.poll()
    poller.register(fd_stdin, select.POLLIN)
    poller.register(fd_s, select.POLLIN)

    while any([not eof_stdin, not eof_s]):
        for fd, revents in poller.poll():
            if fd == fd_stdin:
                if revents & select.POLLERR:
                    print("poll(): POLLERR from stdin, exiting", file = sys.stderr)
                    raise SystemExit(1)

                read = stdin_reader.read(4096)

                if read:
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

if __name__ == "__main__":
    main()
