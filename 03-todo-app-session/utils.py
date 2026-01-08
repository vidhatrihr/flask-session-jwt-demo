import string
import secrets
from flask import request
from models import Session


def generate_token(length=10):
  chars = string.ascii_letters + string.digits
  return ''.join(secrets.choice(chars) for _ in range(length))


def validate_session():
  session_id = request.cookies.get('sessionId')
  token = request.cookies.get('token')

  session = Session.query.filter_by(id=session_id).first()
  if session and session.token == token:
    return session
  return None
