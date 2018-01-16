from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login
from hashlib import md5


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


# The User class created inherits from db.Model, a base class for all models from Flask-SQLAlchemy.
# For a one-to-many relationship, a db.relationship field is normally defined on the "one" side, and is used as a convenient way to get access to the "many". So if I have a user stored in u, the expression u.posts will run a database query that returns all the posts written by that user.
# The first argument to db.relationship indicates the class that represents the "many" side of the relationship. The backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object. This will add a post.author expression that will return the user given a post. The lazy argument defines how the database query for the relationship will be issued
# The lazy = 'dynamic' is special and can be useful if you have many items and always want to apply additional SQL filters to them. Instead of loading the items SQLAlchemy will return another query object which you can further refine before loading the items. Note that this cannot be turned into a different loading strategy when querying so it’s often a good idea to avoid using this in favor of lazy=True. A query object equivalent to a dynamic user.addresses relationship can be created using Address.query.with_parent(user) while still being able to use lazy or eager loading on the relationship itself as necessary.

# Flask-Login requires these items to be added to model:
#   is_authenticated -> True if the user has valid credentials, False otherwise
#   is_active -> True if the user's account is active, False otherwise
#   is_anonymous -> False for regular users, True for a special anonymous user
#   get_id() -> a method that returns a unique identifier for the user as a string
# Flask-Login provides a "mixin" class called UserMixin that includes generic implementation for most user model classes.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()

        domain_suffix = [
            "gmail.com",
            "yahoo.com",
            "aol.com",
            "hotmail.com",
        ]
        for domain in domain_suffix:
            if (self.email).endswith(domain):
                return 'http://www.gravatar.com/avatar/{}s?d=mm&s={}d'.format(digest, size)
            else:
                return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
        # return 'http://www.gravatar.com/avatar/{}s?d=mm&s={}d'.format(digest, size)

        # has_gravatar = 'http://www.gravatar.com/avatar/{}s?d=mm&s={}d'.format(digest, size)
        # no_gravatar = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
        # return has_gravatar

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


# The user loader is registered with Flask-Login with the @login.user_loader decorator. The id that Flask-Login passes to the function as an argument is going to be a string, so databases that use numeric IDs need to convert the string to integer.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# When you pass a function as a default, SQLAlchemy will set the field to the value of calling that function (note the missing () after utcnow, so I'm passing the function itself, and not the result of calling it). In general, you will want to work with UTC dates and times in a server application for uniform conversions.
# The user_id field is initialized as a foreign key to user.id, which means that it references an id value from the users table. In this reference the user is the name of the database table, which Flask-SQLAlchemy automatically sets to the name of the model class converted to lowercase.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)



