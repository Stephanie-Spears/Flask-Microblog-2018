import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('MICROBLOG_SECRET_KEY') or 'SecretKey2018'
    SQLALCHEMY_DATABASE_URI = os.environ.get('MICROBLOG_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('YMAIL_SERVER')
    MAIL_PORT = int(os.environ.get('YMAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('YMAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('YMAIL_USERNAME_ONE_ONE')
    MAIL_PASSWORD = os.environ.get('YMAIL_PASSWORD_ONE_ONE')
    ADMINS = [os.environ.get('YMAIL_USERNAME_ONE_ONE')]

