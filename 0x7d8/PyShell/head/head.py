#!/usr/bin/env python
# -*- encoding: utf-8; coding : utf-8 -*-
"""
PyShell No.2  head

head.py is an linux comoand \"head\" like script implemented in Python.

Known issue:
    - readlines(size) doesn't work as expected.
      is this a build-in error?
"""

__author__ = "ymotongpoo <ymotongpoo@gmail.com>"
__date__   = "16 Nov. 2008"
__credits__ = "0x7d8 -- programming training"
__version__ = "$Revision: 0.10"


import sys
import getopt

argc = len(sys.argv)

def version_opt():
    print "head.py -- version 0.10"

def main():
    options = {}
    opts, prg_args = getopt.getopt(sys.argv[1:], 'qvc:n:',
                                   ['bytes=','lines=','quiet','silent','verbose','help','version'])

    for o, v in opts:
        options[o] = v


    if '-n' in options:
        line_num = int(options['-n'])
    elif '--lines' in options:
        line_num = int(options['--lines'])
    else:
        line_num = 10


    if '-c' in options:
        bytes = int(options['-c'])
    elif '--bytes' in options:
        bytes = int(options['--bytes'])
    else:
        bytes = -1

    for fn in prg_args:
        try:
            #
            # --- readlines([sizehint]) doesn't work as expected ---
            #
            #if bytes > 0:
            #    lines = open(fn).readlines(bytes)
            #else:
            #    lines = open(fn).readlines()
            #

            f = open(fn)
            if bytes > 0:
                data = f.read(bytes)
            else:
                data = f.read()
            lines = data.split('\n')

        except:
            print '\nskip file : ' + fn
            continue

        if '--verbose' in options \
               or (not '-q' in options and not '--quiet' in options and not '--silent' in options):
            print '==> ' + fn + ' <=='

        line_num = line_num if (line_num < len(lines)) else len(lines)
        for i in range(0, line_num):
            print lines[i]


if __name__ == '__main__':
    main()

