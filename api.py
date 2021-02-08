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
app.register_blueprint(init, url_prefix='/api/init')
app.register_blueprint(login, url_prefix='/api/login')
app.register_blueprint(logout, url_prefix='/api/logout')

if __name__ == "__main__":
    app.debug = True
    app.run()