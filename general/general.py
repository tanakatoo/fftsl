from flask import Blueprint, render_template
# have to import the model for this here

general_bp = Blueprint('general_bp', __name__, template_folder='templates', static_folder='static')

# all go to the root of this, which is defined in app.py ('/')
@general_bp.route('/')
def home():
    return render_template('home.html')

@general_bp.route('/browsing')
def browsing():
    
    return render_template('browsing.html')