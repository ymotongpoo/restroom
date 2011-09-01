#-*- coding: utf-8 -*-
#
# dlc2blgr.py  --- post delicious log to Blogger
#
# external packages
#   - lxml
#   - gdata-python-client
#
# API reference
# 1. Delicious API reference
#   http://delicious.com/help/api
#
#

__author__  = 'ymotongpoo <ymotongpoo AT gmail DOT com>'
__version__ = '1.0'
__date__    = '2009/12/09 (Tue)'

import lxml
import urllib
import time

from datetime import datetime, timedelta
from lxml import etree
from StringIO import StringIO

from gdata import service, client
from gdata.blogger import client
import gdata
import atom

from pit import Pit
import sys

DELICIOUS_API = 'https://%s:%s@api.del.icio.us/v1/posts/get?dt=%s'
TITLE = '[Delicious] %s'

ENCODING = 'utf-8'
DECODING = 'utf-8'
DELICIOUS_FORMAT = '%Y-%m-%d'
DATE_OFFSET = 2

class BloggerOperator:
    def __init__(self, email=None, password=None):
        self.blogger_service = None
        self.email = email
        self.password = password

    def ClientLogin(self, email=None, password=None):
        if not email:
            email = self.email
        if not password:
            password = self.password
        self.blogger_service = service.GDataService(email, password)
        self.blogger_service.source = 'LOG2BLGR'
        self.blogger_service.service = 'blogger'
        self.blogger_service.accout_type = 'GOOGLE'
        self.blogger_service.server = 'www.blogger.com'
        self.blogger_service.ProgrammaticLogin()

    def CreatePublicPost(self, title, content):
        query = service.Query()
        query.feed = '/feeds/default/blogs'
        feed = self.blogger_service.Get(query.ToUri())
        blog_id = feed.entry[0].GetSelfLink().href.split('/')[-1]

        entry = gdata.GDataEntry()
        entry.title = atom.Title('xhtml', title)
        entry.content = atom.Content(content_type='html', text=content)
        return self.blogger_service.Post(entry, '/feeds/%s/posts/default' % blog_id)


def retrieve_posts(duser, dpass, date):
    def extract_property(post):
        return dict( link  = post.attrib['href'],
                     hash  = post.attrib['hash'],
                     title = post.attrib['description'],
                     time  = post.attrib['time'],
                     desc  = post.attrib['extended'] )
                    
    url = DELICIOUS_API % (duser, dpass, date)
    u = urllib.urlopen(url)
    data = u.read()
    
    tree = etree.parse(StringIO(data), etree.XMLParser())
    posts = [extract_property(p) for p in tree.xpath('//post')]
    return posts


def post2content(post):
    line = '<li/><a href="%s">%s</a>' % (post['link'], post['title'])
    if len(post['desc'].strip()) > 0:
        line += ' : ' + post['desc']
    return line


def process(duser, dpass, date, gemail, gpass):
    title_date = date.strftime('%Y-%m-%d (%a)')
    api_date   = date.strftime(DELICIOUS_FORMAT)

    posts = retrieve_posts(duser, dpass, api_date)
    if len(posts) > 0:
        title = TITLE % (title_date,)
        content = ''.join([post2content(p) for p in posts])
        
        blgr = BloggerOperator(gemail, gpass)
        blgr.ClientLogin()
        blgr.CreatePublicPost(title, content)
    else:
        print date.strftime(DELICIOUS_FORMAT) + ' : no posts'


if __name__ == '__main__':
    try:
        daccount = Pit.get('delicious', {'require' : {
                    'user' : 'delicious account name',
                    'pass'  : 'password for delicious account'
                    }})

        gaccount = Pit.get('google', {'require' : {
                    'email' : 'Google mail account',
                    'pass'  : 'password for Google account'
                    }})
        
        target_date = datetime.today() - timedelta(days=DATE_OFFSET)
                
        process(daccount['user'], daccount['pass'], target_date, 
                gaccount['email'], gaccount['pass'])
    except Exception, e:
        print 'error -> ', Exception, e
        sys.exit(2)
