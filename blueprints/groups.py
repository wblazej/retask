from flask import Blueprint, request
from lib.auth import Auth
from lib.messages import Messages
from database.models import Groups, Users, db
import json
import htmlentities

groups = Blueprint('gropus', __name__)


@groups.route('', methods=['get'])
@Auth.root_required
def _groups_():
    all_groups = Groups.query.all()
    to_return = []

    for ag in all_groups:
        to_return.append({
            "id": ag.id,
            "name": ag.name,
            "color": ag.color
        })

    return {"ok": to_return}


@groups.route('/create', methods=['post'])
@Auth.root_required
def _create_():
    post = request.get_json()

    name = post.get("name")
    color = post.get("color")

    if not name:
        return {"errro": Messages.NAME_REQUIRED}, 400

    if not color:
        return {"error": Messages.COLOR_REQIURED}, 400

    if Groups.query.filter_by(name=name).first():
        return {"error": Messages.GROUP_EXISTS}, 400

    name = htmlentities.encode(name)
    if not correct_hex_number(color):
        return {"error": Messages.INVALID_HEX}, 400

    new_group = Groups(name=name, color=color)
    db.session.add(new_group)
    db.session.commit()

    return {"ok": Messages.GROUP_CREATED}

@groups.route('/<group_id>/update', methods=['post'])
@Auth.root_required
def _update_(group_id):
    try:
        group_id = int(group_id)
    except ValueError:
        return {"error": Messages.INT_VALUE_ERROR}, 400

    group = Groups.query.filter_by(id=group_id).first()

    if not group:
        return {"error": Messages.GROUP_NOT_EXISTS}, 404

    post = request.get_json()

    name = post.get("name")
    color = post.get("color")

    if name:
        if Groups.query.filter_by(name=name).first():
            return {"error": Messages.GROUP_EXISTS}, 400
            
        name = htmlentities.encode(name)
        group.name = name

    if color:
        if not correct_hex_number(color):
            return {"error": Messages.INVALID_HEX}, 400
        group.color = color

    db.session.commit()

    return {"ok": Messages.GROUP_UPDATED}

@groups.route('/<group_id>/delete', methods=['get'])
@Auth.root_required
def _delete_(group_id):
    try:
        group_id = int(group_id)
    except ValueError:
        return {"error": Messages.INT_VALUE_ERROR}, 400

    if not Groups.query.filter_by(id=group_id).first():
        return {"error": Messages.GROUP_NOT_EXISTS}, 404

    Groups.query.filter_by(id=group_id).delete()
    db.session.commit()

    return {"ok": Messages.GROUP_DELETED}


@groups.route('/<group_id>/participants', methods=['get'])
@Auth.root_required
def _participants_(group_id):
    try:
        group_id = int(group_id)
    except ValueError:
        return {"error": Messages.INT_VALUE_ERROR}, 400

    all_users = Users.query.all()
    to_return = []

    for user in all_users:
        groups = []
        if user.groups:
            groups = json.loads(user.groups)
        if group_id in groups:
            to_return.append({
                "id": user.id,
                "username": user.username,
                "admin": user.admin
            })

    return {"ok": to_return}


def correct_hex_number(hex_number_string):
    allowed_chars = "0123456789ABCDEF"
    for hns in hex_number_string:
        if not str(hns).upper() in allowed_chars:
            return False

    return True