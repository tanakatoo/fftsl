from flask import Blueprint, render_template, g, redirect, url_for, session
from auth.auth import check_login
from models import Provider
from forms import ProviderInfo
# have to import the model for this here

providers_bp = Blueprint('providers_bp', __name__,
    template_folder='templates', static_folder='static')
    # static_folder='static', static_url_path='assets')

# all go to the root of this, which is defined in app.py ('/products')
@providers_bp.route('/')
@check_login
def home():
    """ get info from db """
    p=Provider.get_provider(g.user)
    if p[0]:
        p=p[1]
        
        return render_template("providers_home.html", p=p)
    else:
        session['msg']=f"Sorry we couldn't find your information. Please contact help@fftsl.ca with the following error: {p[1]}"
        return redirect(url_for('general_bp.system_message'))

@providers_bp.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')

@providers_bp.route('/edit_info')
@check_login
def edit_info():
    p=Provider.get_provider(g.user)
    if p[0]:
        p=p[1]
        form=ProviderInfo(obj=p)
        return render_template("providers_edit_info.html",form=form)
    else:
        session['msg']=f"Sorry we couldn't find your information. Please contact help@fftsl.ca with the following error: {p[1]}"
        return redirect(url_for('general_bp.system_message'))