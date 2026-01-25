import string
import secrets
from flask import request
from models import Session


def generate_token(length=10):
  chars = string.ascii_letters + string.digits
  return ''.join(secrets.choice(chars) for _ in range(length))


def validate_session():
  if request.method == 'GET':
    session_id = request.args.get('sessionId')
    token = request.args.get('token')

  if request.method == 'POST':
    session_id = request.json.get('sessionId')
    token = request.json.get('token')

  session = Session.query.filter_by(id=session_id).first()
  if session and session.token == token:
    return session
  return None
