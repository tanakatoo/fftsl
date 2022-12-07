from flask import Blueprint, render_template, g, redirect, url_for, session, flash, request
from auth.auth import check_login
from models import Provider, Province, City, Dish
from forms import ProviderInfo, MenuInfo,Settings
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

    if p[0]: #no errors getting data but there is no provider yet
        p=p[1]
        if p: #if there was already a provider record in the db, get the city and province names
            city=City.get_name(id=p.city_id)
            province=Province.get_name(id=p.province_id)
        else:
            city=''
            province=''

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
 
    print('**************form is******')
    print(form.province_id.data)
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
            'active':form.active.data,
            'geocode_lat': form.geocode_lat.data,
            'geocode_long': form.geocode_long.data
        }

        res=Provider.set_provider(fp=p_form, u=g.user,p=p)

        if res[0]:
            flash(f'Data saved!')
            return redirect('/providers')
        else:
            flash (f'An error occured saving data: {res[1]}.  Please contact help@fftsl.ca')
            return render_template("providers_edit_info.html",form=form, email=g.user.email)
    else:
        # this is a get request
        flash('this is a get request')
        flash(form.errors)
        return render_template("providers_edit_info.html",form=form, email=g.user.email)
        
@providers_bp.route('/edit_menu', methods=['GET','POST'])
@check_login
def edit_menu():
    m=Dish.get_menu(g.user)
    p=Provider.get_provider(g.user) #settings is in provider table
    if m[0] and p[0]: # means there are no errors getting the info
        m=m[1]
        p=p[1]
        form_m=MenuInfo() 
        form_p=Settings(obj=p)

    if form_m.validate_on_submit() and form_p.validate_on_submit():
        # write to database
        # create an object to pass

        p_form={
            'max_meals_per_day':form_p.max_meals_per_day.data,
            'min_meals':form_p.min_meals.data,
            'serve_num_org_per_day':form_p.serve_num_org_per_day.data
        }

        res=Provider.set_provider(fp=p_form, u=g.user,p=p)

        if res[0]:
            flash(f'Data saved!')
            return redirect('/providers')
        else:
            flash (f'An error occured saving data: {res[1]}.  Please contact help@fftsl.ca')
            return render_template("providers_edit_info.html",form_m=form_m, form_p=form_p)
    else:
        # this is a get request
        return render_template("providers_edit_info.html",form_m=form_m,form_p=form_p)