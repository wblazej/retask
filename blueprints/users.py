from flask import Blueprint, session, request
from lib.messages import Messages
from database.models import db
from database.models import Users
from lib.hash import Hash
from lib.auth import Auth
from database.models import Groups
import json
import string
from random import choices
import htmlentities

users = Blueprint('users', __name__)


@users.route('', methods=['get'])
@Auth.root_required
def _users_():
    all_users = Users.query.all()
    all_groups = Groups.query.all()
    to_return = []

    for au in all_users:
        groups = []
        if au.groups:
            for g in json.loads(au.groups):
                groups.append({
                    "id": all_groups[g-1].id,
                    "name": all_groups[g-1].name,
                    "color": all_groups[g-1].color
                })

        to_return.append({
            "id": au.id,
            "username": au.username,
            "groups": groups,
            "admin": au.admin
        })

    return {"ok": to_return}


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

        if not admin or type(admin) != bool:
            admin = False

        for ag in default_groups + groups:
            try: all_groups[ag-1]
            except: return {"error": Messages.GROUP_ID_NOT_FOUND.replace("<id>", str(ag))}, 400

        if Users.query.filter_by(username=username).first():
            return {"error": Messages.USERNAME_EXISTS.replace("<username>", username)}, 400

        groups_json = json.dumps(default_groups + groups)
        username = htmlentities.encode(username)
        new_user = Users(username=username, password=hash_pwd, groups=groups_json, admin=admin)
        db.session.add(new_user)

    db.session.commit()

    return {"ok": Messages.ACCOUNTS_CREATED}


@users.route('/<user_id>/change-username', methods=['post'])
@Auth.root_required
def _change_username_(user_id):
    user = Users.query.filter_by(id=user_id).first()

    if not user:
        return {"error": Messages.USER_NOT_FOUND}, 404

    post = request.get_json()
    new_username = post.get("username")

    if not new_username:
        return {"error": Messages.USERNAME_REQUIRED}, 400

    new_username = htmlentities.encode(new_username)
    user.username = new_username
    db.session.commit()

    return {"ok": Messages.USERNAME_CHANGED}


@users.route("/<user_id>/set-admin/<boolean_value>", methods=['get'])
@Auth.root_required
def _set_admin_(user_id, boolean_value):
    user = Users.query.filter_by(id=user_id).first()

    if not user:
        return {"error": Messages.USER_NOT_FOUND}, 404

    if boolean_value.lower() == "true":
        user.admin = True
    elif boolean_value.lower() == "false":
        user.admin = False
    else:
        return {"error": Messages.BOOL_VALUE_ERROR}, 400

    db.session.commit()

    return {"ok": Messages.ADMIN_STATUS_CHANGED}


@users.route("<user_id>/reset-password", methods=['get'])
@Auth.root_required
def _reset_password_(user_id):
    user = Users.query.filter_by(id=user_id).first()

    if not user:
        return {"error": Messages.USER_NOT_FOUND}, 404

    characters = string.ascii_lowercase + string.digits
    reseted_password = ''.join(choices(characters, k=6))
    hash_pwd = Hash.hash_password(reseted_password)

    user.password = hash_pwd
    db.session.commit()

    return {"ok": f"New password: {reseted_password}"}


@users.route("/<user_id>/group/add/<group_id>", methods=['get'])
@Auth.root_required
def _add_to_group_(user_id, group_id):
    user = Users.query.filter_by(id=user_id).first()

    try:
        group_id = int(group_id)
    except ValueError:
        return {"error": Messages.INT_VALUE_ERROR}

    if not user:
        return {"error": Messages.USER_NOT_FOUND}, 404

    if not Groups.query.filter_by(id=group_id).first():
        return {"error": Messages.GROUP_NOT_EXISTS}, 404

    groups = json.loads(user.groups)

    if not group_id in groups:
        groups.append(group_id)
        user.groups = json.dumps(groups)

        db.session.commit()

    return {"ok": Messages.GROUP_ASSIGMENTED}


@users.route("/<user_id>/group/remove/<group_id>", methods=['get'])
@Auth.root_required
def _remove_from_group_(user_id, group_id):
    user = Users.query.filter_by(id=user_id).first()

    try:
        group_id = int(group_id)
    except ValueError:
        return {"error": Messages.INT_VALUE_ERROR}

    if not user:
        return {"error": Messages.USER_NOT_FOUND}, 404

    if not Groups.query.filter_by(id=group_id).first():
        return {"error": Messages.GROUP_NOT_EXISTS}, 404

    groups = json.loads(user.groups)

    if group_id in groups:
        groups.remove(group_id)
        user.groups = json.dumps(groups)

        db.session.commit()

    return {"ok": Messages.USER_REMOVED_FROM_GROUP}

@users.route("/<user_id>/delete", methods=['get'])
@Auth.root_required
def _delete_(user_id):
    if not Users.query.filter_by(id=user_id).first():
        return {"error": Messages.USER_NOT_FOUND}, 404

    Users.query.filter_by(id=user_id).delete()
    db.session.commit()

    return {"ok": "User has been deleted"}