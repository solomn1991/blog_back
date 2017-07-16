from sqlalchemy import Column, ForeignKey, Integer, String,DateTime,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import datetime

Base = declarative_base()


class User(Base):
    __tablename__="user"

    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String,unique=True)
    password = Column(String)
    email = Column(String)
    passages = relationship("Passage",backref="passages")






class Passage(Base):
    __tablename__ = "passage"

    id = Column(Integer,primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer,ForeignKey('user.id'))
    create_date = Column(DateTime,default=datetime.datetime.now())
    is_publish = Column(Boolean,default=False)

    user = relationship("User",foreign_keys="Passage.user_id")


