# -*- coding: utf-8 -*-
# Copyright (c) 2011 Yoshifumi YAMAGUCHI. See COPYING for details.
"""
py2ch is Python library for operating 2ch BBS.
Mainly for browsing 2ch.
"""

try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)


version_info = (0, 0, 3)
try:
    __version__ = __import__('pkg_resources') \
        .get_distribution('py2ch').version
except Exception:
    __version__ = 'unknown'
__changeset__ = '1508:dc09399c94d4'


# import modules
import conf
import util
from bbsres import Res
from bbsthread import Thread
from bbsboard import Board
from bbsboard import Category
from bbs2ch import BBS2ch


__all__ = ['conf', 'util', 'Res', 'Thread', 'Board', 'Category', 'BBS2ch']

