# -*- coding: utf-8 -*-
"""
http://www.python.jp/doc/release/library/configparser.html
"""

import ConfigParser

config = ConfigParser.SafeConfigParser()
config.read("test.cfg")

print config.get('test1', 'property1')
print config.get('test1', 'property2')
print config.get('test1', 'property3')

print config.getint('test2', 'foo')
print config.getfloat('test2', 'bar')
print config.getboolean('test2', 'buz')

print config.sections()
