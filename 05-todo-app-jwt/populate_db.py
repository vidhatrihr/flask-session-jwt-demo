from models import *
from werkzeug.security import generate_password_hash


def populate_db():
  if User.query.count() > 0:
    return

  user1 = User(
      email='vidu@example.com',
      name='vidu',
      password=generate_password_hash('qwerty')
  )

  user2 = User(
      email='rahul@example.com',
      name='rahul',
      password=generate_password_hash('qwerty')
  )

  db.session.add_all([user1, user2])

  todos = [
      Todo(text='Drink water', user_id=1, is_starred=True, is_done=True),
      Todo(text='Be happy',  user_id=1, is_starred=True, is_done=False),
      Todo(text='Keep coding',  user_id=1, is_starred=False, is_done=True),
      Todo(text='Study hard', user_id=1),
  ]

  db.session.add_all(todos)
  db.session.commit()
