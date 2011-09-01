# -*- coding: utf-8 -*-
#
# 2chへのアクセスに関して
#   http://info.2ch.net/wiki/index.php?monazilla/develop/access
#
# 
# http://www.pxsta.net/blog/?p=231
#

import urllib
import urllib2
import os.path
import urlparse
from urlparse import ParseResult
import re

import conf
import exception


def pathload(path, data=None, last_modified=None, byte=None):
    """
    pathを読み込む。
    
    last_modified, byteが指定されたときは追加分のみをロードする。
    206 : Parcial Content
      - このときはContent-Rangeで取得時の最大値が分かる
      - 当然Content-Lengthは取得したデータサイズ
    304 : Not Modified
    """
    try:
        if os.path.isfile(path):
            path_tokens = urlparse.urlparse(path, 'file')
            opener = urllib2.build_opener(urllib2.FileHandler)
            path = urlparse.urlunparse(path_tokens)
            fp = opener.open(path)
        else:
            last_modified = last_modified
            path_tokens = urlparse.urlparse(path)
            req = urllib2.Request(path)
            req.add_header('User-Agent', conf.user_agent_header)
            req.add_header('Accept-Encoding', 'gzip')
            if last_modified:
                req.add_header('If-Modified-Since', last_modified)
            if byte:
                req.add_header('Range', 'bytes=%s-' % byte)
            if data:
                fp = urllib2.urlopen(req, data)
            else:
                fp = urllib2.urlopen(req)

        data = fp.read().strip()
        info = fp.info()
        fp.close()
        return (data.decode(conf.default_encode, 'ignore').splitlines(),
                path_tokens,
                info)

    except IOError, e:
        raise e
    except urllib2.HTTPError, e:
        raise e.code
    except urllib2.URLError, e:
        raise e
    


def pathjoin(path_tokens):
    '''
    pathloadで返されるpath_tokensを結合して正しいURLまたはファイルパスを返す

    '''
    if isinstance(path_tokens, ParseResult):
        path = urlparse.urlunparse(path_tokens)
    else:
        raise Exception, 'failed!!'  # replace me
    return path


def boardload(path):
    '''
    板を読み込むための関数
    '''
    try:
        data, path_tokens, info = pathload(path)

        if isinstance(path_tokens, ParseResult):
            file = path_tokens.path.split('/')[-1]
        elif len(path_tokens) == 2:
            file = path_tokens[-1]
        else:
            raise ValueError, path_tokens

        if file == conf.subject_file:
            data, path_tokens, info = pathload(path)
            return data, path_tokens, info
        else:
            raise exception.BoardNotFoundException, path_tokens[1]

    except Exception, e:
        raise e
            
    
def menuload(path):
    """
    TODO: 「ずっと人大杉」の対応
    """
    try:
        data, path_tokens, info = pathload(path)
        
        if not (isinstance(path_tokens, ParseResult) or len(path_tokens) == 2):
            raise ValueError, path_tokens

        return data, path_tokens, info

    except Exception, e:
        raise e
            

_find2ch_ptn = re.compile(ur"""
<dt><a\ href="                                                          
(?P<url>https?://[\w\.]+/test/read\.cgi/\w+/\d{9,10}/\d{1,3}\-\d{1,3})  # URL
">
(?P<title>.+?)  # スレッドタイトル
</a>
""", re.VERBOSE)

def searchThread(query, page=0):
    """
    find.2ch.netによるスレッド検索
    query : 検索クエリのリスト（Unicode）
    page  : カウント50毎のオフセット
    
    スレッドURLとスレッドタイトルのタプルのリストを返す
    """
    try:
        query_str = ' '.join([q.encode(conf.find2ch_encode) for q in query])
        query_dict = dict(STR=query_str,
                          OFFSET=str(50*page),
                          TYPE='TITLE',
                          BBS='ALL',
                          COUNT='50')
        params = urllib.urlencode(query_dict)
        data = urllib.urlopen(conf.find2ch + '?' + params)
        
        result = []
        for l in data.readlines():
            match = _find2ch_ptn.search(l.decode(conf.find2ch_encode, 
                                                 'ignore'))
            if match:
                d = match.groupdict()
                result.append( (d['url'], d['title']) )
                
        return result
        
    except Exception, e:
        raise e
