#!/usr/bin/env python3
"""
Setup file for nullsmtp
"""
from setuptools import setup
from nullsmtp import __author__, __version__

setup(name='nullsmtp',
      version=__version__,
      url='http://github.com/MasterOdin/nullsmtp',
      descriptoin='Fake SMTP server',
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
     )
