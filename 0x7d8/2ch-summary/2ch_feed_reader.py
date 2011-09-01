# -*- coding: utf-8 -*-

import sqlite3
from genshi.template import TemplateLoader
from mod_python import apache
import urllib
import time
from datetime import datetime, timedelta
import os

CODING = 'utf-8'
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_FILE = os.path.join(BASE_DIR, 'template.html')
DATABASE_FILE = os.path.join(BASE_DIR, '2ch-summary.db')

entry_per_page = 25

base_query = 'select a.url, a.title, a.summary, a.updated, ' + \
             'b.url as site_url, b.title as site_title ' + \
             'from tentry as a inner join tsite as b ' + \
             'on a.site_id = b.site_id'

title = {'updated':u'最新タイトル',
         'user':u'はてブランキング',
         'hot':u'直近1週間'}

def entry(req, sort='updated', offset=0):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    link_index = []
    if sort == 'updated':
        query = base_query + ' order by a.updated desc'
    elif sort == 'user':
        query = base_query + ' order by a.user desc'
    elif sort == 'hot':
        week_ago = (datetime.utcnow() - timedelta(7)).strftime('%Y-%m-%d %H:%M:%S')
        query = base_query + " where a.updated > '" + week_ago + "' order by a.user desc"
    else:
        sort = 'updated'
        query = base_query + ' order by a.updated desc'
        
    query += ' limit ' + str(entry_per_page) + ' offset ' + str(offset)
    cur.execute(query)

    # create index
    for i in range(1,11):
        link_index.append(dict(num=i,
                               link = '/dokuo/' + sort + '/' + str((i-1)*entry_per_page)))

    # create navigator
    navi_index = {}
    current = int(offset) / entry_per_page + 1 # page number
    prev = (int(offset) / entry_per_page - 1) * entry_per_page
    next = (int(offset) / entry_per_page + 1) * entry_per_page
    navi_index['current'] = current
    navi_index['prev'] = '/dokuo/' + sort + '/' + str(prev if prev > 0 else 0)
    navi_index['next'] = '/dokuo/' + sort + '/' + str(next if next > 0 else 0)
    navi_index['title'] = title[sort]
  
    entrylist = []
    for row in cur:
        # change UTC to JST
        st = time.strptime(row[3], '%Y-%m-%d %H:%M:%S')
        dt = datetime(st.tm_year, st.tm_mon, st.tm_mday, st.tm_hour, st.tm_min, st.tm_sec)
        jst = dt + timedelta(hours=9)
        updated = jst.strftime('%m/%d %H:%M')

        # shorten site title
        site_title = row[5].decode(CODING)
        site_title = site_title[:10].encode(CODING)

        e = dict(url=row[0],
                 title=row[1],
                 summary=row[2],
                 updated=updated,
                 site_url=row[4],
                 site_title=site_title)
        entrylist.append(e)
        
    loader = TemplateLoader([BASE_DIR])
    tmpl = loader.load(TEMPLATE_FILE)
    stream = tmpl.generate(entries=entrylist, index=link_index, navi=navi_index)

    req.content_type = 'text/html'
    req.send_http_header()
    req.write(stream.render('html'))

    return apache.OK
