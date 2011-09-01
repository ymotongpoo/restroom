#
# -*- coding: utf8 -*-;
#
# Twitter XML Logger in Python
#
# Yoshifumi YAMAGUCHI @ymotongpoo
#

__author__ = "ymotongpoo <ymotongpoo@gmail.com>"
__date__ = "$2010/09/20 22:43:10$"
__version__ = "$Revision: 0.10"
__credits__ = "0x7d8 -- programming training"

from time import sleep
import os
import urllib
import re
from StringIO import StringIO
from lxml import etree

xml_header = '<?xml version="1.0" encoding="UTF-8"?>'

twitter_api = 'http://api.twitter.com/1/statuses/user_timeline.xml?'

default_options = {'screen_name':'ymotongpoo',
                   'trim_user':'false',
                   'include_rts':'true',
                   'include_entities':'true',
                   'max_id':'9'*1,
                   'since_id':'0',
                   'count':'200',
                   }

interval = 25 # interval sec. for each HTTP request

def update_option(**options):
    """
    update GET options for Twitter API
    @param options dictionary of options
    """
    api_options = default_options

    for k,v in option.iteritems():
        if k in default_options:
            api_options[k] = v

    return api_options


def retreive_xml(**options):
    """
    retreive timeline in xml format via twitter api
    @param options dictionary of options
    """
    get_query = []
    for k, v in options.iteritems():
        get_query.append(k + '=' + v)

    url = twitter_api + '&'.join(get_query)
    p = urllib.urlopen(url)
    content = p.read()
    return content


def minimum_id(tweets):
    """
    find minimum id from xml
    @param tweets retreived xml
    """
    try:
        tree = etree.parse(StringIO(tweets), etree.XMLParser())
        statuses = tree.xpath('//statuses')
        id_str = statuses[0].xpath('./status/id/text()')
        ids = []
        for id in id_str:
            ids.append(int(id))
        return str(min(ids))

    except IndexError, e:
        raise e
    except ValueError, e:
        raise e


def maximum_id(tweets):
    """
    find maximum id from xml
    @param tweets retreived xml
    """
    try:
        tree = etree.parse(StringIO(tweets), etree.XMLParser())
        statuses = tree.xpath('//statuses')
        id_str = statuses[0].xpath('./status/id/text()')
        ids = []
        for id in id_str:
            ids.append(int(id))
        return str(max(ids))

    except IndexError, e:
        raise e
    except ValueError, e:
        raise e
    


def delete_first_line(string):
    """
    delete head line from assigned lines
    @param lines string
    """
    lines = string.split('\n')
    return '\n'.join(lines[1:])


def sort_status_by_id(statuses):
    """
    sort status by status id.
    @param statuses list of statuses (all <status> elements in <statuses> tag)
    """
    def status_cmp(x, y):
        return id(x.xpath('./id/text()')) - id(x.xpath('./id/text()'))

    st_list = statuses[0].xpath('./status')
    st_list.sort(status_cmp)
    return '\n'.join([st.tostring() for st in st_list])


def _past_retreiver(max_id):
    options = default_options
    if 'since_id' in options:
        del options['since_id']

    options['max_id'] = str(max_id)
    print options
    return retreive_xml(**options)


def _future_retreiver(since_id):
    options = default_options
    if 'max_id' in options:
        del options['max_id']

    options['since_id'] = str(since_id)
    return retreive_xml(**options)


def runner(id = -1, filename = 'twitter.log', direction = 'past'):
    """
    runner() retreives all tweets 
    """
    if os.path.isfile(filename):
        fp = open(filename, 'a+')
    else:
        fp = open(filename, 'w+')
        fp.write(xml_header)
        fp.close()
        fp = open(filename, 'a+')
    try:
        xml = 'initial string...'
        if id==-1:
            print '...done'
            return False
        else:
            print direction + " : " + str(id)
            if direction == 'past':
                xml = _past_retreiver(id)
            elif direction == 'future':
                xml = _future_retreiver(id)
            else:
                return id
            fp.write(xml)
            fp.close()

            min_id = minimum_id(xml)
            print 'minimum id : ' + min_id
            
            sleep(interval)
            print 'passing ' + str(int(min_id)-1)
            return int(min_id)-1

    # Exception is for "Twitter is over capacity"
    except IndexError, e:
        print xml + ' -> ' + str(e)
        fp.close()
        sleep(interval)
        return id
    
    except ValueError, e:
        print xml + ' -> ' + str(e)
        fp.close()
        sleep(interval)
        return False

    except Exception, e:
        print xml + ' -> ' + str(e)
        fp.close()
        sleep(interval)
        return id



if __name__ == '__main__':
    ret = 99999999999
    direction = 'past'
    while (ret != False):
        ret = runner(id = ret, direction = direction)
