#!/usr/bin/env python3
"""User Model - SQLAlchemy"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

#  Base class for our model
Base = declarative_base()


class User(Base):
    """User Class Object"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
