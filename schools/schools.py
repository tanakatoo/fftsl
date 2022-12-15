from flask import Blueprint, render_template, g, redirect, flash, request, url_for
from auth.auth import auth_bp, check_login
from auth.auth import check_login, check_is_school
from models import School, Province, City
from forms import SchoolInfoForm
from util import register_new_city,set_prov_choices,set_city_choices

# have to import the model for this here



schools_bp = Blueprint('schools_bp', __name__,
    template_folder='templates', static_folder='static')
    # static_folder='static', static_url_path='assets')

# all go to the root of this, which is defined in app.py ('/products')
@schools_bp.route('/dashboard')
@check_is_school
@check_login
def home():
    """ get info from db """
    s=School.get_school(g.user.id)

    if s[0]:
        s=s[1]
        city=''
        province=''
        if s.city_id:
            city=City.get_name(id=s.city_id)
        if s.province_id:
            province=Province.get_name(id=s.province_id)
            if city[0] and province[0]:
                # set city and province if possible
                city=city[1]
                province=province[1]

        return render_template("schools_home.html", s=s, city=city,province=province,email=g.user.email)
    else:
        flash(f"Sorry we couldn't find your information. Please contact help@fftsl.ca with the following error: {s[1]}","failure_bkg")
    return redirect('/dashboard')

@schools_bp.route('/learn_more')
def learn_more():
    return render_template('schools_learn_more.html')


@schools_bp.route('/edit_info', methods=['GET'])
@check_is_school
@check_login
def edit_info():
    s=School.get_school(g.user.id)
    all_provinces=set_prov_choices()
    all_cities=set_city_choices()
    
    if s[0] and all_provinces[0] and all_cities[0]:
        s=s[1]
        all_provinces=all_provinces[1]
        all_cities=all_cities[1]
        form=SchoolInfoForm(obj=s)
        
        #populate select field with choices
        form.province_id.choices=all_provinces
        form.city_id.choices=all_cities

        return render_template("schools_edit_info.html",form=form,email=g.user.email)
    else:
        # this is a get request or the validation failed, or some error 
        flash(f'''An error occured getting data:
              p: {s[1]}
              all_provinces: {all_provinces[1]}
              all_cities: {all_cities[1]}''', 'failure_bkg')
        return redirect(url_for('schools_bp.home'))
        
@schools_bp.route('/save_info', methods=['POST'])
@check_is_school
@check_login
def save_info():
        s=School.get_school(g.user.id)
        form=SchoolInfoForm()
        all_provinces=set_prov_choices(form)
        all_cities=set_city_choices(form)
        if all_provinces[0] and all_cities[0] and s[0]:
        # see if it has to register a new city
            s=s[1]
            c=register_new_city(city_id=form.city_id.data,city_name=request.form.get('newCity'))
            if c[0]:
                city_id=c[1]
            else:
                flash (f'An error occured saving the city name: {c[1]}.  The city was not saved. Please contact help@fftsl.ca', 'failure_bkg')
                
            if form.validate_on_submit():
                # write to database
                # create an object to pass
                s_form={
                    'name':form.name.data,
                    'address':form.address.data,
                    'city_id':city_id,
                    'province_id':form.province_id.data,
                    'principal_name':form.principal_name.data,
                    'contact_name':form.contact_name.data,
                    'phone':form.phone.data,
                    'email':request.form['email'],
                    'active':form.active.data,
                    'geocode_lat': form.geocode_lat.data,
                    'geocode_long': form.geocode_long.data
                }
                
                res=School.set_school(fs=s_form, id=g.user.id,s=s)
                
                if res[0]:
                    flash(f'Data saved!', 'success_bkg')
                else:
                    flash (f'An error occured saving data: {res[1]}.  Please contact help@fftsl.ca', 'failure_bkg')

                # have to get all the data again because the data was deleted from saving the data above, so the session doesn't have the newest info
                
                return redirect(url_for('schools_bp.edit_info'))
            else:
                flash(f'An error getting provinces/cities/school information {s[1]}, {all_provinces[1]}, {all_cities[1]}')
                return redirect(url_for('schools_bp.home'))
        else:
            # validation failed
            flash(f'An error occured getting data: {form.errors}', 'failure_bkg')
        return redirect(url_for("schools_bp.edit_info"))
        