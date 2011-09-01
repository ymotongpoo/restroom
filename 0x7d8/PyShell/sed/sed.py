#!/usr/bin/python
# -*- encoding: euc-jp; coding : euc-jp -*-
"""
PyShell No.1  sed

sed.py is an linux comoand \"sed\" like script implemented in Python.
this script mainly focused on just replacing
strings using regular expressions.

Known issue:
    - always act with 'g' option without it.
    - any commands but for 's' and 'g' do not work
"""

__author__ = "ymotongpoo <ymotongpoo@gmail.com>"
__date__   = "13 Nov. 2008"
__credits__ = "0x7d8 -- programming training"
__version__ = "$Revision: 0.10"

import sys
import os
import re
import getopt

argvs = sys.argv
argc = len(argvs)

def usage(opt_args=''):
    print "usage : ./sed.py [-e script] [-f script_file] ... [file ...]"

####################################
# functions for -e style command
####################################
def find_separator(query):
    """
    find separator '/' which is not escaped
    """
    i = 0
    if query == []:
        print 'none'
        return
    else:
        try:
            i = query.index('/')
        except ValueError:
            return

        if query[i-1] != '\\':
            yield i
        for index in find_separator(query[i+1:]):
            yield index + i + 1


def parse_query(query):
    """
    parse command like s/foo/bar/g into tuple
    """
    index = []
    for i in find_separator(query):
        index.append(i)

    if len(index) == 3:
        command = query[:index[0]]
        target  = query[index[0]+1:index[1]]
        replace = query[index[1]+1:index[2]]
        flag    = query[index[2]+1:]
        return (command, target, replace, flag)
    else:
        print "ignore this option -- " + query
        sys.exit(1)


####################################
# functions for options
####################################
def expression_opt(opt_arg):
    """
    function for '-e' option.
    just parse command query.
    """
    return parse_query(opt_arg)


def file_opt(opt_arg):
    """
    function for '-f' option
    read files and pick up and parse commands
    """
    queries = []

    try:
        lines = open(opt_arg).readlines()
        for l in lines:
            queries.append(parse_query(l))

    except IOError:
        print "file not found"
        sys.exit(1)

    return queries


def version_opt(opt_arg=''):
    """
    show version infomation
    """
    print "sed.py -- version 0.10"
    sys.exit()


def suffix_opt(opt_arg=''):
    """
    return suffix for backup file
    """
    suffix = ''
    if len(opt_arg) != 0:
        suffix = '.' + opt_arg
    return suffix


####################################
# process for each command in -e
####################################
def s_command(command, line):
    """
    function for 's/foo/bar/' command
    in this version, it's not dependent on 'g' command
    """
    return re.sub(command[1], command[2], line)

def y_command(command, line):
    """
    function for 'y///' command
    """
    if len(command[1]) != len(command[2]):
        print "transform string are not the same length"
        sys.exit(1)
    elif len(command[3]) != 0:
        print "extra text at the end of a transform command"
        sys.exit(1)
    else:
        for i in len(command[1]):
            line = re.sub(command[1][i], command[2][i], line)
        return line


# options
options = {'-e' : expression_opt,
           '-f' : file_opt,
           '-V' : version_opt,
           '-i' : suffix_opt,
           '-h' : usage,
           '--help' : usage
           }

#
#
#
#
def main():
    if argc < 2:
        sys.exit()
    else:
        try:
            opts, opt_args = getopt.getopt(argvs[1:], "Vhni:e:f:",
                                           ["version", "help", "quiet", "suffix=", "expression=", "file="])
        except getopt.GetoptError:
            usage()
            sys.exit(2)

        # get options
        queries = {}
        for o, v in opts:
            if o == '-e' or o == '-f':
                if not o in queries:
                    queries[o] = []
                queries[o].append(options[o](v))
            else:
                queries[o] = options[o](v)

        for target_file in opt_args:
            try:
                lines = open(target_file).readlines()

            except IOError, e:
                print e
                print "skip file -> " + target_file
                continue

            replace_queries = []
            # put together options
            for c in ['-e', '-f']:
                if queries.has_key(c):
                    for q in queries[c]:
                        replace_queries.append(q)

            f = False
            if queries.has_key('-i'):
                f = open(target_file + queries['-i'], 'w')
            for line in lines:
                for q in replace_queries:
                    if q[0] == 's':
                        line = s_command(q, line)
                    elif q[0] == 'y':
                        line = y_command(q, line)

                print line,
                if f:
                    f.write(line)
            f.close()


if __name__ == '__main__':
    main()
else:
    sys.exit(1)
