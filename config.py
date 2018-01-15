import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('MICROBLOG_SECRET_KEY') or 'SecretKey2018'
    SQLALCHEMY_DATABASE_URI = os.environ.get('MICROBLOG_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

