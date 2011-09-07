# -*- coding: utf-8 -*-

from core import util
from StringIO import StringIO
import json
import cPickle
import os.path

config = util.parse_config()
data_dir = os.path.join(os.path.dirname(__file__), 'data')

default_board_menu_url = 'http://menu.2ch.net/bbsmenu.html'
default_board_tag = u'a'
default_category_tag = u'b'
default_category_xpath = u'//' + default_category_tag

def download_boardlist():
  try:
    from lxml import etree

    encoding = config['menu']['encoding']
    data = util.urlread(default_board_menu_url, config['headers'])
    content = unicode(data, encoding, 'strict')

    tree = etree.parse(StringIO(content), etree.HTMLParser())
    category_elems = tree.xpath(default_category_xpath)

    menu = []
    for c in category_elems:
      category = {}
      category['name'] = c.text
      category['board'] = []
      for e in c.itersiblings():
        if e.tag == default_board_tag:
          board = {}
          board['name'] = e.text
          board['url'] = e.attrib['href']
          category['board'].append(board)
        elif e.tag == default_category_tag:
          menu.append(category)
          break
    
    menu_file = os.path.join(data_dir, 'bbsmenu.txt')
    with open(menu_file, 'wb') as f:
      cPickle.dump(menu, f)

  except ImportError, e:
    if 'lxml' in e:
      "python2ch requires lxml"
    raise



if __name__ == '__main__':
  download_boardlist()
