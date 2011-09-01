#! /usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import sqlite3
import os
import time
import xmlrpclib

CODING = 'utf-8'
BASE_DIR = os.path.dirname(__file__)
DATABASE_FILE = os.path.join(BASE_DIR, '2ch-summary.db')
APIURL = "http://b.hatena.ne.jp/xmlrpc"
server = xmlrpclib.ServerProxy(APIURL)

def get_site_list():
    sitelist = []
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('select site_id, feedurl, title, url from tsite')
    for s in cur.fetchall():
        sitelist.append(dict(id=s[0],
                             feedurl=s[1],
                             title=s[2],
                             url=s[3]))
    return sitelist


def search_siteid(url, sitelist):
    for s in sitelist:
        try:
            s['url'].index(url)
            return s['id']
        except Exception:
            continue


def get_feed(rsslist):
    feedlist = []
    for u in rsslist:
        try:
            feedlist.append(feedparser.parse(u))
        except Exception, e:
            sys.exc_info()[0]
            sys.exc_info()[1]
    
    return feedlist


def rss10feed(feed):
    entries = []
    e = {}
    site = dict(title=feed['feed']['title'].encode(CODING),
                url=feed['feed']['link'].encode(CODING))
    
    for e in feed['entries']:
        updated = time.strftime('%Y-%m-%d %H:%M:%S+09:00',
                                time.strptime(e['updated'], '%Y-%m-%dT%H:%M:%S+09:00'))
        
        entries.append(dict(title=e['title'].encode(CODING).strip(),
                            summary=e['summary'].encode(CODING),
                            url=e['link'].encode(CODING),
                            updated=updated.encode(CODING),
                            site=site))
    return entries


mapfeedfunc = {
    'livedoor': rss10feed,
    'fc2.com': rss10feed
    }


def main():
    # get urllist from DB
    sitelist = get_site_list()
    feedurllist = []
    for s in sitelist:
        feedurllist.append(s['feedurl'])

    # fetch entry data from web
    entrylist = []
    for feed in get_feed(feedurllist):
        feed['feed']['title'].encode(CODING)

        portal = rss10feed
        for k, v in mapfeedfunc.iteritems():
            try:
                feed['feed']['link'].encode(CODING).index(k)
                portal = k
            except:
                continue

        entrylist += mapfeedfunc[portal](feed)

    # insert entry data into DB
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    for e in entrylist:
        t = (e['url'],)
        cur.execute('select url from tentry where url = ?', t)
        if len(cur.fetchall()) == 0:
            site_id = search_siteid(e['site']['url'], sitelist)
            user = server.bookmark.getCount(e['url'])
            t = (e['url'], e['title'], e['summary'], e['updated'], site_id, user[e['url']])
            cur.execute('insert into tentry (url, title, summary, updated, site_id, user) '
                        'values (?, ?, ?, datetime(?), ?, ?)', t)
    conn.commit()
    conn.close()
    

if __name__ == '__main__':
    main()
