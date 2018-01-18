import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
# The 'login' value above is the function (or endpoint) name for the login view. In other words, the name you would use in a url_for() call to get the URL.
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
# We run pybabel to extract the texts we've wrapped with the lazy_gettext function (as '_l') into a separate file:
# # pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .

# The pybabel init command takes the .pot file as input and writes a new language catalog to the directory given in the -d command line option for the language specified in the -l option. By default, Babel expects the translations to be in a translations folder at the same level as the templates, so that's where we'll put them.
# The command can be executed multiple times with different language codes to add support for other languages.
# # pybabel init -i messages.pot -d app/translations -l es

# Once the texts have been translated and saved back to the messages.po file there is yet another step to publish these texts. The pybabel compile step just reads the contents of the .po file and writes a compiled version as a .mo (Machine Object) file in the same directory:
# # pybabel compile -d app/translations

# if you don't feel like messing with your browser configuration you can also fake it by temporarily changing the localeselector function to always request Spanish (file app/views.py):
# # @babel.localeselector
# # def get_locale():
# #    return 'es'  # request.accept_languages.best_match(LANGUAGES.keys())

# To update translation files:
# # pybabel extract -F babel.cfg -o messages.pot app
# # pybabel update -i messages.pot -d app/translations


if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


from app import routes, models, errors


# after setting the FLASK_APP env we can run the native Flask command 'flask run'
# 'flask shell' will run a python shell in context to the program-->you don't have to explicitly type imports into the prompt. It also allows you to configure the 'shell context,' which is a list of other symbols to pre-import. This is done in 'microblog.py'
# the flask-migrate extension allows us to run 'flask db init' --> 'flask db migrate -m "migration message"' (run the migration script, optional message, does not actually change database *this is because it allows us to check the automatic generation before actually applying changes) --> flask db upgrade (or downgrade--applies migration script changes to database, if no db is found, it will be created)   **When working with MySQL or PostgreSQL you have to create the db in the db server before running the upgrade command

# Flask-Login requires these items to be added to model:
#   is_authenticated -> True if the user has valid credentials, False otherwise
#   is_active -> True if the user's account is active, False otherwise
#   is_anonymous -> False for regular users, True for a special anonymous user
#   get_id() -> a method that returns a unique identifier for the user as a string
# Flask-Login provides a "mixin" class called UserMixin that includes generic implementation for most user model classes.

