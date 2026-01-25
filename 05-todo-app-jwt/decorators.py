import inspect
from functools import wraps

import time
from flask import jsonify, request
from jwt import jwt_decode

# Token expiration duration in seconds (1 hour)
TOKEN_EXPIRATION_SECONDS = 3600


def verify_jwt():
  jwt = request.cookies.get('jwt')
  if jwt:
    try:
      payload = jwt_decode(jwt)
      # Check if the token has expired
      if time.time() > payload['iat'] + TOKEN_EXPIRATION_SECONDS:
        return None
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
    if payload:
      if count_parameters == 0:
        return fn(*args, **kwargs)  # Not passing user_id
      return fn(payload['user_id'], *args, **kwargs)  # Passing user_id as first parameter
    return jsonify({'success': False, 'message': 'Unauthorized'}), 401

  return wrapper
