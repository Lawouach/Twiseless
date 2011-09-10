# -*- coding: utf-8 -*-
import cherrypy

from lib.model.user import User

__all__ = ['UserTool']

class UserTool(cherrypy.Tool):
    def __init__(self):
        """
        The user tool takes care of fetching the current
        logged in user to then associating it with
        the request.
        """
        cherrypy.Tool.__init__(self, 'before_handler',
                               self._fetch,
                               priority=20)
 
    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource',
                                      self._cleanup,
                                      priority=80)

    def _fetch(self):
        if 'user_id' not in cherrypy.session:
            raise cherrypy.HTTPRedirect("/login")

        uid = cherrypy.session['user_id'].decode('utf-8')
        user = User.get_by_uid(cherrypy.request.db, uid)
        if not user:
            raise cherrypy.HTTPRedirect("/login/")

        cherrypy.request.user = user

    def _cleanup(self):
        cherrypy.request.user = None
