from flask import Blueprint, render_template, g
from auth.auth import check_login
# have to import the model for this here

providers_bp = Blueprint('providers_bp', __name__,
    template_folder='templates', static_folder='static')
    # static_folder='static', static_url_path='assets')

# all go to the root of this, which is defined in app.py ('/products')
@providers_bp.route('/')
@check_login
def home():
    print('**********g user')
    print(g.user)
    return render_template('providers_home.html')

@providers_bp.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')