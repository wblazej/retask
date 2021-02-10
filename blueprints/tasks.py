from flask import Blueprint, request, session, abort
from lib.auth import Auth
from lib.messages import Messages
from database.models import db, Tasks, Groups, Users
import json
from datetime import datetime
from lib.calculate_task_points import calculete_task_points
import htmlentities

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

    name = htmlentities.encode(name)

    new_task = Tasks(name=name, group_id=group_id, tasks_count=tasks_count, 
                     deadline_timestamp=deadline_timestamp)

    db.session.add(new_task)
    db.session.commit()

    return {"ok": Messages.TASK_CREADTED}


@tasks.route('/<task_id>/delete', methods=['get'])
@Auth.admin_required
def _delete_(task_id):
    task = Tasks.query.filter_by(id=task_id).first()

    if not task:
        return {"error": Messages.TASK_NOT_FOUND.replace("<id>", task_id)}, 404

    Tasks.query.filter_by(id=task_id).delete()
    db.session.commit()

    return {"ok": Messages.TASK_DELETED}


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
        name = htmlentities.encode(name)
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


@tasks.route('/<task_id>/<action>/<number>', methods=['get'])
@Auth.logged_user
def _check_(task_id, action, number):
    if action != "check" and action != "uncheck":
        abort(404)

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

    if task.banned_solutions:
        banned_solutions = json.loads(task.banned_solutions)
        if banned_solutions.get(user_id):
            if number in banned_solutions[user_id]:
                return {"error": Messages.FORBIDDEN_SOLUTION}, 403

    if action == "check":
        if not solutions.get(user_id):
            solutions[user_id] = []

        if not number in solutions[user_id]:
            solutions[user_id].append(number)
    elif action == "uncheck":
        if solutions.get(user_id):
            if number in solutions[user_id]:
                solutions[user_id].remove(number)
            if len(solutions[user_id]) == 0:
                solutions.pop(user_id, None)

    task.solutions = json.dumps(solutions)
    db.session.commit()

    if action == "check": return {"ok": Messages.SOLUTION_CHECKED}
    else: return {"ok": Messages.SOLUTION_UNCHECKED}


@tasks.route('/solution/<action>', methods=['post'])
@Auth.admin_required
def _solution_remove_(action):
    if action != "remove" and action != "ban" and action != "unban":
        abort(404)

    post = request.get_json()

    task_id = post.get('task-id')
    user_id = post.get('user-id')
    solution = post.get('solution')

    if not task_id:
        return {"error": Messages.TASK_ID_REQUIRED}, 400

    if not user_id:
        return {"error": Messages.USER_ID_REQUIRED}, 400

    if not solution:
        return {"error": Messages.SOLUTION_NUMBER_REQUIRED}, 400

    task = Tasks.query.filter_by(id=task_id).first()

    if not task:
        return {"error": Messages.TASK_NOT_FOUND.replace("<id>", str(task_id))}, 404

    if not Users.query.filter_by(id=user_id).first():
        return {"error": Messages.USER_NOT_FOUND}, 404

    if solution > task.tasks_count:
        return {"error": Messages.SOLUTION_NOT_FOUND}, 404

    user_id = str(user_id)

    if action != "unban":
        if task.solutions:
            solutions = json.loads(task.solutions)
            if solutions.get(user_id):
                if solution in solutions[user_id]:
                    solutions[user_id].remove(solution)
                    if len(solutions[user_id]) == 0:
                        solutions.pop(user_id, None)

                    task.solutions = json.dumps(solutions)

    if action == "ban":
        banned_solutions = {}
        if task.banned_solutions:
            banned_solutions = json.loads(task.banned_solutions)

        if not banned_solutions.get(user_id):
            banned_solutions[user_id] = []

        if not solution in banned_solutions[user_id]:
            banned_solutions[user_id].append(solution)

        task.banned_solutions = json.dumps(banned_solutions)

    if action == "unban":
        if task.banned_solutions:
            banned_solutions = json.loads(task.banned_solutions)
            if banned_solutions.get(user_id):
                if solution in banned_solutions[user_id]:
                    banned_solutions[user_id].remove(solution)
                    if len(banned_solutions[user_id]) == 0:
                        banned_solutions.pop(user_id, None)
                    
                    task.banned_solutions = json.dumps(banned_solutions)

    db.session.commit()

    if action == "remove": return {"ok": Messages.SOLUTION_REMOVED}
    elif action == "ban": return {"ok": Messages.SOLUTION_BANNED}
    else: return {"ok": Messages.SOLUTION_UNBANNED}


@tasks.route('/my/<_type>', methods=['get'])
@Auth.logged_user
def _my_(_type):
    if _type != "current" and _type != "finished":
        abort(404)

    all_tasks = Tasks.query.all()
    user = Users.query.filter_by(id=session['user_id']).first()

    user_groups = []
    if user.groups:
        user_groups = json.loads(user.groups)

    to_return = []

    for task in all_tasks:
        if task.group_id in user_groups:
            correct_one = False
            if _type == "current" and task.deadline_timestamp > datetime.now().timestamp():
                correct_one = True
            if _type == "finished" and task.deadline_timestamp <= datetime.now().timestamp():
                correct_one = True

            if correct_one:
                task_report = {
                    "id": task.id,
                    "name": task.name,
                    "deadline": task.deadline_timestamp,
                    "points": 0,
                    "solutions": []
                }

                solutions = {}
                if task.solutions:
                    solutions = json.loads(task.solutions)

                banned_solutions = {}
                if task.banned_solutions:
                    banned_solutions = json.loads(task.banned_solutions)

                user_id = str(session['user_id'])
                points = calculete_task_points(solutions, task.tasks_count)

                for i in range(task.tasks_count):
                    s = {
                        "checked": False,
                        "banned": False,
                        "points": points[i]
                    }

                    if solutions.get(user_id):
                        if i + 1 in solutions[user_id]:
                            s['checked'] = True
                            task_report['points'] += points[i]

                    if banned_solutions.get(user_id):
                        if i + 1 in banned_solutions[user_id]:
                            s['banned'] = True

                    task_report['solutions'].append(s)
                
                to_return.append(task_report)
        
    return {"ok": to_return}