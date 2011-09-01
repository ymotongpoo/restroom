# -*- encoding: utf-8 -*-
"""
Count.py

Referrence:
    http://python.matrix.jp/tips/string/encoding.html#shift-jis
"""

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/12/02 00:48:52$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import urllib
from xml.dom import minidom

SITE_URL = 'http://www.benricho.org/kazu/database/kazu_database.cgi'

def searchCounterSuffix(key, encoding, proxies={}):
    key = key.encode(encoding)
    get_dict = dict( key = key,
                     select = 50)
    params = urllib.urlencode(get_dict)
    if 'http' in proxies:
        print proxies
        f = urllib.urlopen(SITE_URL + '?' + params, proxies=proxies)
    else:
        f = urllib.urlopen(SITE_URL + '?' + params)

    print f.read().decode(encoding)


def extractResult(body):
    pass


def main():
    key = u'帽子'
    encoding = 'cp932'
    #searchCounterSuffix(key, encoding)
    proxies = {'http':'http://proxy.example.com:80'}
    searchCounterSuffix(key, encoding, proxies)


if __name__ == '__main__':
    main()
