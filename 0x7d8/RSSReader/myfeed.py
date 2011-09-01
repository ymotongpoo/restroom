# -*- encoding: utf-8 -*-;
"""
feed.py

Class for parsing RSS/ATOM feeds.
Referred to Ch.8.5.3 in Python Library Referrence

RSS1.0:
    http://www.kanzaki.com/docs/sw/rss.html#rss-set

RSS2.0:
    http://blog.koshigoe.jp/archives/2005/05/rss20.html

"""

import xml.parsers.expat

class FeedParser:
    def __init__(self, body):
        self.body = body
        self.parser = xml.parsers.expat.ParserCreate()

    def GetRssType(self, body = ''):
        p = xml.parsers.expat.ParserCreate()
        
        def start_element(name, attrs):
            if name == 'rdf:RDF':
                print attrs

        def end_element(name):
            if name == 'rdf:RDF':
                print 'end'

        def char_data(data):
            pass

        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data
        
        if len(body) == 0:
            p.Parse(self.body)
        else:
            p.Parse(body)

    def do_parsing(self):
        r = RSS10Handlers
        self.parser.StartElementHandler = r.start_element
        self.parser.EndElementHandler = r.end_element
        self.parser.CharacterDataHandler = r.char_data

        self.parser.Parse(self.body)


class FeedHandlers:
    def __init__(self):
        pass

    @classmethod
    def state_element(name, attrs):
        if name == 'rss':
            if 'version' in attrs and attrs['version'] == '2.0':
                return RSS20Handler()
                


class RSS10Handlers:
    def __init__(self):
        pass

    @staticmethod
    def start_element(name, attrs):
        print 'Start element: ', name, attrs

    @staticmethod
    def end_element(name):
        print 'End element: ', name

    @staticmethod
    def char_data(data):
        print 'Character data: ', repr(data)


class RSS20Handlers:
    def __init__(self):
        pass

    @staticmethod
    def start_element(name, attrs):
        print 'Start element: ', name, attrs

    @staticmethod
    def end_element(name):
        print 'End element: ', name

    @staticmethod
    def char_data(data):
        print 'Character data: ', repr(data)


class ATOMHandlers:
    def __init__(self):
        pass

    @staticmethod
    def start_element(name, attrs):
        print 'Start element: ', name, attrs

    @staticmethod
    def end_element(name):
        print 'End element: ', name

    @staticmethod
    def char_data(data):
        print 'Character data: ', repr(data)

