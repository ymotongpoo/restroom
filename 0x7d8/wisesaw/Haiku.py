# -*- encoding: utf-8 -*-
"""
Haiku.py

Based on Twitter API
    (Japanese) http://watcher.moe-nifty.com/memo/docs/twitterAPI13.txt
    (Original) http://apiwiki.twitter.com/REST+API+Documentation
"""

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/11/22 09:57:30$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import urllib
import urllib2

FORMAT = set(['xml', 'rss', 'json', 'atom'])
default_format = 'json'

class Twitter:
    def __init__(self, username, password, base_url='', proxy_host='', proxy_port=''):
        self.username = username
        self.password = password
        self.base_url = base_url if len(base_url) > 0 else 'http://twitter.com/'
        
        if len(proxy_host) > 0 and type(proxy) is IntType:
            self.proxies = {'http': proxy_host + ':' + proxy_port}
        else:
            self.proxies = {}

    def __create_opener(self):
        if 'http' in self.proxies:
            proxy_handler = urllib2.ProxyHandler(self.proxies)
            auth_handler = urllib2.ProxyBasicAuthHandler()
        else:
            auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password('Twitter API', self.base_url, self.username, self.password)

        if 'http' in self.proxies:
            opener = urllib2.build_opener(proxy_handler, auth_handler)
        else:
            opener = urllib2.build_opener(auth_handler)
        return opener

    def __add_format(self, url, format):
        if format in FORMAT:
            url = url + '.' + format
        else:
            url = url + '.' + default_format
        return url

    def __open_url_in_get(self, url, get_dict={}):
        opener = self.__create_opener()
        urllib2.install_opener(opener)
        if len(get_dict) > 0:
            params = urllib.urlencode(get_dict)
            f = urllib2.urlopen(url + '?' + params)
        else:
            f = urllib2.urlopen(url)
        return f.read()

    def __open_url_in_post(self, url, post_dict={}):
        opener = self.__create_opener()
        urllib2.install_opener(opener)
        if len(post_dict) > 0:
            params = urllib.urlencode(post_dict)
            f = urllib2.urlopen(url, params)
            return f.read()
        else:
            return

    def __query_dict_generator(self, func_args):
        get_dict = {}
        if 'since_id' in func_args and func_args['since_id'] > 0 and type(func_args['since_id']) is int:
            get_dict['since_id'] = func_args['since_id']
        if 'twitterid' in func_args and len(func_args['twitterid']) > 0:
            get_dict['id'] = func_args['twitterid']
        if 'since' in func_args and len(func_args['since']) > 0:
            get_dict['since'] = func_args['since']
        if 'page' in func_args and func_args['page'] > 0 and type(func_args['page']) is int:
            get_dict['page'] = func_args['page']
        if 'lite' in func_args and not func_args['lite']:
            get_dict['lite'] = 'true'
        return get_dict    

    def __get_request_without_options(self, url_part, format):
        url = self.base_url + url_part
        url = self.__add_format(url, format)
        d = self.__open_url_in_get(url)
        return d

    def __get_request_with_options(self, url_part, format, dict):
        url = self.base_url + url_part
        url = self.__add_format(url, format)
        get_dict = self.__query_dict_generator(dict)
        d = self.__open_url_in_get(url, get_dict)
        return d

    def publicTimeline(self, since_id=-1, format=default_format):
        return self.__get_request_with_options('statuses/public_timeline', format, locals())

    def friendsTimeline(self, twitterid='', since='', page=1, format=default_format):
        """
        since -- expects same type as the return of strftime()
        """
        url_part = 'statuses/friends_timeline'
        if len(twitterid) > 0:
            url_part = url_part + '/' + twitterid
        return self.__get_request_with_options(url_part, format, locals())

    def userTimeline(self, twitterid='', count=20, since='', since_id='', page=1, format=default_format):
        """
        since -- expects same type as the return of strftime()
        """
        url_part = 'statuses/user_timeline'
        if len(twitterid) > 0:
            url_part = url_part + '/' + twitterid            
        return self.__get_request_with_options(url_part, format, locals())
        

    def showStatusByID(self, status_id, format=default_format):
        if type(status_id) is int:
            status_id = str(status_id)
        return self.__get_request_without_options('statuses/show/' + status_id, format)

    def updateStatus(self, status, source='', format=default_format):
        url = self.base_url + 'statuses/update'
        url = self.__add_format(url, format)
        post_dict = {}
        if len(status) <= 160:
            post_dict['status'] = status
        if len(source) > 0:
            post_dict['source'] = source
        d = self.__open_url_in_post(url, post_dict)
        return d

    def repliesPost(self, since='', since_id='', page=1, format=default_format):
        return self.__get_request_with_options('statuses/replies', format, locals())

    def destroyPost(self, status_id, format=default_format):
        return self.__get_request_without_options('statuses/destroy/' + status_id, format)

    def friendsList(self, twitterid='', page=1, lite=False, since='', format=default_format):
        return self.__get_request_with_options('statuses/friends', format, locals())

    def followersList(self, twitterid='', page=1, lite=False, format=default_format):
        return self.__get_request_with_options('statuses/followers', format, locals())

    def featured(self, format=default_format):
        return self.__get_request_without_options('statuses/featured', format)

    def showUserInfo(self, twitterid, email='', format=default_format):
        url = self.base_url + 'users/show'
        get_dict = {}
        if 'email' in locals():
            url = self.__add_format(url, format)
            get_dict['email'] = email
        else:
            url = url + '/' + twitterid
            url = self.__add_format(url, format)

        for k, v in self.__query_dict_generator(locals()): 
            get_dict[k] = v
        d = self.__open_url_in_get(url, get_dict)
        return d

    def directMsgs(self, since='', since_id='', page=1, format=default_format):
        return self.__get_request_with_options('direct_messages', format, locals())

    def sentMsgs(self, since='', since_id='', page=1, format=default_format):
        return self.__get_request_with_options('direct_messages/sent', format, locals())
    
    def sendNewDirectMsg(self, user, text, format=default_format):
        if len(user) > 0 and len(text) > 0:
            url = self.base_url + 'direct_messages/new'
            url = self.__add_format(url, format)
            post_dict = self.__query_dict_generator(locals())
            d = self.__open_url_in_post(url, post_dict)
            return d
        else:
            sys.exit(0)
    
    def destroyDirectMsg(self, msgid, format=default_format):
        if type(msgid) is int:
            url = self.base_url + 'direct_messages/destroy/'
            url = self.__add_format(url, format)
            get_dict['id'] = msgid
            d = self.__open_url_in_get(url, get_dict)
            return d
        else:
            return
    
    def createFriend(self, twitterid, format=default_format):
        return self.__get_request_without_options('friendships/create/' + twitterid, format)

    def destroyFriend(self, twitterid, format=default_format):
        return self.__get_request_without_options('friendships/destroy/' + twitterid, format)

    def existsRelationship(self, user_a, user_b, format=default_format):
        url = self.base_url + 'friendships/exists'
        url = self.__add_format(url, format)
        get_dict = {}
        get_dict['user_a'] = user_a
        get_dict['user_b'] = user_b
        d = self.__open_url_in_get(url, get_dict)
        return d
           
    def verifyCredentials(self, format=default_format):
        url = self.base_url + 'account/verify_credentials'
        url = self.__add_format(url, format)
        d = self.__open_url_in_get(url)
        return d

    def endSession(self):
        url = self.base_url + 'account/end_session'
        d = self.__open_url_in_get(url)
        return d

    # *** 'archive' was no longer available ***
    #
    # def archivePost(self, page=1, since='', since_id='', format=default_format):
    #    return self.__get_request_with_options('account/archive', format, locals())

    def updateLocation(self, location, format=default_format):
        url = self.base_url + 'account/update_location'
        url = self.__add_format(url, format)
        get_dict = {}
        get_dict['location'] = location
        d = self.__open_url_in_get(url, get_dict)
        return d

    def updateDeliveryDevice(self, device, format=default_format):
        devices = set(['sms', 'im', 'none'])
        url = self.base_url + 'account/update_delivery_device'
        url = self.__add_format(url, format)
        post_dict = self.__query_dict_generator(locals())
        d = self.__open_url_in_post(url, post_dict)
        return d

    def rateLimitStatus(self, format=default_format):
        return self.__get_request_without_options('account/rate_limit_status', format)

    def favoritesPost(self, twitterid='', page=1, format=default_format):
        return self.__get_request_with_options('favorites', format, locals())

    def createFavorite(self, twitterid, format=default_format):
        return self.__get_request_without_options('favourings/create/' + twitterid, format)

    def destroyFavorite(self, twitterid, format=default_format):
        return self.__get_request_without_options('favourings/destory/' + twitterid, format)

    def followIM(self, twitterid, format=default_format):
        return self.__get_request_without_options('notifications/follow/' + twitterid, format)

    def leaveIM(self, twitterid, format=default_format):
        return self.__get_request_without_options('notifications/leave/' + twitterid, format)

    def createBlock(self, twitterid, format=default_format):
        return self.__get_request_without_options('blocks/create/' + twitterid, format)

    def destoryBlock(self, twitterid, format=default_format):
        return self.__get_request_without_options('blocks/destroy/' + twitterid, format)

    def testConnection(self, format=default_format):
        return self.__get_request_without_options('help/test', format)

    def downtimeSchedule(self, format=default_format):
        return self.__get_request_without_options('help/downtime_schedule', format)

    def updateProfileColors(self, bg='', txt='', link='', sbfill='', sbbdr='', format=default_format):
        url = self.base_url + 'account/update_profile_colors'
        url = self.__add_format(url, format)
        post_dict = {}
        if len(bg) > 0:
            post_dict['profile_background_color'] = bg
        if len(txt) > 0:
            post_dict['profile_text_color'] = txt
        if len(link) > 0:
            post_dict['profile_link_color'] = link
        if len(sbfill) > 0:
            post_dict['profile_sidebar_fill_color'] = sbfill
        if len(sbbdr) > 0:
            post_dict['profile_sidebar_border_color'] = sbbdr
            
        d = self.__open_url_in_post(url, post_dict)
        return d

    def updateProfileBackgroundImage(self, image='', format=default_format):
        url = self.base_url + 'account/update_profile_background_image'
        url = self.__add_format(url, format)
        post_dict = self.__query_dict_generator(locals())
        d = self.__open_url_in_post(url, post_dict)
        return d
