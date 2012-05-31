# -*- coding: utf-8 -*-

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.file import Storage

import ConfigParser
import os.path
import requests
from datetime import datetime

date_fmt = "%Y-%m-%dT%H:%M:%SZ"

config = ConfigParser.SafeConfigParser()
config.read("credential.cfg")
channel = "yoshifumitest0000"

storage = Storage("youtube.dat")
credentials = storage.get()

def check_credential(credentials):
    if credentials is None or credentials.invalid == True:
        return False
    elif datetime.now() >= credentials.token_expiry:
        return False
    else:
        return True

if not check_credential(credentials):
    flow = OAuth2WebServerFlow(
        client_id=config.get(channel, "client_id"),
        client_secret=config.get(channel, "client_secret"),
        scope="https://gdata.youtube.com",
        user_agent="youtoube-testuploader/1.0")
    credentials = run(flow, storage)

location = (r"http://uploads.gdata.youtube.com/" +
            r"feeds/api/users/%s/uploads") % config.get(channel, "username")

bounary_string = "YOUTUBE_PARTIAL_UPLOAD"
video_filename = "test.mp4"
filesize = os.path.getsize(video_filename)


api_xml_request = """\
Content-Type: application/atom+xml; charset=UTF-8

<?xml version="1.0"?>
<entry xmlns="http://www.w3.org/2005/Atom"
  xmlns:media="http://search.yahoo.com/mrss/"
  xmlns:yt="http://gdata.youtube.com/schemas/2007">
  <media:group>
    <media:title type="plain">Test partial update</media:title>
    <media:description type="plain">
      Ko-san looks funny
    </media:description>
    <media:category
      scheme="http://gdata.youtube.com/schemas/2007/categories.cat">People
    </media:category>
    <media:keywords>test, life, funny</media:keywords>
  </media:group>
</entry>
"""

headers = {"Authorization": "Bearer %s" % credentials.access_token,
           "GData-Version": "2",
           "X-GData-Client": config.get(channel, "client_id"),
           "X-GData-Key": "key=%s" % config.get(channel, "key"),
           "Slug": video_filename,
           "Content-Type": "multipart/related; boundary=%s" % bounary_string,
           "User-Agent": "youtoube-testuploader/1.0",
           "Transfer-Encoding": "chunked",
           "Connection": "close"}


read_length = 100 * 1024

body = "--%s\r\n" % bounary_string
body += api_xml_request
body += "\r\n"
with open(video_filename, "rb") as f:
    length = 0
    while True:
        body += "--%s\r\n" % bounary_string
        body += "Content-Type: video/mp4\r\n"
        body += "Content-Transfer-Encoding: binary\r\n"
        chunk = f.read(read_length)
        size = len(chunk)
        if size == 0:
            break
        length += size
        print length
        body += "Content-Range: bytes %d/*\r\n\r\n" % size
        body += chunk
        body += "\r\n"

    body += "Content-Range: bytes */%d\n\n" % length
    body += "--%s--\r\n" % bounary_string

    fp = open("hoge.bin", "wb")
    fp.write(body)
    fp.close()

try:
    r = requests.post(location, data=body, headers=headers)
    print r.text
except requests.exceptions.ConnectionError as e:
    print e.message
