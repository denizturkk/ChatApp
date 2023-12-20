from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'

    Id = Column(Integer, primary_key=True)
    UserId = Column(Integer)
    ReceiverId = Column(Integer)
    Message = Column(String(400))
