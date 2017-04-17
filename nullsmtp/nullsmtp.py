#!/usr/bin/env python3
"""
NullSMTP module that allows to run a mock email server that just logs all incoming emails to a file
instead of actually trying to send them. Helps for developing applications that utilize email,
without spamming customers' emails and not having overhead from some GUI program.
"""
import argparse
import asyncore
import logging
import os
import smtpd
import sys
import time

__author__ = 'Matthew Peveler'
__version__ = '0.2.0'
__license__ = 'Unlicense (Public Domain)'

LOGGER = logging.getLogger("nullsmtp")
LOGGER.setLevel(logging.INFO)


class NullSMTP(smtpd.SMTPServer):
    """
    Fake SMTP server
    """
    def __init__(self, localaddr, mail_dir):
        smtpd.SMTPServer.__init__(self, localaddr, None)
        if mail_dir is not None and not os.path.isdir(mail_dir):
            try:
                os.mkdir(mail_dir)
            except IOError as io_error:
                logging.error(str(io_error))
                raise
        self.mail_dir = mail_dir
        LOGGER.info("Starting nullsmtp started on {:s}:{:d}".format(*localaddr))
        if self.mail_dir is not None:
            LOGGER.info("Mail Directory: {:s}".format(self.mail_dir))
        else:
            LOGGER.info("Mail Directory could not be created. Emails won't be written to file.")

    # pylint: disable=arguments-differ
    def process_message(self, peer, mailfrom, rcpttos, data, **_):
        """
        Process incoming email messages

        :param peer:
        :param mailfrom:
        :param rcpttos:
        :param data:
        :return:
        """
        LOGGER.info("Incoming mail from {:s}".format(mailfrom))
        for recipient in rcpttos:
            LOGGER.info("Mail received for {:s}".format(recipient))
            if self.mail_dir is not None:
                mail_file = "{}.{:d}.msg".format(mailfrom, int(time.time()))
                mail_path = os.path.join(self.mail_dir, recipient, mail_file)
                if not os.path.isdir(os.path.join(self.mail_dir, recipient)):
                    os.mkdir(os.path.join(self.mail_dir, recipient))
                with open(mail_path, 'a') as open_file:
                    open_file.write(data + "\n")
            else:
                LOGGER.info(data)


def _parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--log-level", type=int, default=1, choices=[0, 1, 2],
                        help="Level of logging from 0 (nothing), 1 (just to file), "
                             "and 2 (to file and console). Defaults to 2.")
    parser.add_argument("-H", "--host", type=str, default="localhost", help="Host to listen on")
    parser.add_argument("-P", "--port", type=int, default=25, help="Port to listen on")
    parser.add_argument("--mail-dir", type=str, default="/var/log/nullsmtp",
                        help="Location to write email logs")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s ("+__version__+")")
    return parser.parse_args()


def main():
    """
    Main process
    :return:
    """
    args = _parse_args()
    if not os.path.isdir(args.mail_dir):
        try:
            os.mkdir(args.mail_dir, 777)
        except IOError:
            args.mail_dir = None

    log_format = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    if args.log_level > 0:
        if args.mail_dir is not None:
            file_logger = logging.FileHandler(os.path.join(args.mail_dir, "nullsmtp.log"))
            file_logger.setFormatter(log_format)
            LOGGER.addHandler(file_logger)

        if args.log_level == 2:
            console_logger = logging.StreamHandler(sys.stdout)
            console_logger.setFormatter(log_format)
            LOGGER.addHandler(console_logger)
    else:
        LOGGER.addHandler(logging.NullHandler())

    smtp_server = NullSMTP((args.host, args.port), args.mail_dir)
    # noinspection PyBroadException
    # pylint: disable=bare-except
    try:
        asyncore.loop()
    except:
        logging.info("Stopping nullsmtp")
        smtp_server.close()


if __name__ == "__main__":
    main()
