# -*- config: utf-8 -*-

import re

import tweepy

consumer_key = 'b33CMmkAfcy8wH54Am3vLA'
consumer_secret = 'Kz594sfVeb1ropQ8DCPB4bfdc3rMOg68YLCQP2KZ4'
access_token =  '4135891-JdqurXem220KLauW1krvwq4cCMzgKeGLlVWrODvCyE'
access_secret = 'UcE1zphlTXsq0egbNEOIGwe81xruxZbMp7Kj8gbwZY'

#youtube_url = r'[http://](youtube.com|youtu.be)/[=\w\?\+/]+'
youtube_url = r'(bit\.ly|htn\.to|t\.co)'
youtube_prog = re.compile(youtube_url)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

class MyStreamListener(tweepy.StreamListener):
  def on_status(self, status):
    if youtube_prog.search(status.text):
      print status.author.screen_name, status.text

stream = tweepy.Stream(auth=auth, listener=MyStreamListener(), secure=True)
stream.userstream()

