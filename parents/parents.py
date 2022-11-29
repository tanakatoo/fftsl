from flask import Blueprint, render_template
# have to import the model for this here

parents_bp = Blueprint('parents_bp', __name__,
    template_folder='templates', static_folder='static')
    # static_folder='static', static_url_path='assets')

# all go to the root of this, which is defined in app.py ('/products')
@parents_bp.route('/')
def home():
    # products = Product.query.all()
    return render_template('parents_home.html')