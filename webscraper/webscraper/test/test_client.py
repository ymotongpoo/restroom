# -*- coding: utf-8 -*-

from webscraper import client

def test_convert_to_xpath():
  assert client.convert_to_xpath("a") == 'a'
  assert client.convert_to_xpath("foo.bar") == 'foo[@class="bar"]'
  assert client.convert_to_xpath("foo#bar") == 'foo[@id="bar"]'


def test_selector_to_xpath():
  assert ( client.selector_to_xpath('a > foo.bar > hoge#piyo') == 
           '//a/foo[@class="bar"]/hoge[@id="piyo"]' )
  assert ( client.selector_to_xpath('a foo.bar hoge#piyo') == 
           '//a//foo[@class="bar"]//hoge[@id="piyo"]' )
  assert ( client.selector_to_xpath('a + foo.bar + hoge#piyo') ==
           '//a/following-sibling::foo[@class="bar"]/following-sibling::hoge[@id="piyo"]' )
    
