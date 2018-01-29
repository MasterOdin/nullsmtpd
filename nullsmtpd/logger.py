"""
Logger module for NullSMTP
"""
import logging
import os
import sys

LOGGER_NAME = 'nullsmtpd'


# pylint: disable=too-few-public-methods
class InfoFilter(logging.Filter):
    """
    Filter for logging which only allows DEBUG and INFO to go through. We use this
    to allow us to best split the logging where WARN and above are on sys.stderr and
    INFO and below are on sys.stdout.
    """
    def filter(self, record):
        return record.levelno in (logging.DEBUG, logging.INFO)


def configure_logging(mail_dir, console_logging=False):
    """
    :param mail_dir:
    :param console_logging:
    :return:
    """

    logger = get_logger()
    logger.setLevel(logging.DEBUG)

    file_logger = logging.FileHandler(os.path.join(mail_dir, 'nullsmtpd.log'))
    file_logger.setLevel(logging.ERROR)

    info_format = "%(asctime)s [%(levelname)-7.7s] %(message)s"

    file_logger.setLevel(logging.INFO)
    log_format = logging.Formatter(fmt=info_format, datefmt="%Y-%m-%d %H:%M:%S")
    file_logger.setFormatter(log_format)

    if console_logging:
        stdout = logging.StreamHandler(sys.stdout)
        stdout.addFilter(InfoFilter())
        stdout.setLevel(logging.INFO)

        stderr = logging.StreamHandler(sys.stderr)
        stderr.setLevel(logging.WARNING)

        stdout.setFormatter(log_format)
        stderr.setFormatter(log_format)

        logger.addHandler(stderr)
        logger.addHandler(stdout)

    return logger


def get_logger():
    """
    Shortcut method to get the logger for our application
    :return:
    """
    return logging.getLogger(LOGGER_NAME)
