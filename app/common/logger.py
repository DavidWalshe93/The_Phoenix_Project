"""
Author:     David Walshe
Date:       13 May 2021
"""

import logging
import logging.config

import yaml
from colorama import Fore

logger = logging.getLogger(__name__)


def init_logger(config_file: str) -> None:
    """
    Initialised the logger from a configuration file.

    :param config_file: The path to the config file to initialise the logger with.
    """
    with open(config_file, "r") as fh:
        config = yaml.safe_load(fh.read())

        logging.config.dictConfig(config)


class ColorFormatter(logging.Formatter):
    """Adds colored output to logger."""

    # log output format.
    format = "[USER-SERVICE] - %(levelname)-8s - %(message)-8s"

    FORMATS = {
        logging.DEBUG: Fore.CYAN + format + Fore.RESET,
        logging.INFO: format,
        logging.WARNING: Fore.YELLOW + format + Fore.RESET,
        logging.ERROR: Fore.RED + format + Fore.RESET,
    }

    def format(self, record):
        """
        Formats the log record before returning it to the caller.
        :param record: The record to colorize.
        :return: The colur formatted record.
        """
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format)

        return formatter.format(record)
