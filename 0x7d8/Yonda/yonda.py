# -*- encoding: utf-8 -*-

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/12/10 00:29:41$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"


from mod_python import apache
import sqlite3
import os
from genshi.template import TemplateLoader

BASEPATH = os.path.dirname(__file__)
DBPATH = os.path.join(BASEPATH, 'bookmark.db')
TEMPLATEPATH = os.path.join(BASEPATH, 'yonda.tpl')

conn = sqlite3.connect(DBPATH)
cur = conn.cursor()

# popular entry
cur.execute('select url, title, user+clip+buzz as point from tbookmark order by point desc limit 10')
bookmarks = []
for row in cur:
    bookmarks.append(dict(url=row[0], title=row[1]))

# hot entry
cur.execute('select url, title from tbookmark order by hotpoint desc limit 10')
hotentry = []
for row in cur:
    hotentry.append(dict(url=row[0], title=row[1]))

loader = TemplateLoader([BASEPATH])
tmpl = loader.load(TEMPLATEPATH)
stream = tmpl.generate(bookmarks=bookmarks, hotentry=hotentry)

conn.close()

def handler(req):
    req.content_type = 'text/html'
    req.send_http_header()
    req.write(stream.render('html'))
    return apache.OK

