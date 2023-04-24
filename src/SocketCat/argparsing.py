from typing import *
import socket
from pathlib import Path

from . import argparse32c705 as argparse
from . import socketserverd94b3a6 as socketserver

def add_cli_args_af(parser: argparse.ArgumentParser, add_bind_options: bool = False) -> None:
    parser_af = parser.add_subparsers(
        title = "address",
        dest = "af",
        required = True,
        description = "which address family (AF) to create the socket in"
    )

    parser_af_unix = parser_af.add_parser("unix", help = "AF_UNIX", subspace_name = "unix")
    parser_af_unix.add_argument("path",
        metavar = "SOCKET-PATH",
        help = "path to Unix socket",
        type = Path
    )
    if add_bind_options:
        parser_af_unix.add_argument("--chmod",
            metavar = "MODE",
            dest = "chmod",
            help = "Call os.umask(0o777) before calling socket.bind(), restore umask, and call os.chmod(MODE) on the socket. MODE is in octal, eg --chmod 777 for a public socket",
            type = octal
        )

    parser_af_inet = parser_af.add_parser("inet", help = "AF_INET", subspace_name = "inet")
    parser_af_inet.add_argument("ip",
        metavar = "IP",
        help = "IP address"
    )
    parser_af_inet.add_argument("port",
        metavar = "PORT",
        help = "port number",
        type = int
    )

def octal(s: str) -> int:
    """Used instead of a lambda for argparse 'invalid octal value' message"""
    return int(s, 8)

def add_cli_args_bind(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--fork", "-f",
        help = "Have the server call os.fork() after calling socket.listen()",
        action = "store_true"
    )

    add_cli_args_af(parser, add_bind_options = True)

def add_cli_args_connect(parser: argparse.ArgumentParser) -> None:
    add_cli_args_af(parser, add_bind_options = False)

def add_cli_args_bind_or_connect(parser: argparse.ArgumentParser) -> None:
    parser_bind_or_connect = parser.add_subparsers(
        title = "connection",
        dest = "bind_or_connect",
        required = True,
        description = "run a server or connect as a client"
    )

    add_cli_args_bind(parser_bind_or_connect.add_parser("bind", help = "server", subspace_name = "bind"))
    add_cli_args_connect(parser_bind_or_connect.add_parser("connect", help = "client", subspace_name = "connect"))

def af_const_from_args(args: argparse.Namespace):
    return {
        "unix": socket.AF_UNIX,
        "inet": socket.AF_INET,
    }[args.af]

def socket_address_from_args(args: argparse.Namespace):
    if args.af == "unix":
        return f"{args.unix.path}"
    elif args.af == "inet":
        return (args.inet.ip, args.inet.port)
    else:
        raise NotImplementedError

def socketserver_class_from_args(args: argparse.Namespace) -> socketserver.BaseServer:
    return {
        "unix": socketserver.ForkingUnixStreamServer,
        "inet": socketserver.ForkingTCPServer,
    }[args.af]
