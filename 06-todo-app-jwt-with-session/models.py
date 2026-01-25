from sqlalchemy import Column, Integer, String, Boolean
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
  __tablename__ = 'users'
  id = Column(Integer, autoincrement=True, primary_key=True)
  email = Column(String, unique=True)
  name = Column(String)
  password = Column(String)


class Session(db.Model):
  __tablename__ = 'sessions'
  id = Column(Integer, autoincrement=True, primary_key=True)
  user_id = Column(Integer)


class Todo(db.Model):
  __tablename__ = 'todos'
  id = Column(Integer, autoincrement=True, primary_key=True)
  text = Column(String)
  user_id = Column(Integer)
  is_done = Column(Boolean)
  is_starred = Column(Boolean)
