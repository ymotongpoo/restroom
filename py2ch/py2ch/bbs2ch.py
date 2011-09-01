# -*- coding: utf-8 -*-

import re
import util
import conf
from py2ch import Board
from py2ch import Category

_board_url_ptn = re.compile(u'''
<A\ HREF=(?P<board_url>https?://[\S\.\-]+/(?:[\S\-\._/]+)*)    # 板のURL
(?:\ TARGET=_blank)?>                                          # TARGET=_blank
(?P<board_name>[\S\ \.-=]+)                                    # 板の名前
</A>(?:<br>|<BR>)?
''', re.VERBOSE | re.UNICODE)

_category_ptn = re.compile(u'<BR><BR><B>(?P<cat_name>[\S\ ]+)</B><BR>',
                           re.UNICODE)


class BBS2ch(object):
    '''
    板一覧を管理するクラス
    '''
    def __init__(self, menu_url=r''):
        self.menu_url=menu_url
        self.categories = []
        self.create2ch(self.menu_url)
        
    def create2ch(self, menu_url):
        data, path_tokens, info = util.menuload(menu_url)
        self._menu_scraper(data)
        
    def _menu_scraper(self, menuhtml_lines):
        '''
        bbsmenu.htmlの1行からカテゴリ名と板情報を取得する
        '''
        from urllib2 import HTTPError
        c = None
        for l in menuhtml_lines:
            try:
                if l.strip() != '':
                    if isinstance(c, Category):
                        matched = _board_url_ptn.search(l)
                        if matched:
                            d = matched.groupdict()
                            b = Board(d['board_url'] + conf.subject_file, 
                                      d['board_name'])
                            c.boards.append(b)
                    else:
                        matched = _category_ptn.search(l)
                        if matched:
                            d = matched.groupdict()
                            c = Category(d['cat_name'])
                
                # 空行でカテゴリが切り替わる
                elif c is not None:
                    self.categories.append(c)
                    c = None

            except HTTPError, e:
                if d:
                    print '%s --> %s' % (e, d['board_url'])
                continue
            
            except Exception, e:
                print 'some error -> %s' % (e,)
                continue
