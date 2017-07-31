# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2017, Paul Cunningham'

from os import path as op
from functools import update_wrapper, wraps
from flask import Flask, render_template, send_file, current_app, make_response
from flask_security import Security, SQLAlchemySessionUserDatastore, login_required, current_user
from database import db_session, init_db
from models import User, Role

# Create app
app = Flask(__name__, instance_path='D:/Paul/Documents/GitHub/flask-protected-resource/instance')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SECURITY_PASSWORD_SALT'] = '433e399b2f2f5c89e8dd8988a78a8a040023de58fcd7227e'


# https://gist.github.com/roshammar/8932394
def nocache(f):
    @wraps(f)
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        return resp
    return update_wrapper(new_func, f)


# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)


# Create a user to test with
@app.before_first_request
def create_user():
    init_db()
    _user = user_datastore.create_user(
        email='jane.smith@example.com',
        password='password',
        username='Jane Smith',
    )
    db_session.commit()


# Views
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')


@app.route('/unprotected')
def unprotected():
    return render_template('unprotected.html')


def get_instance_path(prefix, filename):
    return op.join(current_app.instance_path, prefix, filename)


@app.route('/resource/image/<string:filename>')
@nocache
def resource_image(filename):

    if not current_user.is_authenticated:
        return '', 204

    _image_path = get_instance_path('images', filename)

    if not op.isfile(_image_path):
        print "Image not found : {}".format(_image_path)
        return '', 204

    print "Serving image : {}".format(_image_path)

    return send_file(_image_path)


@app.route('/resource/css/<string:filename>')
@nocache
def resource_css(filename):
    # Deliver CSS files
    print filename
    return '', 204


@app.route('/resource/js/<string:filename>')
@nocache
def resource_js(filename):
    # Deliver JavaScript files
    print filename
    return '', 204


if __name__ == '__main__':
    app.run()

