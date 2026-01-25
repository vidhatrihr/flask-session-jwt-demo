import time

from flask import Blueprint, render_template, request, jsonify
from werkzeug.security import check_password_hash

from jwt import jwt_encode
from models import db, User, Todo
from decorators import login_required


routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
  return render_template('index.html')


@routes.route('/auth/whoami')
@login_required
def whoami(user_id):
  user = User.query.filter_by(id=user_id).first()
  return jsonify({
      'success': True,
      'message': f'Logged in as {user.name}'
  })


@routes.route('/auth/login', methods=['POST'])
def login():
  email = request.json.get('email')
  password = request.json.get('password')

  user = User.query.filter_by(email=email).first()

  if user and check_password_hash(user.password, password):
    response = jsonify({
        'success': True,
        'message': f'Logged in as {user.name}'
    })

    payload = {
        'user_id': user.id,
        'iat': time.time()
    }
    jwt = jwt_encode(payload)

    response.set_cookie('jwt', jwt, httponly=True)
    return response
  else:
    return jsonify({
        'success': False,
        'message': 'Email or password incorrect'
    }), 401


@routes.route('/todo/list')
@login_required
def list_todos(user_id):
  todos = Todo.query.filter_by(user_id=user_id).all()

  return jsonify({
      'success': True,
      'message': 'All todos are fetched',
      'payload': {
          'todos': [
              {
                  'id': todo.id,
                  'text': todo.text,
                  'isStarred': todo.is_starred,
                  'isDone': todo.is_done,
              }
              for todo in todos
          ]
      }
  })


@routes.route('/todo/create', methods=['POST'])
@login_required
def create_todos(user_id):
  text = request.json.get('text')

  db.session.add(Todo(
      text=text,
      user_id=user_id,
  ))
  db.session.commit()

  return jsonify({'success': True, 'message': 'Todo is created'})


@routes.route('/todo/update')
@login_required
def update_todo():
  todo_id = request.args.get('todoId')
  action = request.args.get('action')

  todo = Todo.query.filter_by(id=todo_id).first()

  if action == 'markDone':
    todo.is_done = not todo.is_done
  elif action == 'markStarred':
    todo.is_starred = not todo.is_starred

  db.session.commit()
  return jsonify({'success': True, 'message': 'Todo updated'})


@routes.route('/todo/delete')
@login_required
def delete_todo():
  todo_id = request.args.get('todoId')

  todo = Todo.query.filter_by(id=todo_id).first()
  db.session.delete(todo)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Todo deleted'})
