#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import re
from cmd import Cmd

from py2ch import BBS2ch
from py2ch import Board
from py2ch import Thread
from py2ch import Res

cui_welcome_banner = """\
********************************************
********** CUI client using py2ch **********
********************************************
         
    copyright Yoshifumi YAMAGUCHI, 2011

"""

cui_leave_banner = """\
exit ....
"""

help_thread_msg = """\
thread commands
  load <dat file/dat url>

  select
    - select loaded threads

  view <res range>
    - res range is assigned like these:
      thread view 10-100 (print #10 to #100)
      thread view -200   (print #1 to #200)
      thread view 500-   (print #500 until the end of the thread)

  reload
    - reload current thread
"""

class CuiBBSApp(Cmd):
    def __init__(self):
        self.__super = Cmd
        self.__super.__init__(self)
        self.prompt = 'py2ch >>>> '
        self.intro  = cui_welcome_banner

        # Thread settings
        self.curthread = None
        self.curidx = 0
        self.threads = []

    def postloop(self):
        print cui_leave_banner

    def emptyline(self):
        pass

    def help_help(self):
        print "type 'help <command>' to get each commands' help"


    def do_thread(self, s):
        l = s.split()
        if l[0] == 'load':
            th = Thread(l[1])
            self.curthread = th
            self.threads.append(th)
            return

        elif l[0] == 'view':
            for i, r in enumerate(self.curthread):
                p = PrettyRes(r)
                print p.prettyprint()
            return

        elif l[0] == 'select':
            for i, t in enumerate(self.threads):
                print '%s : %s' % (str(i), t.title)
            r = raw_input('which thread? : ')
            try:
                idx = int(r.strip())
                if isinstance(idx, int) and 0 <= idx < len(self.threads):
                    self.curthread = self.threads[idx]
                    print "now thread : '%s'" % self.curthread.title
                else:
                    print "%s is not number" % (r,)
                return

            except Exception, e:
                print e
                print r
                print "**** argument should be number"
                return

    def help_thread(self):
        print help_thread_msg


    def do_add(self, s):
        l = s.split()
        if len(l)!=2:
            print "*** invalid number of arguments"
            return
        try:
            l = [int(i) for i in l]
        except ValueError:
            print "*** arguments should be numbers"
            return
        print l[0]+l[1]



template = """
[%d] %s <%s> %s %s %s
%s 
"""
class PrettyRes(object):

    """
    Resを成形するクラス
    """
    def __init__(self, res):
        if isinstance(res, Res):
            self.res = res
        else:
            raise ValueError, "input variable must be Res class instance"

        self.escapechars = {u'<br>': u'\n',
                            u'<BR>': u'\n',
                            u'&gt;': u'>',
                            u'&lt;': u'<',
                            u'&nbsp;': u"　"}

    def prettyprint(self):
        prettyname = self.res.name
        prettytext = self.res.text
        for k, v in self.escapechars.iteritems():
            prettyname = string.replace(prettyname, k, v)
            prettytext = string.replace(prettytext, k, v)
            

        return template % (self.res.num, self.res.name, self.res.mailto,
                           self.res.date, self.res.resid, self.res.be,
                           prettytext)
        

if __name__ == '__main__':
    bbsapp = CuiBBSApp()
    bbsapp.cmdloop()

