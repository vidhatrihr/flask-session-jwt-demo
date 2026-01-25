import inspect
from functools import wraps

import time
from flask import jsonify, request
from models import Session
from jwt import jwt_encode, jwt_decode

# Token expiration duration in seconds (10 minutes)
TOKEN_EXPIRATION_SECONDS = 600


def verify_jwt():
  jwt = request.cookies.get('jwt')
  if jwt:
    try:
      payload = jwt_decode(jwt)
      return payload
    except Exception as e:
      print(e)
  return None


def login_required(fn):
  # How many parameters defined by view function (fn)
  count_parameters = len(inspect.signature(fn).parameters)

  @wraps(fn)
  def wrapper(*args, **kwargs):
    payload = verify_jwt()
    new_token = None

    if not payload:
      return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    # Check if the token has expired
    if time.time() > payload['iat'] + TOKEN_EXPIRATION_SECONDS:
      session = Session.query.filter_by(id=payload['session_id']).first()
      if session:
        payload['iat'] = int(time.time())
        new_token = jwt_encode(payload)
      else:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    if count_parameters == 0:
      response = fn(*args, **kwargs)  # Not passing payload
    else:
      response = fn(payload, *args, **kwargs)  # Passing payload as the first parameter

    if new_token:
      response.set_cookie('jwt', new_token, httponly=True)
    return response

  return wrapper
