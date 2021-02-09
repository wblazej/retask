from flask import Blueprint, session
from database.models import Users
from lib.messages import Messages
from lib.auth import Auth

logout = Blueprint('logout', __name__)

@logout.route('', methods=['get'])
@Auth.logged_user
def _logout_():
    session.pop("logged_in", None)
    session.pop("user_id", None)

    return {"ok": Messages.LOGGED_OUT}