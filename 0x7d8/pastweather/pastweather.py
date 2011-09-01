#-*- encoding:utf-8 -*-

import urllib
import simplejson
import types


class SearchTwitter:
    base_url = u'http://search.twitter.com/'
    coding = 'utf-8'
    format = u'json'

    def __init__(self):
        pass

    def search(self, word):
        search_url = self.base_url + 'search.' + self.format

        try:
            if word == None or type(word) != types.UnicodeType:
                raise TypeError, 'Type of argument is not "unicode" : type -> %s' % type(word)
            try:
                getdict = dict(q=word.decode('utf-8'), rpp=10)
                getdict = urllib.urlencode(getdict)
                url = search_url + '?' + getdict
                print url
                fp = urllib.urlopen(url)
                data = fp.read()

                return data
            except:
                raise
        except:
            raise



class WeatherData:
    base_url = u'http://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php'
    coding = 'shift_jis'
    
    prec_no = 0
    

    def __init__(self):
        pass



class PastWeather:
    placeheader = u'L:'
    def __init__(self):
        self.st = SearchTwitter()

    def searchPlace(self, word):
        try:
            ret = self.st.search(word)
            data = simplejson.loads(ret)
            for d in data['results']:
                start = d['text'].find(self.placeheader.decode(self.st.coding))
                if start > 0:
                    print d['text'][start + len(self.placeheader):].split()[0]
        except:
            raise

def main():
    pw = PastWeather()
    pw.searchPlace(u'ｲﾏｺｺ')

if __name__ == '__main__':
    main()
