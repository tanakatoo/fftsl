from flask import Blueprint, render_template
from auth.auth import auth_bp, check_login
# have to import the model for this here



schools_bp = Blueprint('schools_bp', __name__,
    template_folder='templates', static_folder='static')
    # static_folder='static', static_url_path='assets')

# all go to the root of this, which is defined in app.py ('/products')
@schools_bp.route('/')
@check_login
def home():
    # products = Product.query.all()
    return render_template('schools_home.html')