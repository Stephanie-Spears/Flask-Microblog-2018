import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('MICROBLOG_SECRET_KEY') or 'SecretKey2018'
    SQLALCHEMY_DATABASE_URI = os.environ.get('MICROBLOG_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('GMAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT_TLS') or 25)


    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None

    # MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME_ONE_ONE')
    # MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD_ONE_ONE')
    MAIL_PASSWORD = os.environ.get('GMAIL_ONE_ONE_APP_PASSWORD')


    ADMINS = [os.environ.get('GMAIL_USERNAME_ONE_ONE')]

    POSTS_PER_PAGE = 5

