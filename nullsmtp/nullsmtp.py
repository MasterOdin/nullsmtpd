#!/usr/bin/env python3
"""
NullSMTP module that allows to run a mock email server that just logs all incoming emails to a file
instead of actually trying to send them. Helps for developing applications that utilize email,
without spamming customers' emails and not having overhead from some GUI program.
"""
import argparse
import asyncore
import os
import socket
import smtpd
import time

from .logger import get_logger, configure_logging

__author__ = 'Matthew Peveler'
__version__ = '0.3.0'
__license__ = 'Unlicense (Public Domain)'

NULLSMTP_DIRECTORY = os.path.join(os.path.expanduser("~"), ".nullsmtp")


class NullSMTP(smtpd.SMTPServer):
    """
    Fake SMTP server based off the builtin smtpd.SMTPServer allowing us to process messages
    as they come in and then save the messages to a directory locally instead of actually
    sending them anywhere. Useful for development systems where the a real email sender
    would just trigger the spam box of Gmail or some other provider or not even send as the
    domain is set to be localhost:8080 which is an invalid sender address (but NullSMTP will
    happily accept it).
    """
    def __init__(self, localaddr, mail_dir, print_messages=False):
        """

        :param localaddr: tuple containing the host and port of the server (localhost, 25)
        :param mail_dir: directory to store the mail as it comes in
        """
        smtpd.SMTPServer.__init__(self, localaddr, None)

        self.logger = get_logger()
        if mail_dir is None or isinstance(mail_dir, str):
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
        self.print_messages = print_messages is True
        self.logger.info("Starting nullsmtp started on {:s}:{:d}".format(*localaddr))
        self.logger.info("Mail Directory: {:s}".format(self.mail_dir))

    # pylint: disable=arguments-differ
    def process_message(self, peer, mailfrom, rcpttos, data, **_):
        """
        Process incoming email messages as they're received by the server. We take all messages
        and log them to a file in the directory (mailbox) pertaining to the recipient and then
        we save the file with {seconds from epoch}.{mailfrom}.msg so that the messages
        are self-organizing.

        :param peer: the remote host's address
        :param mailfrom: the messsage's originator's address
        :param rcpttos: a list of the message's recipients
        :param data: a string containing the e-mail (which should be in RFC 2822 format)
        """
        self.logger.info("Incoming mail from {:s}".format(mailfrom))
        for recipient in rcpttos:
            self.logger.info("Mail received for {:s}".format(recipient))
            mail_file = "{:d}.{:s}.msg".format(int(time.time()), mailfrom)
            mail_path = os.path.join(self.mail_dir, recipient, mail_file)
            if not os.path.isdir(os.path.join(self.mail_dir, recipient)):
                os.mkdir(os.path.join(self.mail_dir, recipient))
            with open(mail_path, 'a') as open_file:
                open_file.write(data + "\n")

            if self.print_messages:
                self.logger.info(data)


def _parse_args():
    """
    Parse the CLI arguments for use by NullSMTP.

    :return: namespace containing the arguments parsed from the CLI
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--no-fork", action="store_true",
                        help="Don't fork and run nullsmtp as a daemon. Additionally, this will"
                             "print all log messages to stdout/stderr and all emails to stdout.")
    parser.add_argument("-H", "--host", type=str, default="localhost",
                        help="Host to listen on (defaults to localhost)")
    parser.add_argument("-P", "--port", type=int, default=25,
                        help="Port to listen on (defaults to 25)")
    parser.add_argument("--mail-dir", type=str, default=NULLSMTP_DIRECTORY,
                        help="Location to write logs and emails (defaults to ~/.nullsmtp)")
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

    output_messages = 'no_fork' in args and args.no_fork
    logger = configure_logging(args.mail_dir, output_messages)

    try:
        smtp_server = NullSMTP((args.host, args.port), args.mail_dir, output_messages)
    except socket.error:
        msg = "Could not connect to {}:{}, socket in use.".format(args.host, args.port)
        logger.error(msg)
        raise SystemExit
    # noinspection PyBroadException
    # pylint: disable=bare-except
    try:
        asyncore.loop()
    except:
        logger.info("Stopping nullsmtp\n")
        smtp_server.close()


if __name__ == "__main__":
    main()
