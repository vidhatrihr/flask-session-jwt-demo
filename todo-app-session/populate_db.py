from models import db, Todo, User
from werkzeug.security import generate_password_hash


def populate_db():
  if User.query.count() > 0:
    return

  user1 = User(
      name='rahul',
      email='rahul@example.com',
      password=generate_password_hash('qwerty')
  )

  user2 = User(
      name='vidu',
      email='vidu@example.com',
      password=generate_password_hash('qwerty')
  )

  db.session.add_all([user1, user2])

  todos = [
      Todo(text='hello_1', user_id=1, is_done=True),
      Todo(text='hello_2', user_id=1, is_done=True),
      Todo(text='hello_3', user_id=1, is_starred=True),
      Todo(text='hello_4', user_id=1),
      Todo(text='hello_5', user_id=1),
  ]

  db.session.add_all(todos)
  db.session.commit()
