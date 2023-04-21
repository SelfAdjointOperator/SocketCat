"""Simple echo server. send()s back what it recv()s"""

from typing import *
import os
import socket

from .. import argparse32c705 as argparse
from .. import argparsing
from .. import common

def handler(sock: socket.socket) -> None:
    while recved := os.read(sock.fileno(), 4096):
        os.write(sock.fileno(), recved)

def add_cli_args(parser: argparse.ArgumentParser) -> None:
    argparsing.add_cli_args_bind_or_connect(parser)

def main(args: argparse.Namespace) -> None:
    common.run_socket_handler_from_args(args, handler)
