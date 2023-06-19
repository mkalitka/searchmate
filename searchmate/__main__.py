"""This module creates a basic cli and runs program."""

import os
import argparse
import importlib.metadata
import logging

from searchmate.gui import gui


version = importlib.metadata.version(__package__)


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Creates an argument parser for the program

    Returns:
        argparse.ArgumentParser: An argument parser for CLI.
    """
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

    print(f"Current SearchMate version: {version}")


def main() -> None:
    """Runs SearchMate as a Python application"""

    parser = create_argument_parser()
    cmdline_arguments = parser.parse_args()

    if hasattr(cmdline_arguments, "version"):
        print_version()
    elif hasattr(cmdline_arguments, "help"):
        parser.print_help()
    else:
        if hasattr(cmdline_arguments, "verbose"):
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        logging.basicConfig(
            level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
        )

        logging.info("Main - Starting Searchmate version %s", version)

        os.environ["QT_QPA_PLATFORM"] = "xcb"
        gui.run()

        logging.info("Main - Stopping SearchMate.")


if __name__ == "__main__":
    main()
