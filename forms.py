from flask_wtf import FlaskForm
from wtforms import SelectField,StringField, EmailField, PasswordField, RadioField, TextAreaField, IntegerField, BooleanField, DecimalField, HiddenField
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
    address=StringField("Address", id="address")
    city_id=SelectField("City")
    province_id=SelectField("Province")
    contact_name=StringField("Contact Name")
    phone=StringField("Phone Number")
    sales_pitch=TextAreaField("Sales pitch:")
    active=BooleanField("Account active", default=True)
    geocode_lat=HiddenField("Whylat", id="geolat")
    geocode_long=HiddenField("Whylong", id="geolong")
    
class MenuInfo(FlaskForm):
    name=StringField("Name of dish")
    recipe=TextAreaField("Recipe for nutrition calculation")
    num_servings=IntegerField("How many servings does this dish have?")
    ingred_disp=TextAreaField("Recipe to display")
    price=DecimalField("Price per serving")
    sales_pitch=TextAreaField("What is special about your dish? Sell it here!")
    pass_guidelines=BooleanField("Pass ministry guidelines")
    max_meals=IntegerField("Maximum number of servings of this dish you can provide for one organization at one time")
    related_to_dish=SelectField("Related to dish")

    
    
class Settings(FlaskForm):
    max_meals_per_day=IntegerField("Maximum number of meals you can provide at one time to one organization", validators=[NumberRange(min=0)])
    min_meals=IntegerField("Minimum number of meals you will provide to one organization", validators=[NumberRange(min=0)])
    serve_num_org_per_day=IntegerField("How many organizations can you serve per day?", validators=[NumberRange(min=0)])