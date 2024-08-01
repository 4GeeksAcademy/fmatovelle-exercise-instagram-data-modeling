import os
import sys
import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class MediaType(enum.Enum): 
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    
    posts = relationship('Post', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)
    followers = relationship('Follower', foreign_keys='Follower.user_to_id', backref='followed', lazy=True)
    following = relationship('Follower', foreign_keys='Follower.user_from_id', backref='follower', lazy=True)

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    media = relationship('Media', backref='post', lazy=True)
    comments = relationship('Comment', backref='post', lazy=True)

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum(MediaType), nullable=False) 
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)  
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)


try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e