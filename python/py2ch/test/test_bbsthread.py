# -*- coding: utf-8 -*-

import nose
from py2ch.bbsthread import Thread
import test_conf

class TestThread(object):
    def __init__(self):
        self.threads = []

    def test_createThread(self):
        for f in test_conf.dat_data:
            self.threads.append(Thread(f))

    def test___len__(self):
        for th in self.threads:
            assert len(th) == len(th.res)

    def test___getitem__(self):
        for th in self.threads:
            assert th['title'] == th.title
            assert th['url'] == th.url
            for i in range(0,len(th)):
                assert th[i] == th.res[i]

    def tearDown(self):
        print '********** result of createThread **********'
        print 'number of threads --> ' + str(len(self.threads))
        for i, r in enumerate(self.threads):
            print str(i) + ' -> ' + r.title



if __name__ == '__main__':
    nose.run()
