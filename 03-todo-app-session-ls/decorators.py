import inspect
from functools import wraps
from utils import validate_session
from flask import jsonify


def login_required(fn):
  # How many parameters defined by view function (fn)
  count_parameters = len(inspect.signature(fn).parameters)

  @wraps(fn)
  def wrapper(*args, **kwargs):
    session = validate_session()

    if session:
      if count_parameters == 0:
        return fn(*args, **kwargs)  # Not passing session
      return fn(session, *args, **kwargs)  # Session must be passed as first parameter
    return jsonify({'success': False, 'message': 'Unauthorized'}), 401

  return wrapper
