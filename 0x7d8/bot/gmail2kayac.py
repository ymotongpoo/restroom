# -*- coding: utf-8 -*-;
#
# gmail2kayac.py  ---  notify new mail comming in gmail inbox to iPhone user 
#                      through im.kayac.com
#
# external packages
#   - Universal Feed Parser
#     http://www.feedparser.org/
#   - Pit
#
# API reference
# 1. im.kayac.com
#   http://im.kayac.com
#

__author__  = 'ymotongpoo <ymotongpoo AT gmail DOT com>'
__version__ = '0.1'
__date__    = '2009/12/09 (Wed)'

import sys
import urllib
from pit import Pit

try:
    import feedparser
except:
    print 'Universal Feed Parser is necessary'
    sys.exit(2)

try:
    import json
except:
    import simplejson as json

GMAILATOM = 'https://%s:%s@mail.google.com/mail/feed/atom/'
KAYAC_URL = 'http://im.kayac.com/api/post/%s'

def notify(message, user, password='', handler=''):
    url = KAYAC_URL % (user,)
    postparams = dict( message = message,
                       handler = handler,
                       password = password )
    params = urllib.urlencode(postparams)
    
    p = urllib.urlopen(url, params)
    r = json.loads(p.read())
    return r
    
def main():
    gmail = Pit.get('gmail', {'require' : {
                'user' : 'Gmail account name',
                'pass' : 'password for Gmail account',
                'fullcount' : '0'
                }})

    kayac = Pit.get('kayac', {'require' : {
                'user' : 'im.kayac.com account name',
                'pass' : 'password for im.kayac.com account'
                }})

    d = feedparser.parse( GMAILATOM % (gmail['user'], gmail['pass']) )
    

    if int(d.feed.fullcount) == int(gmail['fullcount']):
        sys.exit(0)
    
    elif int(d.feed.fullcount) > int(gmail['fullcount']):
        for e in d.entries:
            title = e.title
            author = e.author
            message = '%s <%s> [%s@gmail.com]' % (title, author, gmail['user'])
            r = notify(message, kayac['user'], kayac['pass'])

        if r['result'] != 'posted':
            print 'failed', r
            sys.exit(2)

    Pit.set('gmail', {'data' : {
                'user' : gmail['user'],
                'pass' : gmail['pass'],
                'fullcount' : str(d.feed.fullcount)}})


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print Exception, e
