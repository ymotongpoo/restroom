# -*- coding: utf-8 -*-
import urllib2
import gzip
from StringIO import StringIO

try:
  from lxml import etree
  htmlparser = etree.HTMLParser()
  xmlparser = etree.XMLParser()
  xmllib = 'lxml'
except ImportError:
  from xml.etree import ElementTree as etree
  htmlparser = etree.HTMLParser()
  xmlparser = xml.parse.expat.ParserCreate()
  xmllib = 'standard'


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
    
      

def parse(source, type=None):
  """parse HTML/XML source and returns element tree

  :param: source : HTML/XML source
  :param: type : 'html' or 'xml'
  """
  if not type:
    header = source.strip().split('\n')[0]
    if 'xml' in header.lower():
      parser = xmlparser
    else:
      parser = httpparser

  tree = etree.parse(source, parser)
  return tree
  

def jquery_to_xpath(jquery):
  """convert jQuery (CSS) style dom to XPath
  """
  paths = [convert_to_xapth(dom) for dom in jquery.split()]
  print '//'.join(paths)

  
def convert_to_xpath(dom):
  try:
    xpath = ""
    if dom == dom.split('.#'):
      xpath = dom
    else:
      if '.' in dom:
        tag, attr = dom.split('.')
        xpath = "%s[@class=%s]" % (tag, attr)
      elif '#' in dom:
        tag, attr = dom.split('#')
        xpath = "%s[@id=%s]" % (tag, attr)
    return xpath
  except ValueError, e:
    raise ValueError, "Check if jQuery string is correct: %s" % dom
