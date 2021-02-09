from flask import Blueprint, request
from lib.auth import Auth
from lib.messages import Messages
from database.models import Groups, db

groups = Blueprint('gropus', __name__)

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
        group.name = name

    if color:
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