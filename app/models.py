from datetime import datetime
from app import db


# The User class created inherits from db.Model, a base class for all models from Flask-SQLAlchemy.
# For a one-to-many relationship, a db.relationship field is normally defined on the "one" side, and is used as a convenient way to get access to the "many". So if I have a user stored in u, the expression u.posts will run a database query that returns all the posts written by that user.
# The first argument to db.relationship indicates the class that represents the "many" side of the relationship. The backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object. This will add a post.author expression that will return the user given a post. The lazy argument defines how the database query for the relationship will be issued
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


# When you pass a function as a default, SQLAlchemy will set the field to the value of calling that function (note the missing () after utcnow, so I'm passing the function itself, and not the result of calling it). In general, you will want to work with UTC dates and times in a server application for uniform conversions.
# The user_id field is initialized as a foreign key to user.id, which means that it references an id value from the users table. In this reference the user is the name of the database table, which Flask-SQLAlchemy automatically sets to the name of the model class converted to lowercase.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)