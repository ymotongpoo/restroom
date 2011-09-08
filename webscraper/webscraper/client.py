# -*- coding: utf-8 -*-
import urllib2
import gzip
from StringIO import StringIO

def urlread(url, headers={}, encoding=None, range=None,
            last_modified=None, last_etag=None):
  try:
    if range:
      headers['Range'] = 'bytes= %s-' % str(range)
    if last_modified:
      haeders['If-Modified-Since'] = last_modified
    if last_etag:
      headers['If-None-Match'] = last_etag
      
    req = urllib2.Request(url, headers)
    p = urllib2.urlopen(req)
    data = p.read()
    headers = p.info().dict
    if p.info().get('Content-Encoding') in ('gzip', 'x-gzip'):
      z = gzip.GzipFile('rb', fileobj=StringIO(data))
      data = z.read()
      size = len(data)
    else:
      size = headers['content-length']

    return data, headers, size

  except urllib2.URLError:
    raise
    
      

