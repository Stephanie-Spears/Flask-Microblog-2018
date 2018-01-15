import os


class Config(object):
    SECRET_KEY = os.environ.get('MICROBLOG_SECRET_KEY') or 'SecretKey2018'

