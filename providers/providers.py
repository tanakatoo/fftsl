from flask import Blueprint, render_template, g, redirect, url_for, session, flash, request
from auth.auth import check_login
from models import Provider, Province, City, Dish
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
    m=Dish.get_menu(g.user.id)
    
    if p[0]:
        p=p[1]
        city=City.get_name(id=p.city_id)
        province=Province.get_name(id=p.province_id)

        return render_template("providers_home.html", p=p, city=city,province=province,email=g.user.email, m=m)
    else:
        session['msg']=f"Sorry we couldn't find your information. Please contact help@fftsl.ca with the following error: {p[1]}"
        return redirect(url_for('general_bp.system_message'))

@providers_bp.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')


@providers_bp.route('/edit_info', methods=['GET','POST'])
@check_login
def edit_info():
    p=Provider.get_provider(g.user)
    if p[0]:
        p=p[1]
        form=ProviderInfo(obj=p)
        provinces=[(pro.id,pro.name) for pro in Province.query.all()]
        cities=[(c.id,c.name) for c in City.query.all()]
        form.province_id.choices=provinces
        form.city_id.choices=cities

    if request.method=="GET":
        return render_template("providers_edit_info.html",form=form, email=g.user.email)
    else:
        if form.validate_on_submit():
            # write to database
            # create an object to pass
            p_form={
                'name':form.name.data,
                'address':form.address.data,
                'city_id':form.city_id.data,
                'province_id':form.province_id.data,
                'contact_name':form.contact_name.data,
                'phone':form.phone.data,
                'email':request.form['email'],
                'sales_pitch':form.sales_pitch.data,
                'active':form.active.data
            }

            res=Provider.set_provider(fp=p_form, u=g.user,p=p)

            flash(f'Data saved!')
            return redirect('/providers')
        else:
            # this is a get request
            
            return render_template("providers_edit_info.html",form=form, email=g.user.email)
        
        
    # else:
    #     session['msg']=f"Sorry we couldn't find your information. Please contact help@fftsl.ca with the following error: {p[1]}"
    #     return redirect(url_for('general_bp.system_message'))