from flask import Blueprint, render_template, request, flash, redirect, url_for
from functools import wraps
from models import User, School
from forms import PasswordReset, PasswordSet


# have to import the model for this here

auth_bp = Blueprint('auth_bp', __name__,
    template_folder='templates', static_folder='static',static_url_path='/auth/static')
    # static_folder='static', static_url_path='assets')


# all go to the root of this, which is defined in app.py ('/products')
@auth_bp.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    form=PasswordReset()
    if form.validate_on_submit():
        # get the email and see if it's in the db
        u=User.get_user(form.email.data)
        if u:
            # if it exists, generate token and send by email
            key=u.get_secret_key()

            # send email
            return redirect(url_for('email_bp.set_password_email',key=key,email=u.email))
        else:
            # u doens't exist
            flash('Email is not registered. Please <a href="/signup">signup</a> first.', "failure_bkg")
            return render_template('forgot_password.html', form=form)
    else:
        return render_template('forgot_password.html', form=form)

# @auth_bp.route('/save_password')
# def save_password():
#     email
#     User.set_password(email=)
    

@auth_bp.route('/set_password',methods=['POST','GET'])
def set_password():
    form=PasswordSet()
    if form.validate_on_submit():
        email=request.form['email']
        pwd=request.form['password']
        # new password are good, save them to db
        res=User.set_password(email=email,pwd=pwd)
        if res[0]:
            u=res[1]
            if u.user_type == "school":
                return redirect('/schools')
            elif u.user_type=="provider":
                return redirect('/providers')
            else:
                return redirect ('/browsing')
        else:
            # setting password returned an error
            message=f"""<p>Sorry, there was an error setting your password. Please contact help@fftsl.ca with the following message:<p>
                    <p>{res[1]}"""
            return render_template("general_bp.message",msg=message) 
    else:
        # verify that their token is correct
        res=User.confirm_secret_key(request.args['key'])
        if res[0]:    
            u=User.get_user(res[1]['email'])
            if u:
                return render_template("set_password.html", form=form, email=u.email)
            else:
                # cannot find email
                message="For some reason we couldn't find you registered in our system. Please contact help@fftsl.ca and we will get you sorted out."
                return render_template("general_bp.message",msg=message)
        else:
            # code is incorrect
            message="The link you are trying to reach to reset your password is incorrect. Please contact help@fftsl.ca and we will get you sorted out."
            return render_template('unauthorized.html',msg=message)

@auth_bp.route('/signup', methods=["GET","POST"])
def signup():
    if request.method=="GET":
        return render_template('signup.html')
    else:
        # user input email and we want to register them first with a random password
        try:
            # when we can register parents, we need to add pwd to this

            u=User.register(user_type=request.form['user_type'],email=request.form['email'])
            if request.form['user_type'] == 'school':
                s=School.register(name=request.form['schoolName'])
                
            if u:
                return redirect(url_for('email_bp.signup_email',user_type=request.form['user_type'],email=request.form['email'], school_name=request.form.get('schoolName')))
            else:
                return "404 dude"
        except Exception as e:
            return e
        

# @auth_bp.route('/login')
# def login():
#     # products = Product.query.all()
#     return render_template('login.html')

# def do_login(user):
#     """Log in user."""

#     session[CURR_USER_KEY] = user.id


# def do_logout():
#     """Logout user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]

#make sure logged in user ia admin


# define decorators to logging in
def login_check(f):
    @wraps(f)
    def decorated_func(*args,**kws):
        # call model to check if user is logged in
        print('in login check decorator')
        print('check to see if user is logged in if so then return decorated function, other return error, like token wrong')
        return f(*args,**kws)
    return decorated_func

@login_check
def name():
    print("Alice")
