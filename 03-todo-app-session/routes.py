from flask import Blueprint, render_template, request, jsonify
from werkzeug.security import check_password_hash
from models import db, User, Session, Todo
from utils import validate_session, generate_token
from decorators import login_required

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
  return render_template('index.html')


@routes.route('/auth/whoami')
@login_required
def whoami(session):
  user = User.query.filter_by(id=session.user_id).first()
  return jsonify({
      'success': True,
      'message': f'logged in as {user.name}',
  })


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

    response = jsonify({
        'success': True,
        'message': f'logged in as {user.name}',
    })
    response.set_cookie('sessionId', str(session.id), httponly=True)
    response.set_cookie('token', session.token, httponly=True)

    return response
  else:
    return jsonify({
        'success': False,
        'message': 'email or password incorrect'
    }), 401


@routes.route('/todo/list')
@login_required
def list_todos(session):
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
              } for todo in todos  # serialization
          ]
      }
  })


@routes.route('/todo/create', methods=['POST'])
@login_required
def create_todo(session):
  text = request.json.get('text')

  db.session.add(Todo(
      text=text,
      user_id=session.user_id
  ))
  db.session.commit()

  return jsonify({'success': True, 'message': 'Todo created'})


@routes.route('/todo/update')
@login_required
def update_todo(session):
  todo_id = request.args.get("todoId")
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
def delete_todo(session):
  todo_id = request.args.get('todoId')

  todo = Todo.query.filter_by(id=todo_id).first()

  db.session.delete(todo)
  db.session.commit()

  return jsonify({'success': True, 'message': 'Todo deleted'})
