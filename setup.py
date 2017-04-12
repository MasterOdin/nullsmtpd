#!/usr/bin/env python3

from setuptools import setup

setup(name='nullsmtp',
      version='0.1.0',
      url='http://github.com/MasterOdin/nullsmtp',
      descriptoin='Fake SMTP server',
      long_description=open('README.rst').read(),
      author='Matthew Peveler',
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
      scripts=['nullsmtp']
)
