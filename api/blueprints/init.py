from flask import Blueprint
from database.models import db
from database.models import Users
from lib.messages import Messages
from lib.hash import Hash

init = Blueprint('init', __name__)

@init.route('', methods=['get'])
def _init_():
    if Users.query.filter_by(username="root").first() == None:
        pwd = Hash.hash_password("root")
        admin_account = Users(username="root", password=pwd, admin=True)
        db.session.add(admin_account)
        db.session.commit()

        return {"ok": Messages.DEFAULT_ROOT_LOGIN}
    else:
        return {"error": Messages.APP_INITIALIZED}, 403

@init.route('/check', methods=['get'])
def _init_check_():
    if Users.query.filter_by(username="root").first() == None:
        return {"ok": False}
    else:
        return {"ok": True}