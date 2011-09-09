# -*- coding: utf-8 -*-

import sys
import os.path
from setuptools import setup, find_packages

##### utility functions
def read(name):
  return open(os.path.join(os.path.dirname(__file__), name)).read()


##### meta
long_description = read('README.rst')

version = '0.0'

classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operation System :: Mac OS :: Mac OS X',
        'Operation System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
    ]

requires = [
  "lxml >= 2.3",
]

extras_require = dict(
  test = [
    "lxml >= 2.3",
    "pytest >= 2.1.1"
    ]
)


##### properties
setup(
    name='webscraper',
    version=version,
    url='https://github.com/ymotongpoo/',
    license='BSD',
    author='Yoshifumi YAMAGUCHI',
    author_email='ymotongpoo@gmall.com',
    description='a library for web scraping',
    long_description=__doc__,
    packages=find_packages(exclude=['test']),
    install_requires=requires,
    extras_require=extras_require,
)
