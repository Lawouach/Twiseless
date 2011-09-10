# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer

from lib.model import Base

__all__ = ['User']

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(Unicode)
    user_id = Column(Integer)
    oauth_token = Column(Unicode)
    oauth_token_secret = Column(Unicode)

    @staticmethod
    def get_by_uid(session, uid):
        return session.query(User).filter(User.user_id==uid).first()

    @staticmethod
    def all_(session):
        return session.query(User)
