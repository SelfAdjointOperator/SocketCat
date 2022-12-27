#!/usr/bin/env python3

from typing import *
import sys
import socket
import select
import argparse
from pathlib import Path

def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "Connect to a Unix socket and read+write data with it. sends stdin to the socket and recvs the socket to stdout"
    )

    parser.add_argument("socket_path",
        metavar = "SOCKET-PATH",
        help = "Path to Unix socket",
        type = Path
    )

    args = parser.parse_args()

    return args

def stdin_reader_interactive(count: int):
    return sys.stdin.readline().encode()

def stdin_reader_noninteractive(count: int):
    return sys.stdin.buffer.read(count)

def get_stdin_reader() -> Callable[[int], bytes]:
    if sys.stdin.buffer.isatty():
        return stdin_reader_interactive
    else:
        return stdin_reader_noninteractive

def main():
    args = get_cli_args()

    socket_path: Path = getattr(args, "socket_path")

    s = socket.socket(family = socket.AF_UNIX)
    s.connect(f"{socket_path}")

    eof_stdin: bool = False
    eof_s: bool = False

    fd_stdin = sys.stdin.buffer.fileno()
    fd_s = s.fileno()

    stdin_reader = get_stdin_reader()

    poller = select.poll()
    poller.register(fd_stdin, select.POLLIN)
    poller.register(fd_s, select.POLLIN)

    while any([not eof_stdin, not eof_s]):
        for fd, revents in poller.poll():
            if fd == fd_stdin:
                if revents & select.POLLERR:
                    print("poll(): POLLERR from stdin, exiting", file = sys.stderr)
                    raise SystemExit(1)

                read = stdin_reader(4096)

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
