from flask import Blueprint, render_template, request, jsonify
from werkzeug.security import check_password_hash
from models import db, User, Session, Todo
from utils import generate_token

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
  return render_template('index.html')


@routes.route('/auth/login', methods=['POST'])
def login():
  email = request.json.get('email')
  password = request.json.get('password')

  user = User.query.filter_by(email=email).first()

  if user and check_password_hash(user.password, password):
    session = Session(
        token=generate_token(),
        user_id=user.id
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'logged in as {user.name}',
        'payload': {
            'token': session.token,
            'sessionId': session.id,
            'userId': session.user_id
        }
    })
  else:
    return jsonify({
        'success': False,
        'message': 'email or password incorrect'
    })


@routes.route('/todo/list')
def list_todos():
  session_id = request.args.get('session_id')
  token = request.args.get('token')

  session = Session.query.filter_by(id=session_id).first()

  if not session or session.token != token:
    return jsonify({'success': False, 'message': 'Invalid session'}), 401

  todos = Todo.query.filter_by(user_id=session.user_id).all()

  return jsonify({
      'success': True,
      'message': 'all todos fetched',
      'payload': {
          'todos': [
              {
                  'id': todo.id,
                  'text': todo.text,
                  'isDone': todo.is_done,
                  'isStarred': todo.is_starred
              } for todo in todos
          ]
      }
  })


@routes.route('/todo/create')
def create_todo():
  ...


@routes.route('/todo/update')
def update_todo():
  todo_id = request.args.get("todo_id")
  action = request.args.get('action')

  todo = Todo.query.filter_by(id=todo_id).first()
  if not todo:
    return jsonify({'success': False, 'message': 'Todo not found'})

  if action == 'mark_done':
    todo.is_done = not todo.is_done
  elif action == 'mark_starred':
    todo.is_starred = not todo.is_starred

  db.session.commit()
  return jsonify({'success': True, 'message': 'Todo updated'})


@routes.route('/todo/delete')
def delete_todo():
  ...
