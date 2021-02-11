from flask import Flask, session
from datetime import timedelta

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=60)

# database
from database.models import db
app = Flask(__name__)
app.config.from_object('database.config.Config')
db.app = app
db.init_app(app)
db.create_all()

# blueprints
from blueprints.init import init
from blueprints.login import login
from blueprints.logout import logout
from blueprints.users import users
from blueprints.groups import groups
from blueprints.tasks import tasks
from blueprints.info import info
app.register_blueprint(init, url_prefix='/api/init')
app.register_blueprint(login, url_prefix='/api/login')
app.register_blueprint(logout, url_prefix='/api/logout')
app.register_blueprint(users, url_prefix='/api/users')
app.register_blueprint(groups, url_prefix='/api/groups')
app.register_blueprint(tasks, url_prefix='/api/tasks')
app.register_blueprint(info, url_prefix='/api/info')

if __name__ == "__main__":
    app.debug = True
    app.run()