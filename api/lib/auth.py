from flask import session
from functools import wraps
from lib.messages import Messages
from database.models import Users

class Auth:
    @staticmethod
    def logged_user(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return {"error": Messages.NOT_LOGGED_IN}, 401

            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def root_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return {"error": Messages.NOT_LOGGED_IN}, 401

            user_id = session['user_id']
            account = Users.query.filter_by(id=user_id).first()

            if not account.username == "root":
                return {"error": Messages.ROOT_REQUIRED}, 401

            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return {"error": Messages.NOT_LOGGED_IN}, 401

            user_id = session['user_id']
            account = Users.query.filter_by(id=user_id).first()
            
            if not account.admin:
                return {"error": Messages.ADMIN_REQUIRED}, 401

            return f(*args, **kwargs)
        return decorated_function