from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from datetime import datetime



#  why there is no db.session.add() before the commit -> consider that when you reference current_user, Flask-Login will invoke the user loader callback function, which will run a database query that will put the target user in the database session. So you can add the user again in this function, but it is not necessary because it is already there.
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# the @app.route decorator creates an association between the URL given as an argument and the function
@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'So overcast today...'
        },
        {
            'author': {'username': 'Stephanie'},
            'body': 'Shut up, Susan.'
        }

    ]
    return render_template('index.html', title='Home', posts=posts)


# we use url_for instead of hardcoding links because if we decide to change the link name, we don't have to hunt down every instance we used. Urls are more likely to change names than our view function names. Also, some URLs have dynamic components, so generating those URLs by hand would be tedious/error prone
# The argument to url_for() (in this case, 'index') is the endpoint name, which is the name of the view function. So it tells it to redirect to the view function 'index()' which points to the explicit template name 'index.html'
# The top two lines in the login() function deal with a weird situation. Imagine you have a user that is logged in, and the user navigates to the /login URL of your application. Clearly that is a mistake, so I want to not allow that. The current_user variable comes from Flask-Login and can be used at any time during the handling to obtain the user object that represents the client of the request. The value of this variable can be a user object from the database (which Flask-Login reads through the user loader callback I provided above), or a special anonymous user object if the user did not log in yet. Remember those properties that Flask-Login required in the user object? One of those was is_authenticated, which comes in handy to check if the user is logged in or not. When the user is already logged in, I just redirect to the index page.
# The login_user() function comes from Flask-Login, it registers the user as logged in, so any future pages the user navigates to will have current_user variable set to that user
# Right after the user is logged in by calling Flask-Login's login_user() function, the value of the next query string argument is obtained. Flask provides a request variable that contains all the information that the client sent with the request. In particular, the request.args attribute exposes the contents of the query string in a friendly dictionary format.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


# This view function is slightly different to the other ones that process a form. If validate_on_submit() returns True I copy the data from the form into the user object and then write the object to the database. But when validate_on_submit() returns False it can be due to two different reasons. First, it can be because the browser just sent a GET request, which I need to respond by providing an initial version of the form template. It can also be when the browser sends a POST request with form data, but something in that data is invalid. For this form, I need to treat these two cases separately. When the form is being requested for the first time with a GET request, I want to pre-populate the fields with the data that is stored in the database, so I need to do the reverse of what I did on the submission case and move the data stored in the user fields to the form, as this will ensure that those form fields have the current data stored for the user. But in the case of a validation error I do not want to write anything to the form fields, because those were already populated by WTForms. To distinguish between these two cases, I check request.method, which will be GET for the initial request, and POST for a submission that failed validation.
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

