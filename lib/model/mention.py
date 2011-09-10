# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy import desc
from sqlalchemy.sql import func

from lib.model import Base

__all__ = ['Mention']

class Mention(Base):
    __tablename__ = 'mention'
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(Unicode)
    user_id = Column(Integer)
    tweet = Column(Unicode)
    tweet_id = Column(Integer)
    date = Column(DateTime)

    @staticmethod
    def all_(session):
        return session.query(Mention)

    @staticmethod
    def grouped(session):
        return session.query(Mention.username, Mention.user_id, func.count(Mention.tweet_id)).group_by(Mention.username, Mention.user_id)

    @staticmethod
    def users(session):
        return session.query(Mention.user_id).group_by(Mention.user_id)

    @staticmethod
    def tweets(session, user_id):
        return session.query(Mention).filter(Mention.user_id==user_id)

    @staticmethod
    def get_by_tweet_id(session, tweet_id):
        return session.query(Mention).filter(Mention.tweet_id==tweet_id).first()

    @staticmethod
    def newest(session):
        return session.query(Mention).order_by(desc(Mention.date)).first()
