# -*- coding: utf-8 -*-

import urllib2
from StringIO import StringIO
import gzip

coding = "Shift_JIS"
headers = [('User-Agent', 'Monazilla/1.00 (Py2chProxy/1.00)'),
           ('Accept-Encoding', 'gzip')
          ]

def opener(path):
  req = urllib2.Request(path)
  req.add_headers = headers
  opener = urllib2.build_opener() # add hander here if necessary
  p = opener.open(req)
  if p.info().get("Content-Encoding") in ('gzip', 'x-gzip'):
    data = decoder(p.read())
  else:
    data = p.read()
  return data.decode(coding)

def decoder(gzipped):
  s = StringIO(gzipped.read())
  zipped = gzip.GzipFile('rb', fileobj=s)
  content = zipped.read()
  return content