"""
This module creates a basic cli and runs program.
"""

import argparse
import importlib.metadata


def create_argument_parser() -> argparse.ArgumentParser:
    """Creates an argument parser for the program"""
    parser = argparse.ArgumentParser(
        prog="searchmate",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            "A modular and versatile desktop assistant that searches for apps, "
            "performs basic math and makes chatting with GPT easier."
        ),
    )

    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        default=argparse.SUPPRESS,
        help="prints installed SearchMate version",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=argparse.SUPPRESS,
        help="verbose mode (prints more logs)",
    )

    return parser


def print_version() -> None:
    """Prints installed SearchMate version"""
    version = importlib.metadata.version(__package__)
    print(f"Current SearchMate version: {version}")


def main() -> None:
    """Runs SearchMate as a Python application"""
    parser = create_argument_parser()
    cmdline_arguments = parser.parse_args()

    if hasattr(cmdline_arguments, "version"):
        print_version()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
