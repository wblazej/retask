class Config:
    # you need to generate your own secret-key
    # it can be a random string
    SECRET_KEY = open('secret/secret-key', 'r').read()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/database.db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False