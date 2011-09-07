# -*- coding: utf-8 -*-
"""
2chスレッドチェック用ライブラリ


http://www.monazilla.org/index.php?c=6-20

"""
from flask import Flask

import os.path
import urllib2
from StringIO import StringIO
import gzip

config = {'url_pattern': r'http://<server>/<board>/dat/<id>.dat',
          'encoding': 'Shift_JIS',
          'separator': '<>',
          'past_url_patterns': [r'http://<server>/<board>/kako/<id1>/<id2>/<id>.dat.gz',
                                r'http://<server>/<board>/kako/<id1>/<id>.dat.gz']}

"""ヘッダに関しては次のURLを確認。
追加取得をする場合gzipを付与してはいけないことを確認
http://www.monazilla.org/index.php?e=198
"""
httpheaders = {'User-Agent': 'Monazilla/1.00 (py2ch/0.10)',
               'Accept-Encoding': 'gzip',
               'Accept-Language': 'ja',
               'If-Modified-Since': None,
               'If-None-Match': None,
               'Range': None}


def get_root_path():
    try:
        directory = os.path.dirname(__file__)
        return os.path.abspath(directory)
    except AttributeError:

      return os.getcwd()


def urlread(url, headers):
  req = urllib2.Request(url, headers=headers)
  p = urllib2.urlopen(req)
  data = p.read()
  info = p.info()
  if p.info().get('Content-Encoding') in ('gzip', 'x-gzip'):
    s = StringIO(data)
    z = gzip.GzipFile('rb', fileobj=s)
    data = z.read()
  return (info, data)


class _MetaThreadManager(object):
  def __init__(self, url_pattern, encoding, separator, past_url_patterns):
    self.url_pattern = url_pattern
    self.encoding = encoding
    self.separator = separator
    self.past_url_patterns = past_url_patterns
    self.id = None


class ThreadManager(_MetaThreadManager):
  def __init__(self, config, httpheaders):
    url_pattern = config['url_pattern']
    encoding = config['encoding']
    separator = config['separator']
    past_url_patterns = config['past_url_patterns']
    _MetaThreadManager.__init__(self, url_pattern, encoding, 
                                separator, past_url_patterns)

    self.httpheaders = httpheaders
    self.threads = set()

  def register_threads(self, threads):
    for t in threads:
      self.threads.add(t)

  def fetch_thread_data(self, url):
    info, data = urlread(url, self.httpheaders)
    return info, data.decode(self.encoding, 'ignore')


if __name__ == '__main__':
  threads = ['http://kamome.2ch.net/traf/dat/1310723624.dat',
             'http://kamome.2ch.net/traf/dat/1313507415.dat',
             'http://yuzuru.2ch.net/ftax/dat/1223984982.dat',
             'http://yuzuru.2ch.net/ftax/dat/1196851586.dat']
  tm = ThreadManager(config, httpheaders)
  tm.register_threads(threads)

  for t in tm.threads:
    print "*"*10 + t
    info, data = tm.fetch_thread_data(t)
    print data

