# -*- coding: utf-8 -*-

import py2ch

version = py2ch.__version__

# URLs and URL templates
bbsmenu         = r"http://menu.2ch.net/bbsmenu.html"
find2ch         = r"http://find.2ch.net/"
past_url_prefix = r"http://%(host)s/%(board)s/kako/"\
                  + "%(short_id)s/%(thread_id)s.html"
dat_url_prefix  = r'http://%(host)s/%(board)s/dat/%(thread_id)s.dat'

# HTTP setting
default_encode = r'shift_jis'
find2ch_encode = r'euc-jp'
user_agent_header = r'Monazilla/1.00 (py2ch/' + version + ')'
subject_file   = u'subject.txt'

