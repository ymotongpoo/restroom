# -*- coding: utf-8 -*-

import os.path
import re
from datetime import datetime

import util
from bbsres import Res

class Thread(object):
    '''
    スレッドを管理するクラス
    '''
    def __init__(self, datfile, title=u'', url=''):
        self.res = []
        self.title = title
        self.url = ''
        self.last_modified = ''
        self.total_size = -1
        if datfile:
            self.createThread(datfile, title, url)

    def createThread(self, datfile, title, url, offset=0):
        '''
        datファイルからスレッドを作成
        
        TODO: url は datファイルではなくhtmlへのリンクに？
        '''
        from httplib import HTTPMessage
        try:
            data, path_tokens, info = util.pathload(datfile)

            for i, d in enumerate(data):
                r = Res(d, i + offset)
            self.res.append(r)

            if isinstance(info, HTTPMessage):
                self.last_modified = info.dict.get('last-modified', '')
                size = int(info.dict.get('content-length', '0'))
                self.total_size = size
            
            if len(title.strip()) > 0:
                self.title = title
            else:
                self.title = self.res[0].title
            self.url = datfile

        except Exception, e:
            print e


    def findTripRes(self):
        '''
        トリップが付いているレスを確認。
        辞書のリストをattrに追加。
        [{<trip1>:[res[i], res[j], ...]},
         {<trip2>:[res[i], res[j], ...]},
         ...]
        '''
        pass


    def __len__(self):
        '''
        スレッドの長さ = レスの数
        '''
        return len(self.res)


    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, slice):
            return self.res[key]
        else:
            return self.__getattribute__(key)


    def __iter__(self):
        for r in self.res:
            yield r



