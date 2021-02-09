from flask import Blueprint, session, request
from lib.messages import Messages
from database.models import db
from database.models import Users
from lib.hash import Hash
from lib.auth import Auth
from database.models import Groups
import json

users = Blueprint('users', __name__)

@users.route('change-password', methods=['post'])
@Auth.logged_user
def _change_password_():
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

@users.route('create', methods=['post'])
@Auth.root_required
def _create_():
    post = request.get_json()

    default_password = post.get("default-password")
    default_groups = post.get("default-groups")
    accounts = post.get("accounts")

    if not default_password:
        return {"error": Messages.DEFAULT_PASSWORD}, 400

    if not accounts:
        return {"error": Messages.ACCOUNTS_REQUIRED}, 400

    if not default_groups:
        default_groups = []

    all_groups = Groups.query.all()
    hash_pwd = Hash.hash_password(default_password)

    for a in accounts:
        username = a.get("username")
        groups = a.get("groups")
        admin = a.get("admin")

        if not username:
            return {"error": Messages.USERNAME_REQUIRED}, 400

        if not groups:
            groups = []

        if not admin:
            admin = False

        try:
            admin = bool(admin)
        except ValueError:
            admin = False

        for ag in default_groups + groups:
            try: all_groups[ag-1]
            except: return {"error": Messages.GROUP_ID_NOT_FOUND.replace("<id>", str(ag))}, 400

        if Users.query.filter_by(username=username).first():
            return {"error": Messages.USERNAME_EXISTS.replace("<username>", username)}, 400

        groups_json = json.dumps(default_groups + groups)
        new_user = Users(username=username, password=hash_pwd, groups=groups_json, admin=admin)
        db.session.add(new_user)

    db.session.commit()

    return {"ok": Messages.ACCOUNTS_CREATED}