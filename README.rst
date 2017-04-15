nullsmtp
========

nullsmtp is a fake SMTP server (written in python) which can be used for development. The server catches incoming mail,
writes them to a file, and doesn't actually send it out to the intended recipients. All emails are saved to a directory
(defaults to ``/var/log/nullsmtp``, but can be changed via flag) where each email address sent to gets its own folder
and then emails are stored in that folder named ``{sender}.{time}.msg``. This is useful for debugging applications
where you don't want a GUI (as you're running a headless VM say), but still actually need to see the messages that
were sent in the system, without having to worry about things getting bounced or whatever.

Generally, you'd probably want to install this instead of something like sendmail or some other package that would
handle sending mail from your server.

Requirements
============
nullsmtp relies on Python 3.3+ and just its standard library. Recommended to also have ``pip`` for installation.

Installation
============
Recommended Installation is through PyPi::

    pip install nullsmtp

Or if you've cloned the repository::

    python3 setup.py install


Usage
=====
::

    usage: nullsmtp [-h] [-H HOST] [-P PORT] [--mail-dir MAIL_DIR]

    optional arguments:
      -h, --help            show this help message and exit
      -H HOST, --host HOST  Host to listen on (defaults to localhost)
      -P PORT, --port PORT  Port to listen on (defaults to 22)
      --mail-dir MAIL_DIR   Location to write email logs (defaults to /var/log/nullsmtp)

By default, you will need to use sudo as the server wants to bind itself to localhost and port 22.
However, if you use a different port, then it will not require using sudo. However, note, that if the current running
user of the script does not have access to create a directory/file within ``/var/log`` or ``/var/log/nullsmtp``, then
no emails will be written to file, but just through the console.

If the mail directory is writeable to, then you should have the following directory structure::

    nullsmtp.log
    person1@example.com/
        person2@example.com.1492024462.msg
        person2@example.com.1492024232.msg
        person1@example.com.1493678462.msg
    person2@example.com/
        person1@example.com.1232421423.msg

where ``nullsmtp.log`` is just a system level log file, and then each folder represents a person's "inbox" and inside
are messages from someone at a given timestamp (seconds from epoch).
