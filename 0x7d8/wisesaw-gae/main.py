# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template, util
from google.appengine.api import urlfetch

from HTMLParser import HTMLParser, HTMLParseError

import oauth
import tokens

import random

WISE_SAW_URL = 'http://www.meigensyu.com/quotations/view/random'
UPDATE_URL = 'http://api.twitter.com/1/statuses/update.json'

class ExtractWiseSaw(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.codec = 'utf-8'

    self.wise_saw = u''
    self.author = u''
    self.url = u''

    self._in_text = False
    self._in_link = False
    self._in_authority = False
    self._data_count = 0

  def handle_starttag(self, tag, attrs):
    attrs = dict(attrs)
    if 'div' == tag and 'class' in attrs:
      if 'text' == attrs['class']:
        self._in_text = True
      elif 'link' == attrs['class']:
        self._in_link = True

    if 'a' == tag and not self._in_link and self._data_count == 1:
      self._in_authority = True

  def handle_endtag(self, tag):
    if 'div' == tag and self._in_text:
      self._in_text = False
    if 'div' == tag:
      self._data_count = 0

  def handle_data(self, data):
    if self._in_text:
      self.wise_saw += data.decode(self.codec)

    if self._in_link:
      self.author = data.decode(self.codec)
      self._data_count += 1
      self._in_link = False

    if self._in_authority:
      self.author += data.decode(self.codec) + ' '
      self._in_authority = False


class MainHandler(webapp.RequestHandler):

  def get(self):
    #url = WISE_SAW_URL % random.randint(min_idx, max_idx)
    url = WISE_SAW_URL
    result = urlfetch.fetch(url)
    
    data = result.content

    # extract text and author from HTML
    parser = ExtractWiseSaw()
    parser.feed(data)
    parser.close()
    wise_saw = parser.wise_saw.encode(parser.codec)
    author = parser.author.encode(parser.codec)
    author = author.strip()
      
    description = '%s [%s]' % (wise_saw, author)
    param = {'status': description}

    client = oauth.TwitterClient(tokens.CONSUMER_KEY,
                                 tokens.CONSUMER_SECRET, None)

    if len(wise_saw) > 0 and len(author) > 0:
      client.make_request(
        UPDATE_URL,
        token=tokens.ACCESS_TOKEN,
        secret=tokens.ACCESS_TOKEN_SECRET,
        additional_params=param,
        protected=True,
        method='POST'
        )

      self.response.out.write(wise_saw + ' : ' + author)

    else:
      self.response.out.write('wisesaw failed -> ' + wise_saw + ' : ' + author)


def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)
  


if __name__ == '__main__':
  main()
