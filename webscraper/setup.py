# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

long_description = open('README.rst', 'rb').read()

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

setup(
    name='webscraper',
    version=version,
    url='https://github.com/ymotongpoo/',
    license='LGPL',
    author='Yoshifumi YAMAGUCHI',
    author_email='ymotongpoo@gmall.com',
    description='a library for web scraping',
    long_description=__doc__,
    packages=['webscraper'],
    install_requires=[
        'setuptools',
        ],
    extras_require=dict(
        test=[
            'lxml>=2.3'
            ],
        ),
)
