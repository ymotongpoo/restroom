# -*- coding: utf-8 -*-


from py2ch import BBS2ch
from py2ch import conf




if __name__ == '__main__':

    print conf.bbsmenu

    bbs = BBS2ch(conf.bbsmenu)
    print '**** start ****'
    print len(bbs.categories)
    for c in bbs.categories:
        print c.name
        for b in c:
            print '   ' + b.title
