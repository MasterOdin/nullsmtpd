#!/usr/bin/env python3
"""
NullSMTP module that allows to run a mock email server that just logs all incoming emails to a file
instead of actually trying to send them. Helps for developing applications that utilize email,
without spamming customers' emails and not having overhead from some GUI program.
"""
import argparse
import os
import time

from aiosmtpd.controller import Controller

from .logger import configure_logging

__author__ = 'Matthew Peveler'
__version__ = '0.4.0'
__license__ = 'Unlicense (Public Domain)'

NULLSMTPD_DIRECTORY = os.path.join(os.path.expanduser("~"), ".nullsmtpd")


class NullSMTPDHandler(object):
    def __init__(self, logger, mail_dir, output_messages):
        self.logger = logger
        if mail_dir is None or not isinstance(mail_dir, str):
            msg = "Invalid mail_dir variable: {}".format(mail_dir)
            self.logger.error(msg)
            raise SystemExit(msg)
        elif not os.path.isdir(mail_dir):
            try:
                os.mkdir(mail_dir)
            except IOError as io_error:
                self.logger.error(str(io_error))
                raise
        self.mail_dir = mail_dir
        self.print_messages = output_messages is True
        self.logger.info("Mail Directory: {:s}".format(mail_dir))

    async def handle_DATA(self, server, session, envelope):
        peer = session.peer
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos
        data = envelope.content.decode('utf-8')

        self.logger.info("Incoming mail from {:s}".format(mail_from))
        for recipient in rcpt_tos:
            self.logger.info("Mail received for {:s}".format(recipient))
            mail_file = "{:d}.{:s}.msg".format(int(time.time()), mail_from)
            mail_path = os.path.join(self.mail_dir, recipient, mail_file)
            if not os.path.isdir(os.path.join(self.mail_dir, recipient)):
                os.mkdir(os.path.join(self.mail_dir, recipient))
            with open(mail_path, 'a') as open_file:
                open_file.write(data + "\n")

            if self.print_messages:
                self.logger.info(data)
        return '250 OK'


def _parse_args():
    """
    Parse the CLI arguments for use by NullSMTPD.

    :return: namespace containing the arguments parsed from the CLI
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--no-fork", action="store_true",
                        help="Don't fork and run nullsmtpd as a daemon. Additionally, this will"
                             "print all log messages to stdout/stderr and all emails to stdout.")
    parser.add_argument("-H", "--host", type=str, default="localhost",
                        help="Host to listen on (defaults to localhost)")
    parser.add_argument("-P", "--port", type=int, default=25,
                        help="Port to listen on (defaults to 25)")
    parser.add_argument("--mail-dir", type=str, default=NULLSMTPD_DIRECTORY,
                        help="Location to write logs and emails (defaults to ~/.nullsmtpd)")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s ("+__version__+")")
    return parser.parse_args()


def main():
    """
    Main process where we get the CLI arguments, set up our loggers and then start NullSMTP,
    either running it as a daemon (default behavior) or interactively based on a passed in flag.
    """
    args = _parse_args()
    if not os.path.isdir(args.mail_dir):
        os.mkdir(args.mail_dir)

    if args.no_fork is not True:
        pid = os.fork()
        if pid is not 0:
            raise SystemExit()

    host = args.host
    port = args.port
    output_messages = 'no_fork' in args and args.no_fork
    logger = configure_logging(args.mail_dir, output_messages)
    mail_dir = args.mail_dir

    logger.info("Starting nullsmtpd {:s} on {:s}:{:d}".format(__version__, host, port))
    controller = Controller(NullSMTPDHandler(logger, mail_dir, output_messages), hostname=host, port=port)
    try:
        controller.start()
        if output_messages:
            input('nullsmtpd running. Press enter to stop server and exit.')
            raise SystemExit
    finally:
        logger.info('Stopping nullsmtpd')
        controller.stop()


if __name__ == "__main__":
    main()
