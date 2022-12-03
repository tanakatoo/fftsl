from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, RadioField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Email, Length, NumberRange

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
    
class ProviderInfo(FlaskForm):
    name=StringField("Name of Restaurant/Caterer")
    address=StringField("Address")
    city=StringField("City")
    province=StringField("Province")
    contact_name=StringField("Contact Name")
    phone=StringField("Phone Number")
    email=EmailField("Email")
    sales_pitch=TextAreaField("Sales Pitch for Company")
    max_meals_per_day=IntegerField("Maximum number of meals you can provide at one time to one organization", validators=[NumberRange(min=0)])
    min_meals=IntegerField("Minimum number of meals you will provide to one organization", validators=[NumberRange(min=0)])
    serve_num_org_per_day=IntegerField("How many organizations can you serve per day?", validators=[NumberRange(min=0)])
    active=BooleanField("Deactivate account")