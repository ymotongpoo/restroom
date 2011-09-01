#-*- encoding: utf-8 -*-

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2009/02/01 19:15:14$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import sqlite3

# create database
conn = sqlite3.connect('bookmark.db')
cur = conn.cursor()

cur.execute('create table ttag (id int, tag text)')
cur.execute('create table tbookmark (url text primary key, title text, user int, clip int, buzz int, hotpoint float, timestamp text)')
conn.commit()


taglist = [u'あとで読む', u'あとでよむ', u'後で読む', u'後でよむ', u'あとで',
           u'あとで見る', u'後で見る', u'後でみる', u'あとでみる', u'あと',
           u'いつか読む', u'いつか見る', u'later']

for t in enumerate(taglist):
    cur.execute('insert into ttag values (?, ?)', t)
conn.commit()

conn.close()
