#! /usr/bin/env python
#-*- encoding: utf-8 -*-
"""
wisesaw.py

post wise saw from following web site
http://www.meigensyu.com/
"""

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2009/01/24 22:47:30$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"


import urllib
from HTMLParser import HTMLParser, HTMLParseError
from Haiku import Twitter

WISE_SAW_URL = 'http://www.meigensyu.com/quotations/view/random'

username = 'hoge'
password = 'piyo'

class ExtractWiseSaw(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.codec = 'utf-8'

        self.wise_saw = u''
        self.author = u''
        self.url = u''

        self._in_text = False
        self._in_link = False
        self._in_authority = False
        self._data_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'div' == tag and 'class' in attrs:
            if 'text' == attrs['class']:
                self._in_text = True
            elif 'link' == attrs['class']:
                self._in_link = True

        if 'a' == tag and not self._in_link and self._data_count == 1:
            self._in_authority = True

    def handle_endtag(self, tag):
        if 'div' == tag and self._in_text:
            self._in_text = False
        if 'div' == tag:
            self._data_count = 0

    def handle_data(self, data):
        if self._in_text:
            self.wise_saw += data.decode(self.codec)

        if self._in_link:
            self.author = data.decode(self.codec)
            self._data_count += 1
            self._in_link = False

        if self._in_authority:
            self.author += data.decode(self.codec) + ' '
            self._in_authority = False
            

def main():
    try:
        f = urllib.urlopen(WISE_SAW_URL)
        data = f.read()
        # extract text and author from HTML
        parser = ExtractWiseSaw()
        parser.feed(data)
        parser.close()
        wise_saw = parser.wise_saw.encode(parser.codec)
        author = parser.author.encode(parser.codec)
        author = author.strip()

        description = '%s （%s）' % (wise_saw, author)

        if len(wise_saw) > 0 and len(author) > 0:
            twitter = Twitter(username, password)
            twitter.updateStatus(description, 'Python')
        else:
            main()

    except HTMLParseError, msg:
        print 'HTMLParseError:', msg
        main()

    except Exception, e:
        print e
        main()

if __name__ == '__main__':
    main()
