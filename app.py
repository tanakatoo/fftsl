from flask import Flask, request, jsonify, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
import os
from dotenv import load_dotenv, find_dotenv

# import blueprints
from providers.providers import providers_bp
from auth.auth import auth_bp
from general.general import general_bp
from parents.parents import parents_bp
from schools.schools import schools_bp


app = Flask(__name__)
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True not sure why this is not working

# register blueprints
app.register_blueprint(general_bp)
app.register_blueprint(providers_bp, url_prefix='/providers')
app.register_blueprint(auth_bp)
app.register_blueprint(parents_bp, url_prefix='/parents')
app.register_blueprint(schools_bp, url_prefix='/schools')

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///fftsl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
app.debug=True
debug=DebugToolbarExtension(app)

connect_db(app)

