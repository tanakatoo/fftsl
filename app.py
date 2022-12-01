from flask import Flask, request, jsonify, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
import os
from config import DevConfig,ProdConfig


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
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True not sure why this is not working

connect_db(app)

db.create_all()

# register blueprints
app.register_blueprint(general_bp,url_prefix='/')
app.register_blueprint(providers_bp, url_prefix='/providers')
app.register_blueprint(auth_bp,url_prefix='/')
app.register_blueprint(email_bp,url_prefix='/')
app.register_blueprint(parents_bp, url_prefix='/parents')
app.register_blueprint(schools_bp, url_prefix='/schools')


#@email_bp.route('/email')
# def test_email():
#     msg = Message('Twilio SendGrid Test Email', recipients=['recipient@example.com'])
#     msg.body = 'This is a test email!'
#     msg.html = '<p>This is a test email!</p>'
#     mail.send(msg)




