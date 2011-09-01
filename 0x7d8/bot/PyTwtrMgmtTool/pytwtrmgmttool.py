# -*- coding: utf-8 -*-;
#
# pytwtrmgmttool.py  ---  twitter management tool for python
#
# external packages
#   - simplejson (for Python 2.5 or earlier)
#   - oauth
#   - pit
#
# API reference
# 1. Twitter API
#   http://apiwiki.twitter.com/Twitter-API-DocumentationTwitter API
#
# Request token URL : http://twitter.com/oauth/request_token
# Access token URL : http://twitter.com/oauth/access_token
# Authorize URL : http://twitter.com/oauth/authorize
#

__author__  = 'ymotongpoo <ymotongpoo AT gmail DOT com>'
__version__ = '1.0'
__date__    = '2009/11/29 (Sun)'

import urllib, urllib2
import time, random
import hmac, hashlib
from datetime import datetime, timedelta
try:
    import simplejson as json
except:
    import json
from oauth import oauth

from pit import Pit

TWTR_TIME_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'
INTERVAL = 90
DECODING = 'utf-8'
APPNAME  = 'pytwtrmgmttool'

following_url = 'http://twitter.com/statuses/friends.json'
unfollow_url  = 'http://twitter.com/friendships/destroy/%s.json'

class TwitterClass:
    def __init__(self, ckey, csecret, atoken, asecret):
        self.following = []
        self.follower  = []
        self.ckey = ckey
        self.csecret = csecret
        self.atoken = atoken
        self.asecret = asecret

        
    def _init_params(self):
        return dict( oauth_consumer_key = self.ckey,
                     oauth_signature_method = 'HMAC-SHA1',
                     oauth_timestamp = str(int(time.time())),
                     oauth_nonce = str(random.getrandbits(64)),
                     oauth_version = '1.0',
                     oauth_token = self.atoken
                     )


    def _make_signature(self, params, url, method):
        pstr = '&'.join(['%s=%s' % (i, params[i]) for i in sorted(params)])
        msg  = '%s&%s&%s' % (method, urllib.quote(url, ''),
                             urllib.quote(pstr, ''))
        h    = hmac.new('%s&%s' % (self.csecret, self.asecret), msg, hashlib.sha1)
        sig  = h.digest().encode('base64').strip()
        return sig


    def _oauth_header(self, params):
        plist = ['%s="%s"' % (p, urllib.quote(params[p])) for p in params]
        hstr = 'OAuth %s' % (', '.join(plist),)
        return hstr


    def open_api(self, method, url, **additional):
        params = self._init_params()
        for k, v in additional.iteritems():
            params[k] = v

        sig = self._make_signature(params, url, method)
        params['oauth_signature'] = sig

        for k in additional.keys():
            params[k] = ''

        req = urllib2.Request(url)
        for k, v in additional.iteritems():
            req.add_data( '%s=%s' % (k, urllib.quote(v, '')) )
                
        req.add_header('Authorization', self._oauth_header(params))
        return urllib2.urlopen(req)


    def get_following(self, cursor=-1):
        p = self.open_api('GET', following_url + '?cursor=' + str(cursor))
        data = json.loads(p.read().decode(DECODING))
        next = data['next_cursor']
        
        self.following += [u for u in data['users']]

        if next != 0:
            self.get_following(next)
        else:
            return len(self.following)
            

    def _is_inactive(self, x):
        try:
            last   = time.strptime(x['status']['created_at'], TWTR_TIME_FORMAT)
            dtlast = datetime(last.tm_year, last.tm_mon, last.tm_mday,
                              last.tm_hour, last.tm_min, last.tm_sec)
            today = datetime.today()
                
            return (today - dtlast) > timedelta(days=INTERVAL)

        except Exception, e:
            return False


    def get_inactive(self):
        return [u for u in self.following if self._is_inactive(u)]


    def unfollow(self, users):
        result = []
        for u in users:
            id = str(u['id'])
            r = self.open_api('POST', unfollow_url % (id,), id=id)
            d = json.loads(r.read().decode(DECODING))
            result.append(d)
        return result


if __name__ == '__main__':
    appname = APPNAME
    oauth_keys = Pit.get( appname, {'require' : {
                'consumer_key' : 'Your consumer_key from web',
                'consumer_secret' : 'Your consumer_secret from web'
                'access_token' : 'Your access_token from accsess_token.py'
                'access_token_secret' : 'Your access_token_secret from accsess_token.py'
                }})
    ckey    = oauth_keys['consumer_key']
    csecret = oauth_keys['consumer_secret']
    atoken  = oauth_keys['access_token']
    asecret = oauth_keys['access_token_secret']

    tw = TwitterClass(ckey, csecret, atoken, asecret)
    tw.get_following()
    inactives = tw.get_inactive()
    print tw.unfollow(inactives)
    
