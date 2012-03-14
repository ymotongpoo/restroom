# -*- coding: utf-8 -*-

import os
import os.path

import py2ch

network = False

def source_list(urls):
    return urls if network else []

#---------------------------------------------------------------------
# スレッドdatファイル
#---------------------------------------------------------------------
_dat_urls  = [r'http://hibari.2ch.net/tech/dat/1235050215.dat',
              r'http://hibari.2ch.net/tech/dat/1288342460.dat']
dat_urls   = source_list(_dat_urls)

dat_dir   = os.path.join(os.path.dirname(__file__), './data/dat')
dat_files = [os.path.join(dat_dir, f) for f in os.listdir(dat_dir)]

dat_data  = dat_files + dat_urls


#---------------------------------------------------------------------
# Subject.txt
#---------------------------------------------------------------------
_subject_txt_urls = [r'http://hibari.2ch.net/tech/subject.txt',
                     r'http://toki.2ch.net/goods/subject.txt']
subject_txt_urls  = source_list(_subject_txt_urls)

#---------------------------------------------------------------------
# bbsmenu
#---------------------------------------------------------------------
_bbsmenu_urls  = [r'http://menu.2ch.net/bbsmenu.html']
bbsmenu_urls  = source_list(_bbsmenu_urls)
bbsmenu_dir   = os.path.join(os.path.dirname(__file__), 'data/menu')
bbsmenu_files = [os.path.join(bbsmenu_dir, f) for f in os.listdir(bbsmenu_dir)]

bbsmenu = bbsmenu_urls + bbsmenu_files
