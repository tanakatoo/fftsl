from flask import Blueprint, render_template
# have to import the model for this here

auth_bp = Blueprint('auth_bp', __name__,
    template_folder='templates', static_folder='static')
    # static_folder='static', static_url_path='assets')

# all go to the root of this, which is defined in app.py ('/products')
@auth_bp.route('/forgot_password')
def forgot_password():
    # products = Product.query.all()
    return render_template('forgot_password.html')

@auth_bp.route('/signup')
def signup():
    # products = Product.query.all()
    return render_template('signup.html')

@auth_bp.route('/login')
def login():
    # products = Product.query.all()
    return render_template('login.html')