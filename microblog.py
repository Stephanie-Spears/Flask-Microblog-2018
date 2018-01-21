from app import create_app, db, cli
from app.models import User, Post


app = create_app()
cli.register(app)

# set context for 'flask shell' to pre-import the db instance and models to the shell session. The function returns a dictionary and not a list because for each item you have to also provide a name under which it will be referenced in shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
