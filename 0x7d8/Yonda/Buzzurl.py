#-*- encoding: utf-8 -*-
"""
Buzzurl.py


"""

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2009/02/01 18:30:41$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"


import urllib
from HTMLParser import HTMLParser, HTMLParseError
import re # temporary for invalid HTML of hatena bookmark web page

class ExtractEntryInfo(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.codec = 'utf-8'

        self.entry = {}
        self.entries = []

        self.in_entry_body = False
        self.in_entry_ptag = False
        self.in_users = False
        self.in_user_ptag = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'div' == tag and 'class' in attrs:
            if 'detail' == attrs['class']:
                self.in_entry_body = True

        if 'p' == tag and 'class' in attrs and self.in_entry_body:
            if 'txt' == attrs['class']:
                self.in_entry_ptag = True

        if 'a' == tag and self.in_entry_body and self.in_entry_ptag:
            url = attrs['href'].decode(self.codec)
            urlstart = url.index('http')
            self.entry['url'] = url[urlstart:]

        if 'div' == tag and 'class' in attrs:
            if 'userinfo' == attrs['class']:
                self.in_users = True

        if 'p' == tag and 'class' in attrs and self.in_users:
            if 'num' == attrs['class']:
                self.in_user_ptag = True
                
            
    def handle_endtag(self, tag):
        if 'div' == tag and self.in_entry_body:
            self.in_entry_body = False
            self.entries.append(self.entry)
            self.entry = {}

        if 'div' == tag and self.in_users:
            self.in_users = False

        if 'p' == tag and self.in_user_ptag:
            self.in_user_ptag = False

        if 'p' == tag and self.in_entry_ptag:
            self.in_entry_ptag = False


    def handle_data(self, data):
        if self.in_entry_body and self.in_entry_ptag:
            self.entry['title'] = data.decode(self.codec)

        if self.in_users and self.in_user_ptag:
            self.entry['user'] = int(data.strip())


class Buzzurl:
    rooturi = u'http://buzzurl.jp/'
    hbcodec = 'utf-8'
    
    def __init__(self):
        pass


    def __parseResultBody(self, htmlbody):
        try:
            parser = ExtractEntryInfo()
            parser.feed(htmlbody)
            parser.close()
        except HTMLParseError, msg:
            print 'Error Message: %s' % msg
        return parser.entries


    def searchByTag(self, tag, sort=u'', offset=0):
        if len(tag) != 0:
            uri = self.rooturi + u'tag/' + tag
        else:
            raise Exception('NoTagException')

        getdict = {}
        if len(sort) != 0:
            getdict['sort'] = sort

        if offset > 0:
            getdict['of'] = offset

        if len(getdict):
            params = urllib.urlencode(getdict)
            uri += '?' + params

        f = urllib.urlopen(uri.encode(self.hbcodec))
        data = f.readlines() # magic code for hatena bookmark result
        p = re.compile('"class')
        for i, l in enumerate(data):
            l = p.sub('" class', l)
            data[i] = l.lstrip()
            
        data = ''.join(data)
        return self.__parseResultBody(data)
