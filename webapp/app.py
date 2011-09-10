# -*- coding: utf-8 -*-
import cgi

import cherrypy

from lib.model.user import User
from lib.model.mention import Mention

__all__ = ['Twiseless']

class Twiseless(object):
    def __init__(self):
        self.login = Login()
        
    @cherrypy.expose
    @cherrypy.tools.user()
    @cherrypy.tools.render(template="index.mako")
    def index(self):
        pass
    
    @cherrypy.expose
    def logout(self):
        cherrypy.lib.sessions.expire()
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def mentions(self):
        db = cherrypy.request.db
        
        graph = []
        root = {'id': 'root', 'name': '', "data": { "$type": "none" }, 'adjacencies': []}
        for user_id in Mention.users(db):
            node = {
                "nodeTo": "%d" % user_id,
                "data": {
                    '$type': 'none'
                    }
                }
            root['adjacencies'].append(node)
        graph.append(root)

        total = len(root['adjacencies'])
        
        for index, (username, user_id, count) in enumerate(Mention.grouped(db)):
            node = {
                "id": "%d" % user_id,
                "name": username,
                "data": {
                    "$color": "#cf5",
                    "$height": 120,
                    "$angularWidth": count * 360 / (total * 1.0)
                    },
                "adjacencies": []
                }
            graph.append(node)
        return graph
            
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def tweets(self, user_id):
        db = cherrypy.request.db
        tweets = []
        for mention in Mention.tweets(db, int(user_id)):
            tweets.append(mention.tweet)

        return tweets

class Login(object):
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    authenticate_url = 'https://api.twitter.com/oauth/authorize'

    @cherrypy.expose
    def index(self):
        engine = cherrypy.engine
        content = engine.publish("oauth-request", Login.request_token_url).pop()
        cherrypy.session['request_token'] = dict(cgi.parse_qsl(content))
        cherrypy.lib.sessions.save()

        url = "%s?oauth_token=%s" % (Login.authenticate_url,
                                     cherrypy.session['request_token']['oauth_token'])

        raise cherrypy.HTTPRedirect(url)

    @cherrypy.expose
    def success(self, *args, **kwargs):
        engine = cherrypy.engine
        content = engine.publish("oauth-request", Login.access_token_url,
                                 cherrypy.session['request_token']['oauth_token'],
                                 cherrypy.session['request_token']['oauth_token_secret']).pop()

        access_token = dict(cgi.parse_qsl(content))
        cherrypy.session['user_id'] = uid = access_token['user_id']
        db = cherrypy.request.db
        user = User.get_by_uid(db, uid.decode('utf-8'))
        if not user:
            user = User(name=access_token['screen_name'],
                        user_id=int(uid),
                        oauth_token=access_token['oauth_token'],
                        oauth_token_secret=access_token['oauth_token_secret'])
            db.add(user)
        else:
            user.oauth_token = access_token['oauth_token']
            user.oauth_token_secret = access_token['oauth_token_secret']
        
        raise cherrypy.HTTPRedirect("/")
    
