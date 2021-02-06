from flask import Flask

app = Flask(__name__)

# database
from database.models import db
app = Flask(__name__)
app.config.from_object('database.config.Config')
db.app = app
db.init_app(app)
db.create_all()

# blueprints
from blueprints.init import init
app.register_blueprint(init, url_prefix='/api/init')

if __name__ == "__main__":
    app.debug = True
    app.run()