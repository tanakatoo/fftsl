from flask_wtf import FlaskForm
from wtforms import FormField, DateField, widgets, SelectMultipleField, SelectField,StringField, EmailField, PasswordField, RadioField, TextAreaField, IntegerField, BooleanField, DecimalField, HiddenField
from wtforms.validators import InputRequired, Email, Length, NumberRange, Optional

class PasswordResetForm(FlaskForm):
    email=EmailField("Email", validators=[InputRequired(), Email()])

class PasswordSetForm(FlaskForm):
    password=PasswordField("New Password", id="password",validators=[InputRequired(),Length(min=8)])
    password_again=PasswordField("Please input password again", id="passwordConfirm",validators=[InputRequired(),Length(min=8)])
    
class UserRegisterForm(FlaskForm):
    email=EmailField("Email", validators=[InputRequired(), Email()],id="email")
    user_type=RadioField("You are a: ",choices=[('provider','Provider'),('school','School'),('parent','Parent')], default='provider')
    school_name=StringField("Name of School ", id="schoolName")
    
class LoginForm(FlaskForm):
    email=EmailField("Email", validators=[InputRequired(), Email()])
    password=PasswordField("Password", validators=[InputRequired(),Length(min=8)])
    
class ProviderInfoForm(FlaskForm):
    name=StringField("Name of Restaurant/Caterer", validators=[InputRequired()])
    website=StringField("Website")
    address=StringField("Address", id="address")
    city_id=SelectField("City", coerce=int, validate_choice=False)
    province_id=SelectField("Province", coerce=int, validate_choice=False)
    contact_name=StringField("Contact Name")
    phone=StringField("Phone Number")
    sales_pitch=TextAreaField("Sales pitch")
    active=BooleanField("Account active")
    geocode_lat=StringField("Latitude",id="geolat", validators=[Optional()])
    geocode_long=StringField("Longtitude", id="geolong", validators=[Optional()])
    submit_inspection=HiddenField(id='submit_inspection')
    inspection_report=StringField("Inspection Report", id="inspection_report")
    max_meals_per_day=StringField("Maximum number of meals you can provide at one time to one organization")
    min_meals=StringField("Minimum number of meals you will provide to one organization")
    serve_num_org_per_day=StringField("How many organizations can you serve per day?")
    dates=HiddenField(id="dates_avail")
    recurring_dates=HiddenField(id="recurring_dates")
    # @classmethod
    # def add_cuisines_fields(cls, cform):
    #     cls.cuisines = FormField(cform)
    # geocode_lat=HiddenField(id="geolat")
    # geocode_long=HiddenField(id="geolong")

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    # prefix_label is to render label before the checkbox
    option_widget = widgets.CheckboxInput()
    
class CuisineForm(FlaskForm):
    cuisines = MultiCheckboxField('Cuisine', coerce=int, validate_choice=False)

class RestrictionForm(FlaskForm):
    restrictions=MultiCheckboxField('Restriction', coerce=int, validate_choice=False)

class DaysForm(FlaskForm):
    days = RadioField('Available every', coerce=int, validate_choice=False)
    
class CategoryForm(FlaskForm):
    categories = RadioField('Category', coerce=int, validate_choice=False)
    
class DishInfoForm(FlaskForm):
    name=StringField("Name of dish", validators=[InputRequired()])
    recipe=TextAreaField("Recipe for nutrition calculation")
    num_servings=IntegerField("How many servings is this recipe?",validators=[NumberRange(min=0),Optional(strip_whitespace=True)])
    ingred_disp=TextAreaField("Recipe to display")
    price=DecimalField("Price per serving", validators=[NumberRange(min=0),Optional(strip_whitespace=True)])
    sales_pitch=TextAreaField("What is special about your dish? Sell it here!")
    pass_guidelines=BooleanField("Pass ministry guidelines", id="guidelines")
    max_meals=IntegerField("Maximum number of servings of this dish you can provide for one organization at one time",validators=[NumberRange(min=0), Optional(strip_whitespace=True)])
    related_to_dish=SelectField("Related to dish")
    active=BooleanField("Active")
    
  
class SchoolInfoForm(FlaskForm):
    name=StringField("Name of School", validators=[InputRequired()])
    address=StringField("Address", id="address")
    city_id=SelectField("City", coerce=int, validate_choice=False)
    province_id=SelectField("Province", coerce=int, validate_choice=False)
    principal_name=StringField("Name of Principal")
    contact_name=StringField("Contact Name")
    phone=StringField("Phone Number")
    active=BooleanField("Account active", default=True)
    geocode_lat=StringField("Latitude",id="geolat", validators=[Optional()])
    geocode_long=StringField("Longtitude", id="geolong", validators=[Optional()])
    
    dates=HiddenField(id="dates_avail")
    recurring_dates=HiddenField(id="recurring_dates")
