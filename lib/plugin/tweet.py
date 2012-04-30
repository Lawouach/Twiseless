# -*- coding: utf-8 -*-
import json
import re

import cherrypy
from cherrypy.process import wspbus, plugins
import oauth2 as oauth
from dateutil.parser import parse
from guess_language import guessLanguageTag

from lib.model import Base
from lib.model.user import User
from lib.model.mention import Mention

__all__ = ['TweetEnginePlugin']
        
class TweetEnginePlugin(plugins.SimplePlugin):
    def __init__(self, bus, freq=30.0):
        """
        Handles background tasks that will go and fetch
        the data from twitter's API and feed the local database
        with them.

        Do not set a too low requency or you'll probably
        reach the API's rate limit quickly.
        """
        plugins.SimplePlugin.__init__(self, bus)
        self.tasks = []
        self.freq = freq
        
    def start(self):
        self.bus.log('Starting up twitter cyclic loader')
        task = plugins.BackgroundTask(self.freq, self.fetch_mentions)
        self.tasks.append(task)
        task.bus = self.bus
        task.start()
    start.priority = 70
        
    def stop(self):
        self.bus.log('Stopping down twitter cyclic loader')
        for task in self.tasks:
            task.bus = None
            task.cancel()
        self.tasks = []

    def fetch_mentions(self):
        url = "http://api.twitter.com/1/statuses/mentions.json?count=50"
        
        session = cherrypy.engine.publish('bind-session').pop()
        newest = Mention.newest(session)
        if newest:
            url += "&since_id=%d" % newest.tweet_id
        for user in User.all_(session):
            content = self.bus.publish("oauth-request", url,
                                       user.oauth_token,
                                       user.oauth_token_secret).pop()
            tweets = json.loads(content)
            if newest: cherrypy.log("Retrieved %d tweets since %s" % (len(tweets), newest.date))
            else: cherrypy.log("Retrieved %d tweets" % (len(tweets), ))
            for tweet in tweets:
                user = tweet.get('user')
                if user:
                    session.add(Mention(username=user['name'],
                                        user_id=user['id'],
                                        tweet=tweet['text'],
                                        tweet_id=tweet['id'],
                                        lang=self.guess_language(tweet['text']),
                                        date=parse(tweet['created_at'])))

        cherrypy.engine.publish('commit-session')

    def guess_language(self, tweet):
        # based on the simple idea at:
        # http://granades.com/2009/04/06/using-regular-expressions-to-match-twitter-users-and-hashtags/
        tweet = re.sub(r'(\A|\s)@(\w+)', r'\1', tweet)
        tweet = re.sub(r'(\A|\s)#(\w+)', r'\1', tweet)
        return guessLanguageTag(tweet.strip()).decode('utf-8')
