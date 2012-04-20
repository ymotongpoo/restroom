# -*- coding: utf-8 -*-

import zmq
from lxml import etree
from zmq.eventloop import ioloop

import time
import os
import functools
import urllib2
from StringIO import StringIO
import re
import sqlite3

# PyPI page related constants
PYPI_BASE_URL = "http://pypi.python.org%s"
pkg_list_url = PYPI_BASE_URL % r"/pypi?%3Aaction=index"
PKG_PATH = "//td/a"

# ZeroMQ setting
VENTILATOR_TARGET = "ipc://pypiv.ipc"
SINK_TARGET = "ipc://pypis.ipc"
INTERVAL = 0.1

# SQLite setting
SQLITE_STORE = "pypi.db"
INSERT_TEMPLATE = ("""insert into pypi values """ +
                   """(':name', ':version', ':url')""")

def init():
    if os.path.exists(SQLITE_STORE):
        os.remove(SQLITE_STORE)

    conn = sqlite3.connect(SQLITE_STORE)
    cur = conn.cursor()
    cur.execute( ("""create table pypi (""" +
                  """name text, version text, url text)""") )
    conn.commit()
    conn.close()


def ventilator():
    context = zmq.Context()
    ventilator = context.socket(zmq.PUSH)
    ventilator.bind(VENTILATOR_TARGET)

    fp = urllib2.urlopen(pkg_list_url)
    data = fp.read()
    tree = etree.parse(StringIO(data), etree.HTMLParser())
    pkgs = tree.xpath(PKG_PATH)

    time.sleep(1.0)

    for p in pkgs:
        url = PYPI_BASE_URL % p.attrib['href']
        print url
        ventilator.send(url)
    

def worker():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect(VENTILATOR_TARGET)

    sender = context.socket(zmq.PUSH)
    sender.connect(SINK_TARGET)

    callback = functools.partial(pkg_url_handler, sender)

    loop = ioloop.IOLoop.instance()
    loop.add_handler(receiver, callback, zmq.POLLIN)
    loop.start()


def sink():
    context = zmq.Context()
    sink = context.socket(zmq.PULL) 
    sink.bind(SINK_TARGET)

    conn = sqlite3.connect(SQLITE_STORE)
    cur = conn.cursor()

    def pull_handler(socket, events):
        message = socket.recv_pyobj()
        sql = INSERT_TEMPLATE % message
        print sql
        cur.execute(sql)

    def timeout_handler():
        conn.commit()
        conn.close

    loop = ioloop.IOLoop.instance()
    loop.add_handler(sink, pull_handler, zmq.POLLIN)
    loop.add_timeout(5.0, timeout_handler)
    loop.start()


def pkg_url_handler(sender, receiver, events):
    pkg_url = receiver.recv()
    p = urllib2.urlopen(pkg_url)
    data = p.read()

    pkginfo = parse_pkginfo(data)
    sender.send_pyobj(pkginfo)

def __parse_helper(li):
    strong = li.xpath('./strong')[0].text
    span = li.xpath('./span')[0].text

    strong.lower()[:-1]


def parse_pkginfo(source):
    tree = etree.parse(StringIO(source), etree.HTMLParser())

    # hard coding
    title_tag = tree.xpath("//title")[0].text.split()
    name = title_tag[:-1].join(' ')
    version = title_tag[-1]
    additional_path = "/pypi/%s/%s" % (name, version)
    url = PYPI_BASE_URL % additional_path
    
    ul = tree.xpath("//div[@id='content']/div[@class='section']/ul[@class='nodot']/li")
    for li in ul:
        
        
    
    return dict(name=name, version=version, url=url)


def main():
    from multiprocessing import cpu_count, Process, Pool
    max_process = 2 * cpu_count()

    sinkp = Process(target=sink)
    print "*** SINK START ***"
    sinkp.start()
    
    for i in range(max_process):
        workerp = Process(target=worker)
        print "*** WORKER %d START ***" % i
        workerp.start()
    
    ventilatorp = Process(target=ventilator)
    print "*** VENTILATOR START"
    ventilatorp.start()
    ventilatorp.join()
    
    sinkp.join()


if __name__ == '__main__':


    import argparse
    description = "PyPI data scraper"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('type', choices='vwsim')
    
    class Prog:
        """dummy class for namespace"""
        pass

    def exec_error():
        print "to see usage, type --help"

        
    prog = Prog()

    parser.parse_args(namespace=prog)
    process_type = {
        'v': ventilator,
        'w': worker,
        's': sink,
        'i': init,
        'm': main
        }

    process = process_type.get(prog.type, exec_error)
    process()
    
    
    
