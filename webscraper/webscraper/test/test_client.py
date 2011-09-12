# -*- coding: utf-8 -*-

from webscraper import client

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
<<<<<<< HEAD

=======
  assert ( client.selector_to_xpath('a[target="pee"] foo.bar + hoge#piyo') ==
           '//a[@target="pee"]//foo[@class="bar"]/following-sibling::hoge[@id="piyo"]' )
    
>>>>>>> fc3e9c0cc97a2e7f56b4ced746a97daac120b922
