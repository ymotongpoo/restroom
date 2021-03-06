#-*- encoding: utf-8 -*-
"""
HatenaBookmark.py


"""

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/12/10 00:29:41$"
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
        self.in_users = False
        self.in_user_atag = False
        self.in_h3 = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'div' == tag and 'class' in attrs:
            if 'entry-body' == attrs['class']:
                self.in_entry_body = True
                
        if 'h3' == tag and self.in_entry_body:
            self.in_h3 = True

        if 'a' == tag and not 'class' in attrs and self.in_entry_body and self.in_h3:
            self.entry['url'] = attrs['href'].decode(self.codec)
            self.entry['title'] = attrs['title'].decode(self.codec)

        if 'li' == tag and 'class' in attrs and self.in_entry_body:
            if 'users' == attrs['class']:
                self.in_users = True

        if 'a' == tag and self.in_users:
            self.in_user_atag = True
            
            
    def handle_endtag(self, tag):
        if 'li' == tag and self.in_users:
            self.in_users = False
            self.entries.append(self.entry)
            self.entry = {}

        if 'h3' == tag and self.in_h3:
            self.in_h3 = False

        if 'a' == tag and self.in_user_atag:
            self.in_user_atag = False

    def handle_data(self, data):
        if self.in_users and self.in_user_atag:
            users = data.split(' ')
            self.entry['user'] = int(users[0])


class HatenaBookmark:
    rooturi = u'http://b.hatena.ne.jp/'
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
            uri = self.rooturi + u't/' + tag
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
