import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('MICROBLOG_SECRET_KEY') or 'SecretKey2018'
    SQLALCHEMY_DATABASE_URI = os.environ.get('MICROBLOG_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    MAIL_SERVER = os.environ.get('GMAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT_TLS') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME_ONE_ONE')
    MAIL_PASSWORD = os.environ.get('GMAIL_ONE_ONE_APP_PASSWORD')

    ADMINS = [os.environ.get('GMAIL_USERNAME_ONE_ONE')]

    # Flask-Babel language code: en = English, es = Spanish, ja=Japanese, it=Italian, de=German, fr=French
    LANGUAGES = ['en', 'es', 'ja', 'it', 'de', 'ru', 'fr']

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    #run 'elasticsearch' in terminal, then diff terminal 'flask run'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    POSTS_PER_PAGE = 10