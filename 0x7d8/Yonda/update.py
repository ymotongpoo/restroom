#! /usr/bin/env python
# -*- encoding: utf-8 -*-

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2009/01/11 12:59:33$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import math
import sqlite3
import os
import urllib
import simplejson
import time, datetime

def main():
    UPDATE_UNIT = 20
    BASE_DIR = os.path.dirname(__file__)
    HATENA_URL = u'http://b.hatena.ne.jp/entry/json/'
    HALF_LIFE = 14

    conn = sqlite3.connect(os.path.join(BASE_DIR, 'bookmark.db'))
    cur = conn.cursor()

    cur.execute('select count(url) from tbookmark')
    num_bookmark = cur.fetchone()[0]

    #for i in range(0, num_bookmark/UPDATE_UNIT):
    for i in range(0, 2):
        cur.execute('select url, user+clip+buzz as point from tbookmark order by user desc limit 10 offset ' + str(i * UPDATE_UNIT))
        rows = cur.fetchall()
        try:
            for row in rows:
                #print row[0]
                params = urllib.urlencode({'url':row[0]})
                f = urllib.urlopen(HATENA_URL + '?' + params)
                data = f.read()
                print data
                """
                info = simplejson.loads(data.lstrip("(").rstrip(")"))
                
                timestamp = []
                for b in info['bookmarks']:
                    timestamp.append(b['timestamp'])
                timestamp.sort(reverse=True)
                oldest = timestamp.pop()
                oldest_sec = time.strptime(oldest, '%Y/%m/%d %H:%M:%S')
                oldest_format = time.strftime('%Y-%m-%d %H:%M:%S', oldest_sec)
                delta = time.mktime(time.localtime()) - time.mktime(oldest_sec)
                delta = datetime.timedelta(seconds=delta)
                # calculate hotpoint
                hotpoint = row[1]*pow(0.5, float(delta.days)/HALF_LIFE)

                t = (str(hotpoint), oldest_format, row[0])
                cur.execute("update tbookmark set hotpoint=?, timestamp=? where url=?",t)
                
            conn.commit()
            """

        except Exception, e:
            print e
            #conn.rollback()
            continue

        print '>>', str(i), 'th'

    conn.close()

if __name__ == '__main__':
    main()
