#-*- encoding: utf-8 -*-;
__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2009/02/02 22:43:10$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import urllib
import re
import time
import sys
import getopt
from StringIO import StringIO
from lxml import etree

MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

YEAR = range(2005, 2010)
view_url_r = re.compile('^view_diary.pl\?id=[0-9]+&owner_id=[0-9]+$')

ROOT_URL = 'http://mixi.jp/'
MONTH_PAGE_URL = 'http://mixi.jp/list_diary.pl'

class MixiExtractor(urllib.FancyURLopener):
    mixicodec = 'utf-8'
    
    def login(self, email, password):
        LOGIN_URL = 'http://mixi.jp/login.pl'
        params = urllib.urlencode({
            'email': email,
            'password': password,
            'next_url': 'home.pl'})

        r = self.open(LOGIN_URL, params)
        cookie = []
        for c in r.headers.getheaders('Set-Cookie'):
            m = re.match('(.+=.+);.*', c)
            if m:
                cookie.append(m.groups()[0])

        self.addheader('Cookie', ';'.join(cookie))
        r = self.open('http://mixi.jp/check.pl?n=home.pl')
        return r.read()


    def getMonthEntryUrls(self, year, month):
        urls = []
        i = 1
        while 1:
            params = urllib.urlencode({
                'year': year,
                'month': month,
                'page': i})

            r = self.open(MONTH_PAGE_URL, params)
            data = r.read()
            tree = etree.parse(StringIO(data), etree.HTMLParser())
            whole_urls = [u.attrib['href'].strip() for u in \
                          tree.xpath('//div[@class="listDiaryTitle"]//a')]

            page_urls = []
            for u in whole_urls:
                if view_url_r.match(u):
                    page_urls.append(u)

            if not len(page_urls):
                break
            else:
                urls += page_urls
                i += 1


        return map(lambda u:ROOT_URL+u, urls)

    def getMonthEntryBody(self, entryurls, comment):
        def extractCommentContents(node):
            cdate = ''.join(node.xpath('.//span[@class="commentTitleDate"]/text()'))
            cuser = ''.join(node.xpath('.//span[@class="commentTitleName"]//a/text()'))
            cbody = '\n'.join(node.xpath('.//dd/text()'))
            return dict(cdate=cdate.decode(self.mixicodec), \
                        cuser=cuser.decode(self.mixicodec), \
                        cbody=cbody.decode(self.mixicodec))
            
        def extractEntryContents(node, comment):
            print 'extracting ...'
            date = ''.join(node.xpath('.//div[@class="listDiaryTitle"]//dd/text()'))
            title = ''.join(node.xpath('.//div[@class="listDiaryTitle"]//dt/text()'))
            body = '\n'.join(node.xpath('.//div[@id="diary_body"]/text()'))

            if comment:
                cnodes = node.xpath('//div[@class="diaryCommentbox" or @class="diaryCommentboxLast"]')
                comments = [extractCommentContents(c) for c in cnodes]
                return dict(date=date.decode(self.mixicodec), \
                            title=title.decode(self.mixicodec), \
                            body=body.decode(self.mixicodec), \
                            comments=comments)
            else:
                return dict(date=date.decode(self.mixicodec), \
                            title=title.decode(self.mixicodec), \
                            body=body.decode(self.mixicodec))

        entries = []

        for u in entryurls:
            print u
            r = self.open(u)
            data = r.read()
            tree = etree.parse(StringIO(data), etree.HTMLParser())
            entry = [extractEntryContents(e, comment) \
                     for e in tree.xpath('//div[@class="viewDiaryBox"]')]
            for e in entry:
                entries.append(e)

            print '-'*8, 'waiting next entry...'
            time.sleep(5)

        return entries


def downloadMixiEntries(username, password, comment):
    me = MixiExtractor()
    me.login(username, password)
    for y in YEAR:
        for m, mon in enumerate(MONTH):
            urls = me.getMonthEntryUrls(y, m+1)

            entries = me.getMonthEntryBody(urls, comment)

            filename = str(y) + str(m+1).zfill(2) + '.txt'
            fp = open(filename, 'w')

            for e in entries:
                fp.write('='*10 + '\n')
                fp.write(e['date'].encode(me.mixicodec) + '\n■' +  \
                         e['title'].encode(me.mixicodec) + '\n' + \
                         e['body'].encode(me.mixicodec) + '\n')
                if 'comments' in e:
                    for c in e['comments']:
                        fp.write('-'*5 + '\n')
                        fp.write(c['cuser'].encode(me.mixicodec) + '\t' + \
                                 c['cdate'].encode(me.mixicodec) + '\n' + \
                                 c['cbody'].encode(me.mixicodec) + '\n')

            print '-'*8, 'waiting next month...'
            time.sleep(10)

            fp.close()

def usage():
    print 'python mixi_download.py -u [USERNAME] -p [PASSWORD]'


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    try:
        opts, opt_args = getopt.getopt(argvs[1:], "u:p:c")
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    userinfo = {}
    for o, v in opts:
        userinfo[o] = v

    print userinfo

    if '-c' not in  userinfo:
        userinfo['-c'] = False
    else:
        userinfo['-c'] = True

    downloadMixiEntries(userinfo['-u'], userinfo['-p'], userinfo['-c'])


