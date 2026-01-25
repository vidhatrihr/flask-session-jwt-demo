from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
import secrets
import string


db = SQLAlchemy()


class User(db.Model):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  email = Column(String)
  password = Column(String)


class Session(db.Model):
  __tablename__ = 'sessions'
  id = Column(Integer, primary_key=True, autoincrement=True)
  token = Column(String, unique=True)
  user_id = Column(Integer)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

with app.app_context():
  db.create_all()
  if User.query.count() == 0:
    db.session.add(User(
        name='vidu',
        email='vidu@example.com',
        password='fish'
    ))
    db.session.add(User(
        name='rahul',
        email='rahul@example.com',
        password='jackal'
    ))
    db.session.commit()


def generate_token(length=10):
  alphabet = string.ascii_letters + string.digits
  return ''.join(secrets.choice(alphabet) for _ in range(length))


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/auth/login', methods=['POST'])
def login():
  email = request.json.get('email')
  password = request.json.get('password')

  user = User.query.filter_by(email=email).first()

  if user and user.password == password:
    session = Session(
        token=generate_token(),
        user_id=user.id
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Logged in as {user.name}',
        'payload': {
            'sessionId': session.id,
            'token': session.token
        }
    })
  else:
    return jsonify({
        'success': False,
        'message': 'Email or password is incorrect'
    })


@app.route('/launch-missile')
def launch():
  session_id = request.args.get('session_id')
  token = request.args.get('token')

  session = Session.query.filter_by(id=session_id).first()

  if session and session.token == token:
    user = User.query.filter_by(id=session.user_id).first()
    return jsonify({
        'success': True,
        'message': f'Missile is launched 🚀 by {user.name}'
    })
  else:
    return jsonify({
        'success': False,
        'message': 'You cannot launch missile'
    }), 401


app.run(debug=True)
