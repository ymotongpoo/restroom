# -*- coding: utf-8 -*-

import nose
from py2ch import util
from py2ch import Res
import test_conf

def test___init__():
    for f in test_conf.dat_data:
        print '*'*20 + f + '*'*20
        lines, path_tokens, info = util.pathload(f)
        for l in lines:
            r = Res(l)
            if len(r.urls) > 0:
                print r.urls[0]


if __name__ == '__main__':
    nose.main()
