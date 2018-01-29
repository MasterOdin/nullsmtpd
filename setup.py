"""
Setup file for nullsmtpd
"""
import os
import pwd
from setuptools import setup
from nullsmtpd.version import __author__, __version__

# If we're not running as root, or the /etc/init.d folder doesn't exist, don't bother copying
# in our services file for NullSMTP
# pylint: disable=invalid-name
if pwd.getpwnam("root").pw_uid != os.getuid() or not os.path.isdir(os.path.join("etc", "init.d")):
    data_files = []
else:
    data_files = [('/etc/init.d', ['init.d/nullsmtpd'])]

setup(name='nullsmtpd',
      version=__version__,
      url='http://github.com/MasterOdin/nullsmtpd',
      description='Fake SMTP server',
      long_description=open('README.rst').read(),
      author=__author__,
      author_email='matt.peveler@gmail.com',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Environment :: Console',
          'Framework :: AsyncIO',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'License :: Public Domain',
          'Topic :: Communications :: Email :: Mail Transport Agents'
      ],
      python_requires='>=3.5.x',
      packages=['nullsmtpd'],
      entry_points={
          'console_scripts': [
              'nullsmtpd = nullsmtpd.nullsmtpd:main',
          ]
      },
      data_files=data_files,
      install_requires=['aiosmtpd'])
