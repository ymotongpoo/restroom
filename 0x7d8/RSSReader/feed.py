# -*- encoding: utf-8 -*-;
"""
feed.py

Class for parsing RSS/ATOM feeds using Universal feed parser.
  http://feedparser.org/

Known issue:
    - MailBodyHTML() is not implemented yet
"""
__author__ = "ymotongpoo <ymotongpoo@gmail.com>"
__date__   = "21 Nov. 2008"
__credits__ = "0x7d8 -- programming training"
__version__ = "$Revision: 0.10"

import feedparser
import StringIO
import time
import sys

class Feed:
    """
    class for parsing RSS/Atom feed
    """
    def __init__(self, urlfile = [], urllist = []):
        """
        initialization

        arguments:
            urlfile : list of files which has list of URLs
            urllist : list of URLs
        """
        self.urlfile = urlfile
        self.urllist = urllist
        self.feedlist = []
        self.mailbody = ""

        for f in urlfile:
            try:
                urls = open(f).readlines()
                for u in urls:
                    self.urllist.append(u)
            except:
                print 'skipped file: ', f


    def GetFeed(self, extraurls = []):
        """
        get RSS/Atom feeds of self.urllist

        arguments:
            extraurls : list of urls
        """
        self.urllist.extend(extraurls)
        for u in self.urllist:
            try:
                self.feedlist.append(feedparser.parse(u))
            except Exception, e:
                sys.exc_info()[0]
                sys.exc_info()[1]


    def MailBodyText(self):
        """
        mail body for text mail

        return:
            formatted text of feeds
        """
        self.mailbody = '*** Feed on ' + time.strftime("%Y-%m-%d %H:%M:%S") + '***\n'
        for f in self.feedlist:
            self.mailbody += '\n\n【' + f.feed.title.encode('utf-8') + '】\n'
            for e in f.entries:
                self.mailbody += '-'*20 + '\n'
                self.mailbody += '■'+e.title.encode('utf-8') + '\n'
                self.mailbody += e.description.encode('utf-8') + '\n\n'
                self.mailbody += e.link.encode('utf-8') + '\n\n'
        return self.mailbody


    def MailBodyHTML(self):
        """
        under implementation

        return:
            HTML of feeds
        """
        for f in self.feedlist:
            f.feed.title.encode('utf-8')
            for e in f.entries:
                print '-'*20
                print e.title.encode('utf-8')
                print e.date.encode('utf-8')

