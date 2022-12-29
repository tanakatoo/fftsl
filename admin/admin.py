from flask import Blueprint, render_template, request, flash, redirect, url_for, session,g
from functools import wraps
from models import User, Provider
from forms import PasswordResetForm, PasswordSetForm, LoginForm, UserRegisterForm
from config import CURR_USER_KEY, UPLOAD_FOLDER, BASEDIR
from auth.auth import check_is_admin, check_login
import os

# have to import the model for this here

admin_bp = Blueprint('admin_bp', __name__,
    template_folder='templates', static_folder='static',static_url_path='/admin/static')
    # static_folder='static', static_url_path='assets')


# all go to the root of this, which is defined in app.py ('/products')
@admin_bp.route('/', methods=['POST', 'GET'])
@check_is_admin
@check_login
def home():
    # get all providers and find all of the ones with submit_inspection = true and reviewed=false
    ps=Provider.get_to_review()
    print('************providers to review, why is id not available')
    print(ps)
    for p in ps:
        p.inspection_report=os.path.join('/',UPLOAD_FOLDER, 'inspection',p.inspection_report)
    return render_template('admin_home.html', ps=ps)   