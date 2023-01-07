from flask import Blueprint, render_template, request, url_for, redirect
from models import Provider, Dish, Parent
# have to import the model for this here

parents_bp = Blueprint('parents_bp', __name__,
    template_folder='templates', static_folder='static')

@parents_bp.route('/')
def home():
    # criteria=request.form.get('search')
    # if criteria:
    #     return redirect(url_for("general_bp.search", criteria=criteria))
    return render_template('parents_home.html')

