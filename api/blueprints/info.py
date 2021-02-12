from flask import Blueprint, session
from database.models import Users

info = Blueprint('info', __name__)

@info.route('', methods=['get'])
def _info_():
    if not session.get("logged_in"):
        return {"error": "NOT_LOGGED_IN"} 

    user = Users.query.filter_by(id=session['user_id']).first()

    account_type = ''
    if user.username == 'root':
        account_type = 'root'
    elif user.admin:
        account_type = 'admin'
    else:
        account_type = 'user'

    return {
        "username": user.username,
        "type": account_type
    }