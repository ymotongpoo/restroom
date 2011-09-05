# -*- coding: utf-8 -*-

import ConfigParser
import urllib2
from StringIO import StringIO
import gzip
import json
import os.path

data_dir = os.path.join(os.path.dirname(__file__), '../data')
config_file = os.path.join(data_dir, 'config.ini')
thread_list_file = os.path.join(data_dir, 'thread.json')

def urlread(url, headers):
  req = urllib2.Request(url, headers=headers)
  p = urllib2.urlopen(req)
  data = p.read()
  if p.info().get("Content-Encoding") in ('gzip', 'x-gzip'):
    s = StringIO(data)
    zipped = gzip.GzipFile('rb', fileobj=s)
    data = zipped.read()
  return data

  
def parse_config(config_file=config_file):
  config = ConfigParser.SafeConfigParser()
  with open(config_file, 'rb') as cf:
    config.readfp(cf)
    
    headers = dict( config.items('Header'))
    menu    = dict( config.items('Menu') )
    board   = dict( config.items('Board') )
    thread  = dict( config.items('Thread') )

    return dict(headers=headers,
                menu=menu, 
                board=board, 
                thread=thread)


def parse_thread_list(thread_list_file=thread_list_file):
  with open(thread_list_file, 'rb') as f:
    threads = json.loads(f.read())
    print threads


if __name__ == '__main__':
  print parse_thread_list()
