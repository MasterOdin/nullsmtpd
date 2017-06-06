"""
Setup file for nullsmtp
"""
import os
import pwd
from setuptools import setup
from nullsmtp import __author__, __version__

# If we're not running as root, or the /etc/init.d folder doesn't exist, don't bother copying
# in our services file for NullSMTP
# pylint: disable=invalid-name
if pwd.getpwnam("root").pw_uid != os.getuid() or not os.path.isdir(os.path.join("etc", "init.d")):
    data_files = []
else:
    data_files = [('/etc/init.d', ['init.d/nullsmtp'])]

setup(name='nullsmtp',
      version=__version__,
      url='http://github.com/MasterOdin/nullsmtp',
      description='Fake SMTP server',
      long_description=open('README.rst').read(),
      author=__author__,
      author_email='matt.peveler@gmail.com',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3 :: Only',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'License :: Public Domain',
          'Topic :: Communications :: Email :: Mail Transport Agents'
      ],
      packages=['nullsmtp'],
      entry_points={
          'console_scripts': [
              'nullsmtp = nullsmtp:main',
          ]
      },
      data_files=data_files)
