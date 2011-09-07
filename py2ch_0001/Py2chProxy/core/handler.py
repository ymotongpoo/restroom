# -*- coding: utf-8 -*-

from data import *
import util
from StringIO import StringIO
from lxml import etree

thread_url_tmpl = r"http://%(server)s/%(board)s/subject.txt"
category_xpath = u'//b'

def __parse_and_create_menu(menu, content):
  tree = etree.parse(StringIO(content), etree.HTMLParser())
  for c in tree.xpath(category_xpath):
    category = Category(unicode(c.text))
    for e in c.itersiblings():
      if e.tag == u'a':
        url = str(e.attrib[u'href'])
        name = unicode(e.text)
        board = Board(name, url)
        category.append(board)
      elif e.tag == u'b':
        menu.append(category)
        break

def fetch_board_menu_from_url(menu):
  data = util.opener(menu.url)
  __parse_and_create_menu(menu, data)

def fetch_board_menu():
  menu = Menu()
  fetch_board_menu_from_url(menu=menu)
  return menu

def fetch_thread_from_url(thread):
  

if __name__ == "__main__":
  data = fetch_board_menu()
  print data.__unicode__().encode('utf-8')
