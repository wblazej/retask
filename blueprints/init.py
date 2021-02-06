from flask import Blueprint
from database.models import db
from database.models import Users

init = Blueprint('init', __name__)

@init.route('', methods=['get'])
def _init_():
    if Users.query.filter_by(username="admin").first() == None:
        admin_account = Users(username="admin", password="admin", admin=True)
        db.session.add(admin_account)
        db.session.commit()

        return {"ok": "App initialized, root account - admin:admin"}
    else:
        return {"error": "App is already initialized"}