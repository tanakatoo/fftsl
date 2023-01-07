from flask import Blueprint, render_template, request, redirect, url_for, session,g
from functools import wraps
from models import User, School, Provider, Parent
from forms import PasswordResetForm, PasswordSetForm, LoginForm, UserRegisterForm
from config import CURR_USER_KEY
from general.general import flash_error,flash_success
from emails.emailing import signup_email

# have to import the model for this here

auth_bp = Blueprint('auth_bp', __name__,
    template_folder='templates', static_folder='static',static_url_path='/auth/static')



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
            flash_error('''Resetting your password failed. Either your email is not registered or you have not yet been verified.
                  Please signup first if you haven't registered, otherwise, please wait for our email
                  that will have a link for you to set your password if you have been verified as a legitimate business/school.
                  ''')
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
            flash_error(f'Trouble setting your password: {res[1]}')
            return redirect(url_for("general_bp.home")) 
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
                    flash_error("Email cannot be found. Please register before logging in.")
                    return redirect(url_for('general_bp.home'))
            else:
                flash_error('Password set/reset is expired. Please input email to obtain a new one.')
                return redirect(url_for('auth_bp.reset_password'))
        else:
            # code is incorrect
            flash_error("Link to reset your password is incorrect. Please reset your password again.")
            return redirect(url_for('general_bp.home'))

@auth_bp.route('/signup', methods=["GET","POST"])
def signup():
    form=UserRegisterForm()
    form_pass=PasswordSetForm()
    if form.validate_on_submit() and form_pass.validate_on_submit():
        res=User.register(user_type=form.user_type.data,email=form.email.data, pwd=form_pass.password.data)
    
        if res[0]:
            u=res[1]
            if form.user_type.data == 'school':
                res=School.register(name=request.form['establishment_name'], user_id=u.id)
                
                if not res[0]:
                    flash_error(f'Trouble registering school name: {res[1]}')
                    return redirect(url_for('general_bp.home'))
            elif form.user_type.data=='provider':
                res=Provider.register(user_id=u.id,name=request.form['establishment_name'])
            elif form.user_type.data=='parent':
                s=School.search_code(form.establishment_name.data)
                if s[0]:
                    s=s[1]
                    if not s is None:
                        # write school id in parent table
                        p=Parent.insert_parent(user_id=u.id,school_id=s.user_id)
                        if not p[0]:
                            flash_error(f'Trouble connecting you to the school: {p[1]}')
                            return url_for('signup')
                    else:
                        flash_error(f'Trouble finding school associated with your code. Please double check and try again.')
                        return url_for('signup')
            # call function to send email
            signup_email(u=u, establishment_name=form.establishment_name.data)
            # login and redirect
            do_login(u.id)
            if u.user_type=='school':
                return redirect(url_for('schools_bp.home'))
            elif u.user_type=='provider':
                return redirect(url_for('providers_bp.home'))
            elif u.user_type=='parent':
                return redirect(url_for('parents_bp.home'))
            elif u.user_type=='admin':
                return redirect(url_for('admin_bp.home'))
            # return redirect(url_for('email_bp.signup_email',u=u, establishment_name=form.establishment_name.data))
            
        else:
            # registration error
            flash_error(f"Trouble registering: {res[1]}")
            return url_for('signup')
        
    else:
        return render_template('signup.html', form=form, form_pass=form_pass)
    

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
            elif u.user_type=='parent':
                return redirect(url_for('parents_bp.home'))
            elif u.user_type=='admin':
                return redirect(url_for('admin_bp.home'))
        else:
            flash_error("Wrong credentials")
            return render_template('login.html',form=form)
    else:

        return render_template('login.html',form=form)

@auth_bp.route('/logout')
def logout():
    """Logout User"""
    do_logout()
    flash_success("You have successfully logged out.")
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
            flash_error("Please login.")
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
            flash_error(f"Please login.")
            return redirect(url_for('auth_bp.login'))
        else:
            if not g.user.user_type=="provider" and not g.user.user_type == "admin":
                flash_error(f"{g.user.user_type.upper()} profiles are not authorized to view the requested page.")
                # save referrer in session
                
                return redirect(url_for('general_bp.home'))
            return f(*args,**kws)
    return decorated_func

def check_is_school(f):
    """If we're logged in, add curr user to Flask global."""
    @wraps(f)
    def decorated_func(*args,**kws):
        if not CURR_USER_KEY in session:
            flash_error(f"Please login")
            return redirect(url_for('auth_bp.login'))
        else:
            if not g.user.user_type=="school" and not g.user.user_type == "admin":
                flash_error(f"{g.user.user_type.upper()} profiles are not authorized to view the requested page.")
                # save referrer in session
                
                return redirect(url_for('general_bp.home'))
            return f(*args,**kws)
    return decorated_func

def check_is_admin(f):
    """If we're logged in, add curr user to Flask global."""
    @wraps(f)
    def decorated_func(*args,**kws):
        if not CURR_USER_KEY in session:
            flash_error(f"Please login")
            return redirect(url_for('auth_bp.login'))
        else:
            if not g.user.user_type=="admin":
                flash_error(f"{g.user.user_type.upper()} profiles are not authorized to view the requested page.")
                # save referrer in session
                
                return redirect(url_for('general_bp.home'))
            return f(*args,**kws)
    return decorated_func