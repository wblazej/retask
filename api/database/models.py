from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# USERS DATABASE TABLE
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(192), nullable=False)
    groups = db.Column(db.String, nullable=True)
    admin = db.Column(db.Boolean, nullable=False)


# GROUPS DATABASE TABLE
class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(6), nullable=False)


# TASKS DATABASE TABLE
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    tasks_count = db.Column(db.Integer, nullable=False)
    deadline_timestamp = db.Column(db.Integer, nullable=False)
    solutions = db.Column(db.String, nullable=True)
    banned_solutions = db.Column(db.String, nullable=True)