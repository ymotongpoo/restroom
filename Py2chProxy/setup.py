# -*- coding: utf-8 -*-

import sys
try:
  from setuptools import setup, find_packages
except:
  from distutils import setup, find_packages

version = '0.0.1'

classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: Japanese',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: BBS',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
    ]

setup(
    name='Py2chProxy',
    version=version,
    url='https://github.com/ymotongpoo/restroom/Py2chProxy',
    license='LGPL',
    author='Yoshifumi YAMAGUCHI',
    author_email='ymotongpoo@gmall.com',
    description='a library for handling 2ch bbs, mainly for browsing it.',
    long_description=__doc__,
    packages=['Py2chProxy'],
    install_requires=[
        'setuptools',
        'flask'
        ],
    extras_require=dict(
      test=['nose>=1.0.0'],
    ),
    test_suite='nose.collector',
    tests_require=['nose']
)
