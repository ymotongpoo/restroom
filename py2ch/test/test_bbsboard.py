# -*- coding: utf-8 -*-

import nose
import test_conf
from py2ch import Board

def test___init__():
    for l in test_conf.subject_txt_urls:
        b = Board(l)
        for th in b.threads:
            print th['title'] + ' -> ' + th['url']


if __name__ == '__main__':
    nose.main()
