from flask import render_template
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


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

