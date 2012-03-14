# -*- coding: utf-8 -*-
"""
py2ch
=====

What is this?
-------------

`py2ch` is a library for handling 2channel_,
one of the most famous BBS site like Digg.
Currently, this is mainly forcusing on browsing it,
i.e. not supporting posting comment to threads,
Be user login, and so on.

.. _2channel: http://www.2ch.net/


Setup
-----

::

   $ easy_install py2ch


"""

import sys
from setuptools import setup, find_packages

version = '0.0.3'

classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: Japanese',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: BBS',
        'Topic :: Software Development :: Libraries'
        'Topic :: Utilities',
    ]

setup(
    name='py2ch',
    version=version,
    url='https://github.com/ymotongpoo/py2ch',
    license='LGPL',
    author='Yoshifumi YAMAGUCHI',
    author_email='ymotongpoo@gmall.com',
    description='a library for handling 2ch bbs, mainly for browsing it.',
    long_description=__doc__,
    packages=['py2ch'],
    package_data={'py2ch':['test/data/*.dat']},
    install_requires=[
        'setuptools',
        ],
    extras_require=dict(
        test=[
            'nose>=1.0.0'
            ],
        ),
    test_suite='nose.collector',
    tests_require=['nose']
)
