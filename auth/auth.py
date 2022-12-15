from flask import Blueprint, render_template, request, flash, redirect, url_for, session,g
from functools import wraps
from models import User, School
from forms import PasswordResetForm, PasswordSetForm, LoginForm, UserRegisterForm
from config import CURR_USER_KEY

# have to import the model for this here

auth_bp = Blueprint('auth_bp', __name__,
    template_folder='templates', static_folder='static',static_url_path='/auth/static')
    # static_folder='static', static_url_path='assets')


# all go to the root of this, which is defined in app.py ('/products')
@auth_bp.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    form=PasswordResetForm()
    if form.validate_on_submit():
        # get the email and see if it's in the db
        u=User.get_user(email=form.email.data)
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
    form=PasswordSetForm()
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
                return redirect('/schools/dashboard')
            elif u.user_type=="provider":
                return redirect('/providers/dashboard')
            else:
                return redirect ('/browsing')
        else:
            # setting password returned an error
            session['msg']=f"""<p>Sorry, there was an error setting your password. Please contact help@fftsl.ca with the following message:<p>
                    <p>{res[1]}"""
            return redirect(url_for("general_bp.system_message")) 
    else:
        # make sure they are not accessing the page by typing in the url
        if(request.args.get('key')):
            # verify that their token is correct
            res=User.confirm_secret_key(request.args.get('key'))
            if res[0]:    
                u=User.get_user(email=res[1]['email'])
                if u:
                    return render_template("set_password.html", form=form, email=u.email)
                else:
                    # cannot find email
                    flash("For some reason we couldn't find you registered in our system. Please contact help@fftsl.ca and we will get you sorted out.",'failure_bkg')
                    return redirect(url_for('general_bp.home'))
            else:
                flash('Password set/reset has been expired. Please input email to obtain a new one', 'failure_bkg')
                # session['msg']="For some reason we couldn't find you registered in our system. Please contact help@fftsl.ca and we will get you sorted out."
                return redirect(url_for('auth_bp.reset_password'))
        else:
            # code is incorrect
            flash("The link you are trying to reach to reset your password is incorrect. Please contact help@fftsl.ca and we will get you sorted out.",'failure_bkg')
            return redirect(url_for('general_bp.home'))

@auth_bp.route('/signup', methods=["GET","POST"])
def signup():
    form=UserRegisterForm()
    if form.validate_on_submit():
        try:
            # when we can register parents, we need to add pwd to this

            res=User.register(user_type=form.user_type.data,email=form.email.data)
            if res[0]:
                u=res[1]
                if request.form['user_type'] == 'school':
                    res=School.register(name=request.form['school_name'], user_id=u.id)
                    
                    if res[0]:
                        s=res[1]
                    else:
                        flash(f'Sorry, the following error occurred while registering the school name. Please contact help@fftsl.ca. {res[1]}')
                        return redirect(url_for('general_bp.home'))
                    
                if u:
                    return redirect(url_for('email_bp.signup_email',user_type=request.form['user_type'],email=request.form['email'], school_name=request.form.get('school_name')))
                else:
                    flash('Not sure what happened in signup, but please contact help@fftsl.ca.', 'failure_bkg')
                    return render_template('signup.html', form=form)
            else:
                # registration error
                flash(f"Sorry the following error occurred while registering you. Please contact help@fftsl.ca. {res[1]}")
                return redirect('/')
        except Exception as e:
            # error 
            flash(f"Sorry the following error occurred while registering you. Please contact help@fftsl.ca. {res[1]}")
            return redirect(url_for('general_bp.home'))
            
    else:
        return render_template('signup.html', form=form)
    

@auth_bp.route('/login', methods=['POST','GET'])
def login():
    """Log in user."""
    form=LoginForm()
    if form.validate_on_submit():
        u=User.authenticate(email=form.email.data,pwd=form.password.data)
        if u:
            do_login(u.id)

            if u.user_type=='school':
                return redirect(url_for('schools_bp.home'))
            elif u.user_type=='provider':
                return redirect(url_for('providers_bp.home'))
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
    return redirect(url_for('general_bp.home'))

def do_login(id):
    """Add user session"""
    session[CURR_USER_KEY] = id
    
def do_logout():
    """Remove user session"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def check_login(f):
    """If we're logged in, add curr user to Flask global."""
    @wraps(f)
    def decorated_func(*args,**kws):
        if CURR_USER_KEY in session:
            g.user = User.get_user(id=session[CURR_USER_KEY])
        else:
            flash("You need to login first", "failure_bkg")
            g.user = None
            # save referrer in session
            
            return redirect(url_for('auth_bp.login'))
        return f(*args,**kws)
    return decorated_func

def check_is_provider(f):
    """If we're logged in, add curr user to Flask global."""
    @wraps(f)
    def decorated_func(*args,**kws):
        if not CURR_USER_KEY in session:
            flash(f"You are not logged in.", "failure_bkg")
            return redirect(url_for('auth_bp.login'))
        else:
            if not g.user.user_type=="provider":
                flash(f"You are not authorized to view this page {g.user.user_type}", "failure_bkg")
                # save referrer in session
                
                return redirect(url_for('general_bp.home'))
            return f(*args,**kws)
    return decorated_func

def check_is_school(f):
    """If we're logged in, add curr user to Flask global."""
    @wraps(f)
    def decorated_func(*args,**kws):
        if not CURR_USER_KEY in session:
            flash(f"You are not logged in.", "failure_bkg")
            return redirect(url_for('auth_bp.login'))
        else:
            if not g.user.user_type=="school":
                flash(f"You are not authorized to view this page {g.user.user_type}", "failure_bkg")
                # save referrer in session
                
                return redirect(url_for('general_bp.home'))
            return f(*args,**kws)
    return decorated_func

def check_is_admin(f):
    """If we're logged in, add curr user to Flask global."""
    @wraps(f)
    def decorated_func(*args,**kws):
        if not CURR_USER_KEY in session:
            flash(f"You are not logged in.", "failure_bkg")
            return redirect(url_for('auth_bp.login'))
        else:
            if not g.user.user_type=="admin":
                flash(f"You are not authorized to view this page {g.user.user_type}", "failure_bkg")
                # save referrer in session
                
                return redirect(url_for('general_bp.home'))
            return f(*args,**kws)
    return decorated_func