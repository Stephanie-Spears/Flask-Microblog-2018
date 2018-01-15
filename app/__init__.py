from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
# The 'login' value above is the function (or endpoint) name for the login view. In other words, the name you would use in a url_for() call to get the URL.

from app import routes, models

# after setting the FLASK_APP env we can run the native Flask command 'flask run'
# 'flask shell' will run a python shell in context to the program-->you don't have to explicitly type imports into the prompt. It also allows you to configure the 'shell context,' which is a list of other symbols to pre-import. This is done in 'microblog.py'
# the flask-migrate extension allows us to run 'flask db init' --> 'flask db migrate -m "migration message"' (run the migration script, optional message, does not actually change database *this is because it allows us to check the automatic generation before actually applying changes) --> flask db upgrade (or downgrade--applies migration script changes to database, if no db is found, it will be created)   **When working with MySQL or PostgreSQL you have to create the db in the db server before running the upgrade command

# Flask-Login requires these items to be added to model:
#   is_authenticated -> True if the user has valid credentials, False otherwise
#   is_active -> True if the user's account is active, False otherwise
#   is_anonymous -> False for regular users, True for a special anonymous user
#   get_id() -> a method that returns a unique identifier for the user as a string
# Flask-Login provides a "mixin" class called UserMixin that includes generic implementation for most user model classes.