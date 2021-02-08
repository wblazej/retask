from flask import Blueprint, session, request
from lib.messages import Messages
from database.models import db
from database.models import Users
from lib.hash import Hash

user = Blueprint('user', __name__)

@user.route('change-password', methods=['post'])
def _change_password_():
    if not session.get("logged_in"):
        return {"error": Messages.NOT_LOGGED_IN}

    post = request.get_json()

    current_pwd = post.get("password")
    new_pwd = post.get("new_password")
    confirm_pwd = post.get("confirm_password")

    if not current_pwd:
        return {"error": Messages.CURRENT_PWD_REQUIRED}, 400

    if not new_pwd:
        return {"error": Messages.NEW_PASSWORD_REQUIRED}, 400

    if new_pwd != confirm_pwd:
        return {"error": Messages.PWD_CONFIRMATION_FAILED}, 400

    account = Users.query.filter_by(id=session["user_id"]).first()
    
    if not Hash.verify_password(account.password, current_pwd):
        return {"error": Messages.WRONG_CURRENT_PWD}, 401

    pwd_hash = Hash.hash_password(new_pwd)
    account.password = pwd_hash
    db.session.commit()

    return {"ok": Messages.PASSWORD_CHANGED}