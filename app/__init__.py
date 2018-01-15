from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models

# after setting the FLASK_APP env we can run the native Flask command 'flask run'
# the flask-migrate extension allows us to run 'flask db init' --> 'flask db migrate -m "migration message"' (run the migration script, optional message, does not actually change database *this is because it allows us to check the automatic generation before actually applying changes) --> flask db upgrade (or downgrade--applies migration script changes to database, if no db is found, it will be created)   **When working with MySQL or PostgreSQL you have to create the db in the db server before running the upgrade command