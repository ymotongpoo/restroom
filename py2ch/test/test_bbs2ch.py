# -*- coding: utf-8 -*-

import nose
from py2ch import BBS2ch
from py2ch import conf


def test___init__():
    b = BBS2ch(conf.bbsmenu)


if __name__ == '__main__':
    nose.run()
