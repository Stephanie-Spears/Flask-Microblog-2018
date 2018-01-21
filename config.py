import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('MICROBLOG_SECRET_KEY') or 'SecretKey2018'
    SQLALCHEMY_DATABASE_URI = os.environ.get('MICROBLOG_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('GMAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT_TLS') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME_ONE_ONE')
    MAIL_PASSWORD = os.environ.get('GMAIL_ONE_ONE_APP_PASSWORD')

    ADMINS = [os.environ.get('GMAIL_USERNAME_ONE_ONE')]

    # Flask-Babel language code: en = English, es = Spanish, ja=Japanese
    LANGUAGES = ['en', 'es', 'ja', 'it', 'de', 'ru', 'fr']

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    POSTS_PER_PAGE = 15




# # FROM GITHUB

    # from Translator.mstranslator.client import MSTranslator
    #
    # from Translator.mstranslator.client import MSTranslatorAccessKey
    # # TEST FROM GITHUB CREDENTIALS
    # client_id = '263ee1af-8087-4592-bf85-5941238bdab6'
    # client_secret = 'jEd2T2wT0dcRaHECngyGfyplmq3PjKlZIaC1iIqfzMw='
    # MS_TRANSLATOR_KEY = MSTranslatorAccessKey(client_id, client_secret)
    # key = MS_TRANSLATOR_KEY
    #
    # SCOPE='http://api.microsofttranslator.com'
    # OAUTH_URL='https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
    # AZURE_TRANSLATE_API_URL='http://api.microsofttranslator.com/V2/Ajax.svc/Translate?%s'
    # TRANSLATE_ARRAY='http://api.microsofttranslator.com/V2/Http.svc/TranslateArray'
    # GRANT_CLIENT_CREDENTIALS_ONLY='client_credentials'
    # YOUR_APP_KEY ='263ee1af-8087-4592-bf85-5941238bdab6'
    # YOUR_APP_SECRET = 'jEd2T2wT0dcRaHECngyGfyplmq3PjKlZIaC1iIqfzMw='