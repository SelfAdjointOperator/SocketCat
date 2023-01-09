#!/usr/bin/env python3

from typing import *
import os
import sys
import socket
import argparse

from .. import argparsing

def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "Connect to a socket and send data to it from stdin"
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

    while line := os.read(sys.stdin.buffer.fileno(), 4096):
        s.sendall(line)

if __name__ == "__main__":
    main()
