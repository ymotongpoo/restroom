# -*- coding: utf-8 -*-

from urlparse import urlparse

board_menu_url = r"http://menu.2ch.net/bbsmenu.html"

class Menu(object):
  """
  url (str) : board list url
  file (str) : board list filename
  """
  url = board_menu_url
  def __init__(self, url=None, file=None):
    self.categories = []
    if url:
      self.url = url
    if file:
      self.file = file
  
  def __getitem__(self, key):
    if isinstance(key, int):
      return self.categories[key]
      
  def __repr__(self):
    ret = ""
    if self.file is None:
      ret = "Menu(%s, %s)" % (self.url, "None")
    else:
      ret = "Menu(%s, %s)" % (self.url, self.file)
    return ret
    
  def __unicode__(self):
    ret = u"[Menu URL] %s\n" % unicode(self.url)
    for c in self.categories:
      for l in c.__unicode__().split(u'\n'):
        ret += u'\t' + l + u'\n'
    return ret
    
  def append(self, category):
    if isinstance(category, Category):
      self.categories.append(category)
    else:
      raise MenuItemError, "Only Category instance can be appended"


class Category(list):
  def __init__(self, name):
    self.name = name
    self.boards = []

  def __getitem__(self, key):
    if isinstance(key, int):
      return self.boards[key]
    
  def __repr__(self):
    ret = "Category(%s)" % (self.name,)
    return ret
    
  def __unicode__(self):
    ret = u"[Category] %s\n" % self.name
    for b in self.boards:
      for l in b.__unicode__().split(u'\n'):
        ret += u'\t' + l + u'\n'
    return ret
  
  def append(self, board):
    if isinstance(board, Board):
      self.boards.append(board)
    else:
      raise CategoryItemError, "Only Board instance can be appended"


class Board(object):
  def __init__(self, uname, url):
    """
    uname : board name for human
    name : board name on server
    url : board url
    server : board server
    threads : threads stored on the server
    """
    self.uname = uname
    self.url  = url
    self.name = name
    self.server = None
    self.threads = {}
    parse_url(url)

  def parse_url(url):
    """
    Parse board url into server name and board name
    """
    o = urlparse(url)
    self.server = o.netloc
    self.name = o.path.split('/')[1]

  def __repr__(self):
    ret = "Board(%s, %s)" %  (self.uname, self.url)
    return ret
    
  def __unicode__(self):
    return u"[Board] %s (%s)" % (self.uname, unicode(self.url))
    
  def append(self, thread):
    if isinstance(thread, Thread):
      thread.bname = self.name
      thread.server = self.server
      self.threads[therad.id] = thread
    else:
      raise BoardItemError, "Only Thread instance can be appended"


class Thread(list):
  """
  id (str) : thread id 
  title (unicode) : thread title
  server (str) : server name
  bname (str) : parent board name on server (= Board.name)
  last_modified (str) : last-modified date on http header
  """
  def __init__(self, id, title, server, bname):
    self.id = id
    self.title = title
    self.server = server
    self.bname = bname
    self.res = []
    self.last_modified = None
    
  def __unicode__(self):
    return u"[Thread] %s (%s, %s)" % (self.title, self.id, self.server)

  def append(self, res):
    if isinstance(res, Res):
      if res.title:
        self.title = res.title
      
      res.index = len(self.res)
      self.res.append(res)
    else:
      raise ThreadItemError, "Only Res instance can be appended"


class Res(object):
  """
  index (int) : 
  """
  def __init__(self, index, id, name, date, be=None, title=None):
    self.index = index
    self.id = id
    self.name = name
    self.date = date
    self.comment = comment
    self.be = be
    self.title = title
