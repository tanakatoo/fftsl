from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, RadioField
from wtforms.validators import InputRequired, Email, Length

class PasswordReset(FlaskForm):
    email=EmailField("Email", validators=[InputRequired(), Email()])

class PasswordSet(FlaskForm):
    password=PasswordField("New Password", validators=[InputRequired(),Length(min=8)])
    password_again=PasswordField("Please input password again", validators=[InputRequired(),Length(min=8)])
    
class UserRegister(FlaskForm):
    email=EmailField("Email", validators=[InputRequired(), Email()],id="email")
    user_type=RadioField("You are a: ",choices=[('provider','Provider'),('school','School')], default='provider')
    school_name=StringField("Name of School ", id="schoolName")
    
class Login(FlaskForm):
    email=EmailField("Email", validators=[InputRequired(), Email()])
    password=PasswordField("Password", validators=[InputRequired(),Length(min=8)])