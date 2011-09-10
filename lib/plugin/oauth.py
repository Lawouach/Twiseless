# -*- coding: utf-8 -*-
import cherrypy
from cherrypy.process import wspbus, plugins
import oauth2

__all__ = ['OAuthEnginePlugin']
        
class OAuthEnginePlugin(plugins.SimplePlugin):
    def __init__(self, bus, consumer_key, consumer_secret):
        """
        Allows to interact with the underlyin OAuth API
        """
        plugins.SimplePlugin.__init__(self, bus)
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        
    def start(self):
        self.bus.log('Starting OAuth plugin')
        self.bus.subscribe("oauth-consumer", self.get_consumer)
        self.bus.subscribe("oauth-token", self.get_token)
        self.bus.subscribe("oauth-request", self.request)
        
    def stop(self):
        self.bus.log('Stopping down OAuth plugin')
        self.bus.unsubscribe("oauth-consumer", self.get_consumer)
        self.bus.unsubscribe("oauth-token", self.get_token)
        self.bus.unsubscribe("oauth-request", self.request)

    def get_consumer(self):
        return oauth2.Consumer(self.consumer_key, self.consumer_secret)

    def get_token(self, key, secret):
        return oauth2.Token(key=key, secret=secret)

    def request(self, url, key=None, secret=None, method='GET'):
        consumer = self.get_consumer()
        token = None
        if key and secret:
            token = self.get_token(key, secret)
        resp, content = oauth2.Client(consumer, token).request(url, method=method)
        if resp['status'] != '200':
            self.bus.log(content)
            raise cherrypy.HTTPError(400, "Invalid response from Twitter OAuth.")
        return content
