# -*- encoding: utf-8 -*-
"""
Bookmark.py
"""

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/11/21 22:08:48$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import xmlrpclib

class HatenaBookmark:
    def __init__(self):
        self.apiaddress = "http://b.hatena.ne.jp/xmlrpc"
        self.server = xmlrpclib.ServerProxy(self.apiaddress)

    def getCount(self, urls=[]):
        """
        get bookmark count of specific web page
        """
        result = {}
        if len(urls) < 50:
            result = self.server.bookmark.getCount(*urls)
        else:
            print "Over 50 URLs"
        return result


    def getTotalCount(self, urls=[]):
        """
        get bookmark count of one site
        """
        result = {}
        if len(urls) < 50:
            for u in urls:
                result[u] = self.server.bookmark.getTotalCount(u)
        else:
            print "Over 50 URLs"
        return result


    def getAsinCount(self, asins=[]):
        """
        get collections of asin
        """
        result = {}
        if len(asins) < 50:
            result = self.server.bookmark.getAsinCount(*asins)
        else:
            print "Over 50 ASINs"
        return result


if __name__ == '__main__':
    urls = ['http://d.hatena.ne.jp/ymotongpoo','http://www.python.org']
    hb = HatenaBookmark()
    r = hb.getCount(urls)
    print r

