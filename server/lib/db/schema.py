from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    Subject = Column(String(255), nullable=False)
    Body = Column(Text, nullable=False)
    ReceiverEmail = Column(String(255), nullable=False)
    HtmlBody = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Email(id={self.id}, Subject='{self.Subject}', ReceiverEmail='{self.ReceiverEmail}')>"

