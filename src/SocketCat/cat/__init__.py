"""Connect to a socket and recv data from it to stdout"""

from typing import *
import sys
import socket

from .. import argparse32c705 as argparse
from .. import argparsing

def add_cli_args(parser: argparse.ArgumentParser) -> None:
    argparsing.add_cli_args_af(parser)

def main(args: argparse.Namespace) -> None:
    socket_af = argparsing.af_const_from_args(args)
    socket_address = argparsing.socket_address_from_args(args)

    s = socket.socket(family = socket_af)
    s.connect(socket_address)

    while recved := s.recv(4096):
        sys.stdout.buffer.write(recved)
