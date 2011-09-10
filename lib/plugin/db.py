# -*- coding: utf-8 -*-
import cherrypy
from cherrypy.process import wspbus, plugins
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from lib.model import Base

__all__ = ['SAEnginePlugin']
        
class SAEnginePlugin(plugins.SimplePlugin):
    def __init__(self, bus):
        """
        The plugin is registered to the CherryPy engine and therefore
        is part of the bus (the engine *is* a bus) registery.
 
        We use this plugin to create the SA engine. At the same time,
        when the plugin starts we create the tables into the database
        using the mapped class of the global metadata.
        """
        plugins.SimplePlugin.__init__(self, bus)
        self.sa_engine = None
        self.session = scoped_session(sessionmaker(autoflush=True,
                                                   autocommit=False))
 
    def start(self):
        self.bus.log('Starting up DB access')
        self.sa_engine = create_engine('sqlite:///twiseless.db', echo=False)
        self.create_all()
        self.bus.subscribe("bind-session", self.bind)
        self.bus.subscribe("commit-session", self.commit)
 
    def stop(self):
        self.bus.log('Stopping down DB access')
        self.bus.unsubscribe("bind-session", self.bind)
        self.bus.unsubscribe("commit-session", self.commit)
        if self.sa_engine:
            #self.destroy_all()
            self.sa_engine.dispose()
            self.sa_engine = None
 
    def bind(self):
        """
        Whenever this plugin receives the 'bind-session' command, it applies
        this method and to bind the current session to the engine.

        It then returns the session to the caller.
        """
        self.session.configure(bind=self.sa_engine)
        return self.session

    def commit(self):
        """
        Commits the current transaction or rollbacks if an error occurs.

        In all cases, the current session is unbound and therefore
        not usable any longer.
        """
        try:
            self.session.commit()
        except:
            self.session.rollback()  
            raise
        finally:
            self.session.remove()
    
    def create_all(self):
        self.bus.log('Creating database')
        from lib.model.user import User
        from lib.model.mention import Mention
        Base.metadata.create_all(self.sa_engine)
        
    def destroy_all(self):
        self.bus.log('Destroying database')
        Base.metadata.drop_all(self.sa_engine)
