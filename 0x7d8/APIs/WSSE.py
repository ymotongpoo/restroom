# -*- encoding: utf-8 -*-
"""
WSSE.py

WSSEAtomClinet:
    http://d.hatena.ne.jp/keyword/%A4%CF%A4%C6%A4%CA%A5%D5%A5%A9%A5%C8%A5%E9%A5%A4%A5%D5AtomAPI?kid=88110
    http://d.hatena.ne.jp/kenkitii/20060429/p1

Known issue:
    - getUpdate()
      'uri' elements cannot be get
"""

__author__="ymotongpoo <ymotongpoo@gmail.com>"
__date__ ="$2008/11/27 09:44:52$"
__version__="$Revision: 0.10"
__credits__="0x7d8 -- programming training"

import random, datetime, time
import base64, sha
import urllib,httplib
from xml.dom import minidom


class WSSEAtomClient:
    """
    class for WSSE authorized Atom Client
    """
    def __init__(self, userid='', password=''):
        """
        initialize class

        arguments:
            userid : user id for web service
            password : password for web service
        """
        self.userid = userid
        self.password = password
        self.useragent = 'WSSEAtomClient'
        self.wsse = None


    def createHeaderToken(self):
        """
        create header informations for WSSE authorization.
        this is used for X-WSSE property in HTTP request
        """
        nonce = sha.sha(str(time.time() + random.random())).digest()
        nonce64 = base64.encodestring(nonce).strip()

        created = datetime.datetime.now().isoformat() + 'Z'

        passdigest = sha.sha(nonce + created + self.password).digest()
        pass64 = base64.encodestring(passdigest).strip()

        wsse = 'UsernameToken Username="%(u)s", PasswordDigest="%(p)s", Nonce="%(n)s", Created="%(c)s"'
        value = dict(u = self.userid, p = pass64, n = nonce64, c = created)

        self.wsse = wsse % value


    def atomRequest(self, method, endpoint, body, content_type):
        """
        send HTTP request using WSSE header information

        arguments:
            method : method type of HTTP request (GET/POST/PUT/DELETE)
            endpoint : URL of service end point
            body : body of HTTP request
            content_type : content type of HTTP request like 'text/html'

        returns:
            dictionary of HTTP status, reason of the status and HTTP body
        """
        header_info = {'X-WSSE': self.wsse,
                       'Content-Type': content_type,
                       'Authorization': 'WSSE profile="UsernameToken"',
                       'User-Agent': self.useragent}

        conninfo = urllib.splittype(endpoint)
        conntypeinfo = conninfo[0]
        connhostinfo = urllib.splithost(conninfo[1])

        conn = httplib.HTTPConnection(connhostinfo[0])
        conn.request(method, connhostinfo[1], body, header_info)
        r = conn.getresponse()
        if not r.status in [200, 201]:
            print r.status, r.reason
            raise Exception('login failure')
        response = dict(status = r.status,
                        reason = r.reason,
                        data = r.read())
        conn.close()
        return response


    def getCollection(self, data):
        """
        get service URL from HTTP response

        arguments:
            data : HTTP body

        returns:
            list of URL and title of each web service
        """
        element_hierarchy = ['workspace', 'collection']
        doc = minidom.parseString(data.lstrip()).getElementsByTagName('workspace').item(0)

        service = []
        for n in doc.getElementsByTagName('collection'):
            url = n.getAttribute('href')
            title = n.getElementsByTagName('atom:title').item(0).childNodes[0].data
            service.append(
                dict(url = url,
                     title = title)
                )

        return service



class MixiClient(WSSEAtomClient):
    """
    class for mixi API (unofficial)
    """
    mixi_codec = 'utf-8'
    def __init__(self, userid, password):
        """
        arguments:
            userid : user id for mixi (i.e. email address)
            password : password for mixi
        """
        WSSEAtomClient.__init__(self, userid, password)


    def __getService(self, endpoint, body='', content_type='text/xml'):
        """
        send HTTP reqest using GET method with WSSE header

        arguments:
            endpoint : service endpoint
            body : body for HTTP request
            content_type : content type of HTTP
        """
        self.createHeaderToken()
        r = self.atomRequest('GET', endpoint, body, content_type)
        return r


    def __postService(self, endpoint, body, content_type='text/xml'):
        """
        send HTTP reqest using POSt method with WSSE header

        arguments:
            endpoint : service endpoint
            body : body for HTTP request
            content_type : content type of HTTP

        returns:
            HTTP response
        """
        self.createHeaderToken()
        r = self.atomRequest('POST', endpoint, body, content_type)
        return r


    def __createSenderXML(self, elem_dict):
        """
        create XML body for HTTP request

        arguments:
            elem_dict : dictionary for XML elements.
                        key are element names.
                        values are contents of elements.

        returns:
            XML string for HTTP request
        """
        impl = minidom.getDOMImplementation()
        doc = impl.createDocument(None, 'entry', None)

        header = doc.documentElement
        header.attributes['xmlns'] = 'http://www.w3.org/2005/Atom'
        header.attributes['xmlns:app'] = 'http://www.w3.org/2005/app#'

        for k, v in elem_dict.iteritems():
            elem = doc.createElement(k)
            elem.appendChild(doc.createTextNode(v))
            header.appendChild(elem)

        body = doc.toxml()
        doc.unlink()

        return body


    def getTracks(self):
        """
        get lataset foot stamps

        returns:
            dictionary of lastest foot stamps.
            name -- user name
            link -- url of each user
            updated -- time stamp of foot stamp
        """
        d = self.__getService('http://mixi.jp/atom/tracks')
        service = self.getCollection(d['data'])[0]['url']

        d = self.atomRequest('GET',service,'','')
        doc = minidom.parseString(d['data'].lstrip())

        tracks = []
        for n in doc.getElementsByTagName('entry'):
            link = n.getElementsByTagName('link').item(0).getAttribute('href')
            person = n.getElementsByTagName('author').item(0)
            name = person.getElementsByTagName('name').item(0).childNodes[0].data
            updated = n.getElementsByTagName('updated').item(0).childNodes[0].data

            tracks.append(
                dict(name = name.decode(self.mixi_codec),
                     link = link,
                     updated = updated)
                )

        return tracks


    def getNotify(self):
        """
        get notifies

        returns:
            dicionary of latest notifies.
            title -- title of notify
            link -- link for the notify
            updated -- time stamp of notify
        """
        d = self.__getService('http://mixi.jp/atom/notify')
        service = self.getCollection(d['data'])[0]['url']

        d = self.__getService(service)
        doc = minidom.parseString(d['data'].lstrip())

        notify = []
        for n in doc.getElementsByTagName('entry'):
            link = n.getElementsByTagName('link').item(0).getAttribute('href')
            title = n.getElementsByTagName('title').item(0).childNodes[0].data
            updated = n.getElementsByTagName('updated').item(0).childNodes[0].data

            notify.append(
                dict(title = title.decode(self.mixi_codec),
                     link = link,
                     updated = updated)
                )

        return notify


    def getFriends(self):
        """
        get my mixi friends list

        returns:
            dictionary of friends list
            name : name of friend
            link : url of each friend profile
            updated : last login
            group : list of assigned group
        """
        d = self.__getService('http://mixi.jp/atom/friends')
        service = self.getCollection(d['data'])[0]['url']

        d = self.__getService(service)
        doc = minidom.parseString(d['data'].lstrip())

        friends = []
        for n in doc.getElementsByTagName('entry'):
            link = n.getElementsByTagName('link').item(0).getAttribute('href')
            name = n.getElementsByTagName('title').item(0).childNodes[0].data
            updated = n.getElementsByTagName('updated').item(0).childNodes[0].data

            group = []
            for item in n.getElementsByTagName('category'):
                label = item.getAttribute('label')
                group.append(label.dncode(self.mixi_codec))

            friends.append(
                dict(name = name.dncode(self.mixi_codec),
                     link = link,
                     updated = updated,
                     group = group)
                )
        return friends


    def getUpdates(self):
        """
        something is wrong with 'uri' element.

        returns:
            dictionary of activity updates of friends
            name -- name of friends
            title -- activity content
            link -- link for activity
            updated -- time stamp of activity
            label -- category of activity
        """
        d = self.__getService('http://mixi.jp/atom/updates')
        service = self.getCollection(d['data'])[0]['url']

        d = self.__getService(service)
        doc = minidom.parseString(d['data'].lstrip())

        updates = []
        for n in doc.getElementsByTagName('entry'):
            link = n.getElementsByTagName('link').item(0).getAttribute('href')
            title = n.getElementsByTagName('title').item(0).childNodes[0].data
            updated = n.getElementsByTagName('updated').item(0).childNodes[0].data
            label = n.getElementsByTagName('category').item(0).getAttribute('label')
            author = n.getElementsByTagName('author').item(0)
            name = author.getElementsByTagName('name').item(0).childNodes.item(0).data
            #uri = author.getElementsByTagName('uri').item(0).childNodes.item(0).data

            updates.append(
                dict(name = name,
                     #uri = uri,
                     title = title.decode(self.mixi_codec),
                     link = link,
                     updated = updated,
                     label = label.decode(self.mixi_codec))
                )
        return updates


    def getPhotoService(self):
        """
        returns:
            HTTP response of photo album list
        """
        d = self.__getService('http://photo.mixi.jp/atom/r=3')
        service = self.getCollection(d['data'])
        return service


    def createAlbum(self, title, summary):
        """
        create brand new photo album

        arguments:
            title : title of photo album
            summary : summary of photo album

        returns:
            edit URL of created photo album
        """
        for s in self.getPhotoService():
            if s['title'] == 'photo album':
                url = s['url']

        elem_dict = dict(title = title.encode(self.mixi_codec),
                         summary = summary.encode(self.mixi_codec),
                         content = '')
        body = self.__createSenderXML(elem_dict)
        d = self.__postService(url, body)

        doc = minidom.parseString(d['data'])
        source = doc.getElementsByTagName('entry').item(0).\
                 getElementsByTagName('id').item(0).childNodes[0].data
        chop = source.split('/')
        endpoint = url + '/' + chop[len(chop)-1]

        return endpoint


    def postPicsToAlbum(self, pics, url):
        """
        upload pictures to specified photo album

        arguments:
            pics : list of filenames of pics
            url : service url of objective photo album

        returns:
            result response of post request
        """
        for pic in pics:
            try:
                p = open(pic, 'rb').read()
                d = self.__postService(url, p, 'image/jpeg')
            except Exception, e:
                print 'file -->', pic, ' caused failure', e
        return d


    def postDiary(self, title, summary, pic=''):
        """
        post new diary.

        variables:
            title : title of a new entry on diary
            summary : body of a new entry
            pic : filename of picture

        returns:
            result of post reqest

        caution:
            dict should be in this order
        """
        d = self.__getService('http://mixi.jp/atom/diary')
        service = self.getCollection(d['data'])[0]['url']
        if len(pic) > 0:
            pics = [pic]
            d = self.postPicsToAlbum(pics, service)

            # get edit uri
            service = ''
            doc = minidom.parseString(d['data'])
            urls = doc.getElementsByTagName('entry').item(0).getElementsByTagName('link')
            for l in urls:
                if 'edit' == l.getAttribute('rel'):
                    service = l.getAttribute('href')

        if len(service) > 0:
            elem_dict = dict(summary = summary.encode(self.mixi_codec),
                             title = title.encode(self.mixi_codec))

            body = self.__createSenderXML(elem_dict)
            d = self.__postService(service, body)
            return d

        elif len(service) == 0:
            raise 'URI Error'


class HatenaBookmarkClient(WSSEAtomClient):
    root_endpoint = 'http://b.hatena.ne.jp/atom'
    service_uri = {'posturi':'', 'feeduri':''}

    def __init__(self, userid, password):
        WSSEAtomClient.__init__(self, userid, password)


    def __extractURIs(self, entrynode):
        links = entrynode.getElementsByTagName('link')
        edituri = ''
        title = ''
        refuri = ''
        for l in links:
            if 'service.edit' == l.getAttribute('rel'):
                edituri = l.getAttribute('href')
                title = l.getAttribute('title')
            elif 'related' == l.getAttribute('rel'):
                refuri = l.getAttribute('href')

        return dict(edituri = edituri,
                    title = title,
                    refuri = refuri)


    def __createSenderXML(self, url='', summary=u'', title=u''):
        impl = minidom.getDOMImplementation()
        doc = impl.createDocument(None, 'entry', None)
        header = doc.documentElement
        header.attributes['xmlns'] = 'http://purl.org/atom/ns#'

        if len(url) > 0:
            elem = doc.createElement('link')
            elem.setAttribute('rel', 'related')
            elem.setAttribute('type', 'text/html')
            elem.setAttribute('href', url)
            header.appendChild(elem)

        if len(summary) > 0:
            elem = doc.createElement('summary')
            elem.setAttribute('type', 'text/plain')
            elem.appendChild(doc.createTextNode(summary))
            header.appendChild(elem)

        if len(title) > 0:
            elem = doc.createElement('title')
            elem.appendChild(doc.createTextNode(title))
            header.appendChild(elem)

        body = doc.toxml(encoding='UTF-8')
        doc.unlink()
        return body


    def getServiceURI(self):
        """
        get PostURI and FeedURI

        returns:
            dictionary of each service URI
        """
        self.createHeaderToken()
        d = self.atomRequest('GET', self.root_endpoint, '', 'text/xml')

        doc = minidom.parseString(d['data'])
        linkelem = doc.getElementsByTagName('feed').item(0).\
                   getElementsByTagName('link')

        posturi = ''
        feeduri = ''
        for l in linkelem:
            if 'service.post' == l.getAttribute('rel'):
                self.service_uri['posturi'] = l.getAttribute('href')
            elif 'service.feed' == l.getAttribute('rel'):
                self.service_uri['feeduri'] = l.getAttribute('href')

        return self.service_uri


    def postBookmark(self, url, summary=u''):
        body = self.__createSenderXML(url, summary, '')

        self.createHeaderToken()
        d = self.atomRequest('POST', self.service_uri['posturi'], body, 'text/xml')

        doc = minidom.parseString(d['data'].lstrip())
        entry = doc.getElementsByTagName('entry').item(0)
        return self.__extractURIs(entry)


    def getFeed(self):
        self.createHeaderToken()
        d = self.atomRequest('GET', self.service_uri['feeduri'], '', 'text/xml')

        doc = minidom.parseString(d['data'].lstrip())
        feed = []
        for e in doc.getElementsByTagName('entry'):
            feed.append(self.__extractURIs(e))

        return feed


    def getBookmarkInfo(self, edituri):
        self.createHeaderToken()
        d = self.atomRequest('GET', edituri, '', 'text/xml')

        doc = minidom.parseString(d['data'].lstrip())
        return d['data']

    def editBookmark(self, edituri, title=u'', summary=u''):
        if len(summary) != 0 or len(title) != 0:
            body = self.__createSenderXML(title=title, summary=summary)
            self.createHeaderToken()
            d = self.atomRequest('PUT', edituri, body, 'text/xml')

            return d['data']
        else:
            raise Exception('title or summary must be set')


    def deleteBookmark(self, edituri):
        self.createHeaderToken()
        d = self.atomRequest('DELETE', edituri, '', 'text/xml')

        doc = minidom.parseString(d['data'].lstrip())
        return d['data']
