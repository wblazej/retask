from flask import Blueprint, session
from database.models import Users
from lib.messages import Messages

logout = Blueprint('logout', __name__)

@logout.route('', methods=['get'])
def _logout_():
    if not session.get("logged_in"):
        return {"error": Messages.NOT_LOGGED_IN}

    session.pop("logged_in", None)
    session.pop("user_id", None)

    return {"ok": Messages.LOGGED_OUT}