# -8- coding: utf-8 -*-

import re
from urlparse import urljoin

import util

_titleptn = re.compile(ur'''
(?P<dat>\d+\.(?:dat|cgi))      # datファイル名
(?:(?:<>)|,)                   # 区切り文字(<>または,)
(?P<title>.+)                  # タイトル
\((?P<num>\d{1,4})\)           # レス数
''', re.VERBOSE | re.UNICODE)

class Board(object):
    '''
    板を管理するクラス
    '''
    def __init__(self, board_url=None, title=u''):
        self.threads = []
        self.title = title
        if board_url:
            self.createBoard(board_url, title)

    def createBoard(self, board_file, title):
        '''
        スレッド一覧ファイルからスレッドリストを作成するクラス

        subject.txtの1行からスレッド情報を取得
        http://info.2ch.net/wiki/index.php?monazilla%2Fdevelop%2Fsubject.txt

        subject.txtの仕様
        =================
        0000000000.dat<>スレッドタイトル (レス数)

        - threads[n]['title'] : スレッドタイトル
        - threads[n]['url']   : http://server/board/dat/0000000000.dat
        '''
        data, path_tokens, info = util.boardload(board_file)
        if title:
            self.title = title

        for l in data:
            matched = _titleptn.search(l)
            if matched:
                r = matched.groupdict()
                subject_url = util.pathjoin(path_tokens)
                datfile = urljoin(subject_url, 'dat/' + r['dat'])
                thread = dict(title = r['title'],
                              url   = datfile)
            else:
                print 'no match --> ' + l

            self.threads.append(thread)



class Category(object):
    '''
    カテゴリを管理するクラス
    name : カテゴリ名
    boards : カテゴリに所属する板のリストw
    '''
    def __init__(self, name):
        self.name = name
        self.boards = []

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.boards[key]
        else:
            return self.__getattribute__(key)
        
