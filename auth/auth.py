from flask import Blueprint, render_template, request, flash, redirect, url_for, session,g
from functools import wraps
from models import User, School
from forms import PasswordReset, PasswordSet, Login, UserRegister

CURR_USER_KEY='curr_user'
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
        if u and u.active:
            # if it exists, generate token and send by email
            key=u.get_secret_key()

            # send email
            return redirect(url_for('email_bp.set_password_email',key=key,email=u.email))
        else:
            # u doens't exist or account has not yet been verified
            flash("""Resetting your password failed. Either your email is not registered or you have not yet been verified.
                  Please signup first if you haven't registered, otherwise, please wait for our email
                  that will have a link for you to set your password if you have been verified as a legitimate business/school.
                  """, "failure_bkg")
            return render_template('forgot_password.html', form=form)
    else:
        return render_template('forgot_password.html', form=form)   

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
            # set the user session
            do_login(u.id)
            if u.user_type == "school": 
                return redirect('/schools')
            elif u.user_type=="provider":
                return redirect('/providers')
            else:
                return redirect ('/browsing')
        else:
            # setting password returned an error
            msg=f"""<p>Sorry, there was an error setting your password. Please contact help@fftsl.ca with the following message:<p>
                    <p>{res[1]}"""
            return redirect(url_for("general_bp.system_message",msg=msg)) 
    else:
        # make sure they are not accessing the page by typing in the url
        if(request.args.get('key')):
            # verify that their token is correct
            res=User.confirm_secret_key(request.args.get('key'))
            if res[0]:    
                u=User.get_user(res[1]['email'])
                if u:
                    return render_template("set_password.html", form=form, email=u.email)
                else:
                    # cannot find email
                    msg="For some reason we couldn't find you registered in our system. Please contact help@fftsl.ca and we will get you sorted out."
                    return redirect(url_for("general_bp.system_message",msg=msg))
        else:
            # code is incorrect
            msg="The link you are trying to reach to reset your password is incorrect. Please contact help@fftsl.ca and we will get you sorted out."
            return render_template('unauthorized.html',msg=msg)

@auth_bp.route('/signup', methods=["GET","POST"])
def signup():
    form=UserRegister()
    if form.validate_on_submit():
        try:
            # when we can register parents, we need to add pwd to this

            u=User.register(user_type=form.user_type.data,email=form.email.data)
            print('*******')
            print(u)
            if request.form['user_type'] == 'school':
                s=School.register(name=request.form['school_name'])
                
            if u:
                return redirect(url_for('email_bp.signup_email',user_type=request.form['user_type'],email=request.form['email'], school_name=request.form.get('school_name')))
            else:
                flash('Not sure what happened in signup, but please contact help@fftsl.ca.', 'failure_bkg')
                return render_template('signup.html', form=form)
        except Exception as e:
            return e
            
    else:
        return render_template('signup.html', form=form)
    
    # if request.method=="GET":
    #     return render_template('signup.html')
    # else:
    #     # user input email and we want to register them first with a random password
    #     try:
    #         # when we can register parents, we need to add pwd to this

    #         u=User.register(user_type=request.form['user_type'],email=request.form['email'])
    #         if request.form['user_type'] == 'school':
    #             s=School.register(name=request.form['schoolName'])
                
    #         if u:
    #             return redirect(url_for('email_bp.signup_email',user_type=request.form['user_type'],email=request.form['email'], school_name=request.form.get('schoolName')))
    #         else:
    #             return "404 dude"
    #     except Exception as e:
    #         return e
        

@auth_bp.route('/login', methods=['POST','GET'])
def login():
    """Log in user."""
    form=Login()
    if form.validate_on_submit():
        u=User.authenticate(email=form.email.data,pwd=form.password.data)
        if u:
            do_login(u.id)

            if u.user_type=='school':
                return redirect('/schools')
            elif u.user_type=='provider':
                return redirect('/providers')
        else:
            flash("Wrong credentials. Please contact help@fftsl.ca if you are having trouble logging in.", "failure_bkg")
            return render_template('login.html',form=form)
    else:

        print(session.get(CURR_USER_KEY))
        return render_template('login.html',form=form)

@auth_bp.route('/logout')
def logout():
    """Logout User"""
    do_logout()
    flash("You have successfully logged out.", "success_bkg")
    return redirect('/')

def do_login(id):
    session[CURR_USER_KEY] = id
    
def do_logout():
     if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def check_login(f):
    """If we're logged in, add curr user to Flask global."""
    @wraps(f)
    def decorated_func(*args,**kws):
        if CURR_USER_KEY in session:
            g.user = User.query.get(session[CURR_USER_KEY])
        else:
            flash("You need to login first", "failure_bkg")
            g.user = None
            return redirect(url_for('auth_bp.login'))
        return f(*args,**kws)
    return decorated_func

# @app.before_request
# def add_user_to_g():
    # """If we're logged in, add curr user to Flask global."""

    # if CURR_USER_KEY in session:
    #     g.user = User.query.get(session[CURR_USER_KEY])

    # else:
    #     g.user = None



# def do_logout():
#     """Logout user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]

#make sure logged in user ia admin


# define decorators to logging in
# def login_check(f):
#     @wraps(f)
#     def decorated_func(*args,**kws):
#         # call model to check if user is logged in
#         print('in login check decorator')
#         print('check to see if user is logged in if so then return decorated function, other return error, like token wrong')
#         return f(*args,**kws)
#     return decorated_func

