# -*- coding: utf-8 -*-
import urllib2
import gzip
from StringIO import StringIO
import re

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
  """
  @param url: URL
  @type  url: string
  @param headers: HTTP headers
  @type  headers: dict
  @param encoding: expecting encoding of fetched data
  @type  encoding: str
  @param last_modified: date info which is available from Last-Modified header
  @type  last_modified: str
  @param last_etag: tag from ETag header
  @type  last_etag: str
  """
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

  @param source: HTML/XML source
  @type  source: str or StringIO
  @param type: 'html' or 'xml'
  @type  type: str
  @return: root node of HTML/XML tree
  @rtype: lxml.etree or xml.etree.ElementTree
  """
  if not type:
    header = source.strip().split('\n')[0]
    if 'xml' in header.lower():
      parser = xmlparser
    else:
      parser = httpparser

  tree = etree.parse(source, parser)
  return tree

xpath_decendent_axis = '//'
xpath_child_axis = '/'
xpath_sibling_axis = '/following-sibling::'
selector_separators = ['>', ',', '+'] # do not supporting ','
selector_pred = re.compile('(?P<tag>[a-zA-Z]+)' +                  # tag
                           '\[(?P<attr>[a-zA-Z]+)' +               # attribute
                           '((?P<contain>~?)="(?P<value>.+)")?\]') # filter
xpath_attr_only = '%(tag)s[@%(attr)s]'
xpath_with_value = '%(tag)s[@%(attr)s="%(value)s"]'
xpath_contain = '%(tag)s[contain(./@%(attr)s,"%(value)s")]'

def selector_to_xpath(selector):
  """convert CSS selector to XPath. 

  @param selector: CSS selector string
  @type  selector: str
  @return XPath which correspond to assigned CSS selector
  @rtype str
  """
  selectors = selector.split()
  paths = []
  for s in selectors:
    if s in selector_separators:
      paths.append(s)
    else:
      paths.append(convert_to_xpath(s))

  xpath = xpath_decendent_axis
  decendents = []
  for p in paths:
    if p == '>':
      xpath += xpath_decendent_axis.join(decendents)
      xpath += xpath_child_axis
      decendents = []
    elif p == '+':
      xpath += xpath_decendent_axis.join(decendents)
      xpath += xpath_sibling_axis
      decendents = []
    else:
      decendents.append(p)
  xpath += xpath_decendent_axis.join(decendents)
  return xpath

  
def convert_to_xpath(selector):
  """convert a CSS selector token to a XPath piece

  @param selector: CSS selector string
  @type  selector: str
  @return: XPath which correspond to assigned CSS selector
  @rtype str
  """
  try:
    xpath = ""
    m = selector_pred.match(selector) 
    if m:
      matched = m.groupdict()
      if matched['value'] is None:
        return xpath_attr_only % matched
      elif matched['contain'] == '':
        return xpath_with_value % matched
      else:
        return xpath_contain % matched

    if selector.find('#') == -1 and selector.find('.') == -1:
      xpath = selector
    else:
      if '.' in selector:
        tag, attr = selector.split('.')
        xpath = '%s[@class="%s"]' % (tag, attr)
      elif '#' in selector:
        tag, attr = selector.split('#')
        xpath = '%s[@id="%s"]' % (tag, attr)
    return xpath
  except ValueError, e:
    raise ValueError, "Check if CSS selector is correct: %s" % dom
