from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


# the @app.route decorator creates an association between the URL given as an argument and the function
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Stephanie'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)


# we use url_for instead of hardcoding links because if we decide to change the link name, we don't have to hunt down every instance we used. Urls are more likely to change names than our view function names. Also, some URLs have dynamic components, so generating those URLs by hand would be tedious/error prone
# The argument to url_for() (in this case, 'index') is the endpoint name, which is the name of the view function. So it tells it to redirect to the view function 'index()' which points to the explicit template name 'index.html'
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

