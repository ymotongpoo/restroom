# -*- coding: utf-8 -*-

from webscraper import client

import os.path
from cStringIO import StringIO

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def test_convert_to_xpath():
  assert client.convert_to_xpath('a') == 'a'
  assert client.convert_to_xpath('foo.bar') == 'foo[@class="bar"]'
  assert client.convert_to_xpath('foo#bar') == 'foo[@id="bar"]'
  assert client.convert_to_xpath('a[target]') == 'a[@target]'
  assert client.convert_to_xpath('a[target="hoge"]') == 'a[@target="hoge"]'
  assert client.convert_to_xpath('a[target~="hoge"]') == 'a[contain(./@target,"hoge")]'


def test_selector_to_xpath():
  assert ( client.selector_to_xpath('a > foo.bar > hoge#piyo') == 
           '//a/foo[@class="bar"]/hoge[@id="piyo"]' )
  assert ( client.selector_to_xpath('a foo.bar hoge#piyo') == 
           '//a//foo[@class="bar"]//hoge[@id="piyo"]' )
  assert ( client.selector_to_xpath('a + foo.bar + hoge#piyo') ==
           '//a/following-sibling::foo[@class="bar"]/following-sibling::hoge[@id="piyo"]' )
  assert ( client.selector_to_xpath('a[target="pee"] foo.bar + hoge#piyo') ==
           '//a[@target="pee"]//foo[@class="bar"]/following-sibling::hoge[@id="piyo"]' )

def test_parse():
  test1 = os.path.join(data_dir, 'test1.html')
  try:
    from lxml import etree

    with open(test1, 'rb') as f:
      data = f.read()
      source = client.parse(StringIO(data), 'html')
      target = etree.parse(StringIO(data), etree.HTMLParser())
      assert ( etree.tostring(source) == etree.tostring(target) )
  
  except ImportError:
    print "no test"


