
import sqlalchemy
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from appNews.settings import DATABASE

Base = declarative_base()

class TimeStampedModelMixin:

    created_at = Column(DateTime, default=datetime.datetime.now)
    modify_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
class Article(TimeStampedModelMixin,Base):
    __tablename__ = 'news_article'

    id = Column(Integer, primary_key=True)
    lid = Column(String(255))
    category = Column(String(255))
    author = Column(String(255))
    # supercid = Column(Integer)
    # cid = Column(Integer)

    # sid = Column(Integer)
    sid_text = Column(String(255))

    url = Column(String(1024))

    title = Column(String(1024))
    post_time = Column(DateTime)
    # post_time_text = Column(String(255))

    desc = Column(String(1024))
    cover = Column(String(1024))
    cover_origin = Column(String(1024))

    content = Column(Text)

engin_url = sqlalchemy.engine.url.URL(
    drivername=DATABASE["dialect"],
    host=DATABASE["host"],
    port=DATABASE["port"],
    username=DATABASE["username"],
    password=DATABASE["password"],
    database=DATABASE["db_name"],
   query={'charset': 'utf8'},  # the key-point setting
)

db_engine = create_engine(
    engin_url, encoding='utf8',
    echo=False, pool_recycle=3600
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
session = scoped_session(Session)

def create_schema():
    """
    Drop schema if exists and create schema

    """
    Base.metadata.drop_all(db_engine)
    Base.metadata.create_all(db_engine)