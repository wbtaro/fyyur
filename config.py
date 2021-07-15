import os

class Config(object):
    SECRET_KEY = os.urandom(32)
    # Grabs the folder where the script runs.
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Enable debug mode.
    DEBUG = True

    # Connect to the database
    SQLALCHEMY_DATABASE_URI = 'postgresql://ryotaro:passw0rd@localhost:5432/fyyur'
