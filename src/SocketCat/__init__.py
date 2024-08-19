"""Tools for connecting to sockets and `send`ing and `recv`ing with them"""

__version__ = "1.0.1"

from . import argparse32c7050 as argparse
from . import cat
from . import echo
from . import send
from . import write

tool_name_to_module = {
    "cat":   cat,
    "echo":  echo,
    "send":  send,
    "write": write,
}

def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = __doc__
    )

    parser_tool = parser.add_subparsers(
        title = "tool",
        dest = "tool",
        required = True
    )

    for tool_name, tool_module in tool_name_to_module.items():
        tool_module.Tool.add_cli_args(parser_tool.add_parser(
            tool_name,
            description = tool_module.__doc__,
            help = tool_module.__doc__,
            subspace_name = tool_name
        ))

    args = parser.parse_args()

    return args

def main() -> None:
    args = get_cli_args()

    tool_name_to_module[args.tool].Tool.main(getattr(args, args.tool))

if __name__ == "__main__":
    main()
