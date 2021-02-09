from flask import Blueprint, request, session
from lib.auth import Auth
from lib.messages import Messages
from database.models import db, Tasks, Groups, Users
import json
from datetime import datetime

tasks = Blueprint('tasks', __name__)

@tasks.route('/create', methods=['post'])
@Auth.admin_required
def _create_():
    post = request.get_json()

    name = post.get("name")
    group_id = post.get("group-id")
    tasks_count = post.get("tasks-count")
    deadline_timestamp = post.get("deadline")

    if not name:
        return {"error": Messages.TASK_NAME_REQUIRED}, 400

    if not group_id:
        return {"error": Messages.GROUP_ID_REQUIRED}, 400

    if not tasks_count:
        return {"error": Messages.TASKS_COUNT_REQUIRED}, 400

    if not deadline_timestamp:
        return {"error": Messages.DEADLINE_REQUIRED}, 400

    if not Groups.query.filter_by(id=group_id).first():
        return {"error": Messages.GROUP_ID_NOT_FOUND.replace("<id>", str(group_id))}, 404

    try:
        tasks_count = int(tasks_count)
    except ValueError:
        return {"error": Messages.INT_VALUE_ERROR}, 400

    if tasks_count > 26:
        return {"error": Messages.MAX_TASKS_COUNT}, 400

    new_task = Tasks(name=name, group_id=group_id, tasks_count=tasks_count, 
                     deadline_timestamp=deadline_timestamp)

    db.session.add(new_task)
    db.session.commit()

    return {"ok": Messages.TASK_CREADTED}


@tasks.route('/<task_id>/update', methods=['post'])
@Auth.admin_required
def _update_(task_id):
    task = Tasks.query.filter_by(id=task_id).first()

    if not task:
        return {"error": Messages.TASK_NOT_FOUND.replace("<id>", str(task_id))}, 404

    post = request.get_json()

    name = post.get("name")
    tasks_count = post.get("tasks-count")
    deadline_timestamp = post.get("deadline")

    if name:
        task.name = name

    if tasks_count:
        try:
            tasks_count = int(tasks_count)
        except ValueError:
            return {"error": Messages.INT_VALUE_ERROR}, 400

        if tasks_count > 26:
            return {"error": Messages.MAX_TASKS_COUNT}, 400

        task.tasks_count = tasks_count

    if deadline_timestamp:
        task.deadline_timestamp = deadline_timestamp

    db.session.commit()

    return {"ok": Messages.TASK_UPDATED}


@tasks.route('/<task_id>/check/<number>', methods=['get'])
@Auth.logged_user
def _check_(task_id, number):
    task = Tasks.query.filter_by(id=task_id).first()

    if not task:
        return {"error": Messages.TASK_NOT_FOUND.replace("<id>", str(task_id))}, 404

    user = Users.query.filter_by(id=session['user_id']).first()

    groups = []
    if user.groups:
        groups = json.loads(user.groups)

    if not task.group_id in groups:
        return {"error": Messages.TASK_NOT_FOUND.replace("<id>", str(task_id))}, 404

    if task.deadline_timestamp < datetime.now().timestamp():
        return {"error": Messages.TASK_EXPIRED}, 401

    solutions = {}
    if task.solutions:
        solutions = json.loads(task.solutions)

    try:
        number = int(number)
    except ValueError:
        return {"error": Messages.INT_VALUE_ERROR}, 400

    if number > task.tasks_count:
        return {"error": Messages.SOLUTION_NOT_FOUND}, 404

    user_id = str(session['user_id'])

    if not solutions.get(user_id):
        solutions[user_id] = []

    if not number in solutions[user_id]:
        solutions[user_id].append(number)

    task.solutions = json.dumps(solutions)
    db.session.commit()

    return {"ok": Messages.SOLUTION_CHECKED}


# @tasks.route('/my', methods=['get'])
# @Auth.logged_user
# def _my_():
#     all_tasks = Tasks.query.all()
#     user = Users.query.filter_by(id=session['user_id']).first()

#     groups = []
#     if user.groups:
#         groups = json.loads(user.groups)

#     to_return = []

#     for at in all_tasks:
#         if at.group_id in groups:
#             to_return.append({
#                 "id": at.id,
#                 "name": at.name,
#                 "tasks_count": at.tasks_count,
#                 "deadline_timestamp": at.deadline_timestamp
#             })