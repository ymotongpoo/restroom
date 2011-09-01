# -*- coding: utf-8 -*-;
#
# atnd2gcal.py  ---  extract event data from ATND and book them into Google Calendar
#
# external packages
#   - gdata-python-client
#   - simplejson (for Python 2.5 or earlier)
#
# API reference
# 1. ATND API
#   http://api.atnd.org
#
# 2. Google Calendar API
#   http://code.google.com/intl/ja-JP/apis/calendar/data/1.0/developers_guide_python.html
#
#
# KNOWN BUGS
# I suppose this code is basically without bug but gdata-python-client and ATND API
# includes some critical bugs in some points:
#   1. if you delete event manually from Web UI, GData search API finds deleted event
#      and this script execute update process but the result is that nothing happens,
#      i.e. no events will be created
#   2. ATND API doesn't reply some event with using 'ym' option
#


__author__  = 'ymotongpoo <ymotongpoo AT gmail DOT com>'
__version__ = '0.3.0'
__date__    = '2009/11/10 (Tue)'

# for Web service
import urllib
import string

# for ATND API
try:
    import simplejson as json
except ImportError:
    import json

# for Google Calendar
try:
    from xml.etree import ElementTree
except ImportError:
    from elementtree import ElementTree
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import random
import time
from datetime import date, timedelta


ATND_URL='http://api.atnd.org/events/?format=json&user_id=%s&ym=%s&count=50'
ENCODING='utf-8'
DECODING='utf-8'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+09:00'

SOURCE = 'ATND2GCAL'
USERNAME = 'default'
VISIBILITY = 'private'
PROJECTION = 'full'


def extract_events(atnd_id, ym_list):
    ym_str = ','.join(ym_list)
    url = ATND_URL % (atnd_id, ym_str)
    p = urllib.urlopen(url)
    data = json.loads(p.read())
    return data['events']



class GcalOperator:
    def __init__(self, email, password):
        self.calendar_service = gdata.calendar.service.CalendarService()
        self.calendar_service.email = email
        self.calendar_service.password = password
        self.calendar_service.source = SOURCE
        self.calendar_service.ProgrammaticLogin()

        self.request_feed = gdata.calendar.CalendarEventFeed()

    def __setEventData(self, event, title, content, where, start_time, end_time):
        event.title = atom.Title(text=title)
        event.content = atom.Content(text=content)
        if where is None or len(where) == 0:
            where = 'TBD'
        event.where.append(gdata.calendar.Where(value_string=where))

        if start_time is None:
            # Use current time for the start_time and have the event last 1 hour
            start_time = time.strftime(TIME_FORMAT, time.gmtime())
        if end_time is None:
            start_ptime = time.strptime(start_time, TIME_FORMAT)
            end_time = time.strftime(TIME_FORMAT,
                                     time.localtime(time.mktime(start_ptime) + 3600))
        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
        return event


    def InsertEvent(self, title, content, where, start_time=None, end_time=None):
        event = gdata.calendar.CalendarEventEntry()
        event = self.__setEventData(event, title, content, where, start_time, end_time)
        event.batch_id = gdata.BatchId(text='insert'+str(random.uniform(0,10)))

        self.request_feed.AddInsert(entry=event)


    def UpdateEvent(self, event, title, content, where, start_time=None, end_time=None):
        event = self.__setEventData(event, title, content, where, start_time, end_time)
        event.batch_id = gdata.BatchId(text='update'+str(random.uniform(0,10)))
        print event.updated

        self.request_feed.AddUpdate(entry=event)


    def getOneEvent(self, date, title):
        query = gdata.calendar.service.CalendarEventQuery(USERNAME, VISIBILITY, PROJECTION)
        query['q'] = title.encode(ENCODING)
        query['start_min'] = date
        query['start_max'] = date
        query['max-results'] = '1'

        feed = self.calendar_service.CalendarQuery(query)

        if len(feed.entry) > 0:
            return feed.entry[0]
        else:
            return None


    def ExecuteBatch(self):
        if self.request_feed:
            response_feed = self.calendar_service.ExecuteBatch(self.request_feed,
                                                  gdata.calendar.service.DEFAULT_BATCH_URL)
        else:
            raise RequestFeedNoneException

        return response_feed



def process(email, password, atnd_id, ym_list):
    gcal = GcalOperator(email, password)

    events = extract_events(atnd_id, ym_list)
    for e in events:
        event_data = dict(title=e[u'title'],
                          content=e[u'url'],
                          where=e[u'place'],
                          start_time=e[u'started_at'],
                          end_time=e[u'ended_at'])

        date = e[u'started_at'].split('T')[0]
        title = e[u'title']
        event = gcal.getOneEvent(date, title)
        if not event:
            gcal.InsertEvent(**event_data)
        else:
            #print 'Event "' + e[u'title'] + '" is updating'
            event_data['event'] = event
            gcal.UpdateEvent(**event_data)

    response_feed = gcal.ExecuteBatch()

    for entry in response_feed.entry:
        if entry.batch_status:
            print 'status: %s' % (entry.batch_status.code,)
            print 'reason: %s' % (entry.batch_status.reason,)
            print 'batch id: %s' % (entry.batch_id.text,)



def usage():
    print 'usage : python atnd2gcal.py -e <email address> -p <password> -a <atnd_id>'



"""
 
  main process

"""
if __name__=='__main__':
    try:
        if len(sys.argv) < 2:
            usage()
            sys.exit()
        else:
            try:
                opts, opt_args = getopt.getopt(sys.argv[1:], 'he:p:a:')
                                               
            except getopt.GetoptError:
                usage()
                sys.exit(2)
                
            for o, v in opts:
                if o == '-e':
                    email = v
                elif o == '-p':
                    password = v
                elif o == '-a':
                    atnd_id = v

            t = date.today()
            ym_list = []
            for i in range(0, 3):
                ym_list.append((t + timedelta(days=30*i)).strftime('%Y%m'))
            process(email, password, atnd_id, ym_list)

    except Exception, e:
        print 'error -> ' + str(e).encode(ENCODING)
