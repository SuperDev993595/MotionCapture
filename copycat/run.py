import argparse
import importlib.metadata as metadata
from argparse import Namespace

__version__ = metadata.version(__package__ or __name__)

from copycat.models.log_level import LogLevel
from copycat.shared.utils.logger import Logger
from copycat.tool.tool import Tool


class Copycat:
    def __init__(self):
        self.logger = Logger()
        self.args = self.parse_args()
        self.set_verbosity()

    def run(self):
        self.check_args()
        self.logger.info(f"Running...")
        self.logger.debug(self.args)

        tool = Tool(theme=self.args.theme, speed=self.args.speed)
        if self.args.gui:
            self.logger.info("Running GUI...")
            tool.show()
        elif self.args.reply:
            macro_name = self.args.reply
            self.logger.info(f"Replying to macro: {macro_name}")
            tool.play_macro(macro_name)

        self.logger.info("Created by ZappaBoy")

    @staticmethod
    def parse_args() -> Namespace:
        parser = argparse.ArgumentParser(
            description="Copycat is a tool that record and replay mouse and keyboard macro.")
        parser.add_argument('--verbose', '-v', action='count', default=1,
                            help='Increase verbosity. Use more than once to increase verbosity level (e.g. -vvv).')
        parser.add_argument('--debug', action='store_true', default=False,
                            help='Enable debug mode.')
        parser.add_argument('--quiet', '-q', action=argparse.BooleanOptionalAction, default=False,
                            required=False, help='Do not print any output/log')
        parser.add_argument('--version', '-V', action='version', version=f'%(prog)s {__version__}',
                            help='Show version and exit.')
        parser.add_argument('--gui', action='store_true', default=False,
                            help='Run the tool in GUI mode.')
        parser.add_argument('--theme', '-t', action='store', default="equilux", type=str,
                            help='Set the "ttkthemes" GUI theme. (Default: equilux)')
        parser.add_argument('--speed', '-s', action='store', default=1.0, type=float,
                            help='Speed of the macro playback. (Default: 1.0)')
        parser.add_argument('--reply', '-r', action='store', type=str,
                            help='Define macro name to reply.')
        return parser.parse_args()

    def check_args(self) -> None:
        error_message = ""
        # Add arguments checks here
        if error_message != "":
            self.logger.error(error_message)
            exit(1)

    def set_verbosity(self) -> None:
        if self.args.quiet:
            verbosity_level = LogLevel.DISABLED
        else:
            if self.args.debug or self.args.verbose > LogLevel.DEBUG.get_value():
                verbosity_level = LogLevel.DEBUG
            else:
                verbosity_level = self.args.verbose
        self.logger.set_log_level(verbosity_level)
