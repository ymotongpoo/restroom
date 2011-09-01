# -*- encoding: utf-8 -*-;
"""
main.py

usage : main.py GoogleAccount GooglePassword
"""

__author__ = "ymotongpoo <ymotongpoo@gmail.com>"
__date__   = "21 Nov. 2008"
__credits__ = "0x7d8 -- programming training"
__version__ = "$Revision: 0.10"

from feed import Feed
from mailto import MailTo
import sys

urllist = ['http://d.hatena.ne.jp/ymotongpoo/rss',
           'http://ws.audioscrobbler.com/1.0/user/ymotongpoo/recenttracks.rss']

f = Feed(urllist=urllist)
f.GetFeed()
body = f.MailBodyText()
m = MailTo('ymotongpoo@gmail.com', 'ymotongpoo+test@gmail.com', 'Test', body)
msg = m.CreateMessage('utf-8')
m.SendViaGmail(msg, sys.argv[1], sys.argv[2])

