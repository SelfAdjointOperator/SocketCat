#!/usr/bin/env python3

from typing import *
import sys
import socket
import argparse
from pathlib import Path

def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "Connect to a Unix socket and send data to it from stdin"
    )

    parser.add_argument("socket_path",
        metavar = "SOCKET-PATH",
        help = "Path to Unix socket",
        type = Path
    )

    args = parser.parse_args()

    return args

def main():
    args = get_cli_args()

    socket_path: Path = getattr(args, "socket_path")

    s = socket.socket(family = socket.AF_UNIX)
    s.connect(f"{socket_path}")

    for line in sys.stdin.buffer:
        s.sendall(line)

if __name__ == "__main__":
    main()
