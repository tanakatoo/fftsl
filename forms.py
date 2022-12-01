from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class PasswordReset(FlaskForm):
    email=EmailField("Email", validators=[InputRequired(), Email()])

class PasswordSet(FlaskForm):
    password=PasswordField("New Password", validators=[InputRequired(),Length(min=8)])
    password_again=PasswordField("Please input password again", validators=[InputRequired(),Length(min=8)])
