from flask import Flask, request, jsonify, redirect, render_template, flash, session,g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
import os
from config import DevConfig, CURR_USER_KEY
from models import User


# import blueprints
from providers.providers import providers_bp
from auth.auth import auth_bp
from general.general import general_bp
from parents.parents import parents_bp
from schools.schools import schools_bp
from emails.emailing import email_bp


app = Flask(__name__)
app.debug=True
app.config.from_object(DevConfig)
debug=DebugToolbarExtension(app)
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

connect_db(app)

db.create_all()

# register blueprints
app.register_blueprint(general_bp,url_prefix='/')
app.register_blueprint(providers_bp, url_prefix='/providers')
app.register_blueprint(auth_bp,url_prefix='/')
app.register_blueprint(email_bp,url_prefix='/')
app.register_blueprint(parents_bp, url_prefix='/parents')
app.register_blueprint(schools_bp, url_prefix='/schools')


# global functions


@app.before_request
def add_user_to_g():
    """Runs before every request - even in blueprint
    If we're logged in, add curr user to Flask global."""
    
    if CURR_USER_KEY in session:
        g.user = User.get_user(id=session[CURR_USER_KEY])
    else:
        g.user = None

