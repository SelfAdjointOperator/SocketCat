"""Tools for connecting to sockets and `send`ing and `recv`ing with them"""

from typing import *

from . import argparse32c705 as argparse
from . import cat
from . import echo
from . import send
from . import write

def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = __doc__
    )

    parser_tool = parser.add_subparsers(
        title = "tool",
        dest = "tool",
        required = True
    )

    cat.add_cli_args(  parser_tool.add_parser("cat",   description = cat.__doc__,   help = cat.__doc__,   subspace_name = "cat"  ))
    echo.add_cli_args( parser_tool.add_parser("echo",  description = echo.__doc__,  help = echo.__doc__,  subspace_name = "echo" ))
    send.add_cli_args( parser_tool.add_parser("send",  description = send.__doc__,  help = send.__doc__,  subspace_name = "send" ))
    write.add_cli_args(parser_tool.add_parser("write", description = write.__doc__, help = write.__doc__, subspace_name = "write"))

    args = parser.parse_args()

    return args

def main() -> None:
    args = get_cli_args()

    {
        "cat": cat.main,
        "echo": echo.main,
        "send": send.main,
        "write": write.main,
    }[args.tool](getattr(args, args.tool))

if __name__ == "__main__":
    main()
