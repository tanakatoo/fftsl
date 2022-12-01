from flask import Blueprint, render_template, request, flash, redirect, url_for
from functools import wraps
from models import User, School

# have to import the model for this here

auth_bp = Blueprint('auth_bp', __name__,
    template_folder='templates', static_folder='static',static_url_path='/auth/static')
    # static_folder='static', static_url_path='assets')

# all go to the root of this, which is defined in app.py ('/products')
@auth_bp.route('/forgot_password')
def forgot_password():
    # products = Product.query.all()
    return render_template('forgot_password.html')

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
        

@auth_bp.route('/login')
def login():
    # products = Product.query.all()
    return render_template('login.html')

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
