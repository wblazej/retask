from flask import Blueprint, request, session
from database.models import Users
from lib.messages import Messages
from lib.hash import Hash

login = Blueprint('login', __name__)

@login.route('', methods=['post'])
def _login_():
    if session.get("logged_in"):
        return {"error": Messages.ALREADY_LOGGED_IN}

    post = request.get_json()

    username = post.get("login")
    password = post.get("password")

    if not username:
        return {"error": Messages.USERNAME_REQUIRED}, 400

    if not password:
        return {"error": Messages.PASSWORD_REQUIRED}, 400

    user = Users.query.filter_by(username=username).first()

    if not user:
        return {"error": Messages.WRONG_LOGIN_DATA}, 401

    if not Hash.verify_password(user.password, password):
        return {"error": Messages.WRONG_LOGIN_DATA}, 401

    session['logged_in'] = True
    session['user_id'] = user.id

    
    return {"ok": Messages.SUCCESSFUL_LOGIN}