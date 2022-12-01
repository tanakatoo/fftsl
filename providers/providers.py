from flask import Blueprint, render_template
# have to import the model for this here

providers_bp = Blueprint('providers_bp', __name__,
    template_folder='templates', static_folder='static')
    # static_folder='static', static_url_path='assets')

# all go to the root of this, which is defined in app.py ('/products')
@providers_bp.route('/')
def home():
    return render_template('providers_home.html')

@providers_bp.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')