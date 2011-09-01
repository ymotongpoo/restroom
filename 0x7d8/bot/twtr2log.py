# -*- coding: utf-8 -*-;
#
# twtr2log.py  ---  get twitter post using Twiter API and write them to daily log files
#
# external packages
#   - simplejson (for Python 2.5 or earlier)
#
# API reference
# 1. Twitter API
#   http://apiwiki.twitter.com/Twitter-API-Documentation
#
#
# TODO toward version 2.0
#   1. fetch in-reply-to tweet
#   2. log conversion class
#

__author__  = 'ymotongpoo <ymotongpoo AT gmail DOT com>'
__version__ = '1.1'
__date__    = '2009/12/26 (Sat)'

# for Web service
import urllib
try:
    import simplejson as json
except ImportError:
    import json

# for taking log
import time
from datetime import date, timedelta, datetime
from os import path
import sys
import getopt
import string

ENCODING = 'utf-8'
DECODING = 'utf-8'
TWTR_API = 'http://twitter.com/statuses/user_timeline/%s.json?since_id=%s'
TWTR_TIME_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'
LOG_TIME_FORMAT  = '%Y-%m-%dT%H:%M:%S'
SEPARATOR = '\t'


def convert_jst(created_at):
    st = time.strptime(created_at, TWTR_TIME_FORMAT)
    gt = datetime(st.tm_year, st.tm_mon, st.tm_mday,
                  st.tm_hour, st.tm_min, st.tm_sec)
    lt = gt + timedelta(hours=9)
    return lt.strftime(LOG_TIME_FORMAT)


def json2list(data):
    tweets = [t for t in json.loads(data)]

    none2blank = lambda t : str(t) if t is not None else u''

    timeline = []
    for tweet in tweets:
        created_at = convert_jst(tweet['created_at'])
        
        tweet = [str(tweet['id']), 
                 string.replace(tweet['text'].encode(ENCODING), '\n', ' '), 
                 created_at, 
                 none2blank(tweet['in_reply_to_status_id']),
                 none2blank(tweet['in_reply_to_user_id']),
                 none2blank(tweet['location'])
                 ]

        timeline.append(tweet)
    
    return timeline


def process(user_id, logdir):
    today = date.today().strftime('%Y%m%d') + '.log'
    
    since_id = 1
    logpath = path.join(logdir, today)
    if path.exists(logpath):
        f = open(logpath, 'r')
        since_id = int(f.readlines().pop().split(SEPARATOR)[0])
        f.close()

    url = TWTR_API % (user_id, since_id)
    p = urllib.urlopen(url)
    data = p.read().decode(DECODING)
    timeline = json2list(data)
    
    timeline.sort()
    
    f = open(logpath, 'a')
    for t in timeline:
        print t
        line = SEPARATOR.join(t) + '\n'
        f.write(line)
    
    f.close()


def usage():
    print "usage : python twtr2log.py -i <twitter id> -p <log path>"


if __name__=='__main__':
    if len(sys.argv) < 2 or '-i' not in sys.argv or '-p' not in sys.argv:
        usage()
        sys.exit()
    else:
        try:
            opts, opt_args = getopt.getopt(sys.argv[1:], 'i:p:')
        except getopt.GetoptError:
            usage()
            sys.exit(2)
                
        for o, v in opts:
            if o == '-i':
                twitter_id = v
            elif o == '-p':
                logdir = v

        process(twitter_id, logdir)
