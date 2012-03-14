# -*- coding: utf-8 -*-
#
# specification of 2ch dat
# http://info.2ch.net/wiki/index.php?monazilla%2Fdat%A4%CE%BB%C5%CD%CD
#

import re
import util


'''
グローバル変数
==============

_urlptn      : レス内のURL系パターン
_greedurlptn : レス内のURLパターン（より貪欲に探す）
_anchorptn   : アンカーへのリンク
_dateidptn   : 日付のパターン。datファイルによっては形式が異なるため
               外部から変更可能にしたい。
_abone       : 「あぼーん」の文字列
'''

_urlptn = re.compile(ur'h?ttps?\://[\w\.]+/?\S*',
                     re.UNICODE)

_greedurlptn = re.compile(ur'[a-zA-Z]+://[\w\.]+/?\S*',
                          re.UNICODE)

_anchorptn = re.compile(u'../test/read.cgi/[\w]+/\d+/(?P<num>\d+)',
                        re.UNICODE)

_dateidptn = re.compile(u'''
(?P<date>\d{4}/\d{2}/\d{2}                   # 日付
\((?:月|火|水|木|金|土|日)\)                 # 曜日
\ \d{2}:\d{2}:\d{2}(?:\.\d{2})?)             # スペース＋HH:MM:SS
(?:\ ID:(?P<id>[\w\+/]{7,10}))?              # スペース＋ID 英数字と/と+ 9桁
(?:\ BE:(?P<be>\d{8,10}\-[\w★]+\(\d+\)))?   # BE
''', re.VERBOSE | re.UNICODE)

_tripptn = re.compile(u'◆[\w\./]{8,12}')

_abone = u'あぼーん'


class Res(dict):
    '''
    レスを表すクラス
    '''
    def __init__(self, datline=None, num=0):
        '''
        datファイルの1行からレスを生成する
        '''
        self.num = num
        if datline.strip() != u'' :
            self.createRes(datline)
        else:
            self.name = u''
            self.mailto = u''
            self.date = u''
            self.resid = u''
            self.be = u''
            self.text = u''
            self.anchors = []
            self.urls = []
            self.trip = u''
            self.title = u''


    def createRes(self, datline):
        '''
        datファイルの1行からレスを作成

        datの仕様
        =========
        - 名前<>E-mail<>日付とIDとBE<>本文<>スレッドタイトル
        - 名前<>E-mail<>日付とIDとBE<>本文<>
        - 名 </b>fusianasan.2ch.net<b>前<>E-mail<>日付とIDとBE<>本文<>
        - 名前 </b>◆ozOtJW9BFA <b><>E-mail<>日付とIDとBE<>本文<>
        - キャップ ★<>E-mail<>日付とIDとBE<>本文<>
        - 名前 </b>◆ozOtJW9BFA <b>＠キャップ ★<>E-mail<>日付とIDとBE<>本文<>
        - あぼーん<>あぼーん<>あぼーん<>あぼーん<>あぼーん
        '''
        data = datline.split('<>')
        if len(data) > 3:
            self.name = data[0]
            self.mailto = data[1]
            self.date, self.resid, self.be = self._split_date_id_be(data[2])
            self.text = data[3]
            self.anchors = self._find_anchor(self.text)
            self.urls = self._find_url(self.text)
            self.trip = self._find_trip(self.name)
        else:
            raise ValueError, datline

        if self.num == 0:
            self.title = data[4]

    def _split_date_id_be(self, date_id_be):
        '''
        日付とIDとBEの部分を正規表現で抽出
        '''
        matched = _dateidptn.search(date_id_be)
        r = matched.groupdict()
        return r['date'], r['id'], r['be']


    def _find_anchor(self, text):
        '''
        テキスト内から安価を探す
        '''
        return _anchorptn.findall(text)

    def _find_url(self, text):
        '''
        テキスト内からURLを探す
        '''
        return _urlptn.findall(text)


    def _find_trip(self, text):
        '''
        テキスト内からトリップを探す
        '''
        r = _tripptn.findall(text)
        return r[0] if r else ''
