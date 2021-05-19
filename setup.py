"""Setup file for nullsmtpd."""
from setuptools import setup
from nullsmtpd.version import __author__, __version__


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
      install_requires=['aiosmtpd<=1.3'])
