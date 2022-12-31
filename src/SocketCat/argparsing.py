from typing import *
import socket
import argparse
from pathlib import Path

def add_socket_address_subparsers(parser: argparse.ArgumentParser):
    parser_address_family = parser.add_subparsers(title = "address", dest = "address_family", required = True,
        description = "which address family (AF) to create the socket in"
    )

    parser_address_family_unix = parser_address_family.add_parser("unix", help = "AF_UNIX")
    parser_address_family_unix.add_argument("address_family_unix_path",
        metavar = "SOCKET-PATH",
        help = "path to Unix socket",
        type = Path
    )

    parser_address_family_inet = parser_address_family.add_parser("inet", help = "AF_INET")
    parser_address_family_inet.add_argument("address_family_inet_ip",
        metavar = "IP",
        help = "IP address"
    )
    parser_address_family_inet.add_argument("address_family_inet_port",
        metavar = "PORT",
        help = "port number",
        type = int
    )

def _socket_address_from_args_unix(args: argparse.Namespace):
    socket_path: Path = getattr(args, "address_family_unix_path")

    return f"{socket_path}"

def _socket_address_from_args_inet(args: argparse.Namespace):
    socket_ip: str = getattr(args, "address_family_inet_ip")
    socket_port: int = getattr(args, "address_family_inet_port")

    return (socket_ip, socket_port)

_af_str_to_af_const = {
    "unix": socket.AF_UNIX,
    "inet": socket.AF_INET,
}

_af_str_to_af_address_generator = {
    "unix": _socket_address_from_args_unix,
    "inet": _socket_address_from_args_inet,
}

def af_const_from_args(args: argparse.Namespace):
    af: str = getattr(args, "address_family")

    return _af_str_to_af_const[af]

def socket_address_from_args(args: argparse.Namespace):
    af: str = getattr(args, "address_family")

    return _af_str_to_af_address_generator[af](args)
