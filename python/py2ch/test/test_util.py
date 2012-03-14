# -*- coding: utf-8 -*-

import nose
import py2ch
from py2ch import util
import test_conf


def test_pathload():
    for f in test_conf.dat_data:
        py2ch.util.pathload(f)


def test_pathjoin():
    for d in test_conf.dat_data:
        data, path_tokens, info = py2ch.util.pathload(d)
        print d + ' -> ' + py2ch.util.pathjoin(path_tokens)
        if path_tokens.scheme == 'http':
            assert py2ch.util.pathjoin(path_tokens) == d
        elif path_tokens.scheme == 'file':
            assert py2ch.util.pathjoin(path_tokens) == ("file://" + d)
        
        
def test_menuload():
    print test_conf.bbsmenu
    for path in test_conf.bbsmenu:
        data, path_tokens, info = util.menuload(path)
        print data

def test_searchThread():
    query = [[u'テスト'],
             [u'python', u'ruby']
             ]
    
    for l in query:
        print util.searchThread(l)

if __name__ == '__main__':
    nose.main()
