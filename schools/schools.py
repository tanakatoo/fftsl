from flask import Blueprint, render_template, g, redirect, flash, request, url_for
from auth.auth import auth_bp, check_login
from auth.auth import check_login, check_is_school
from models import School, Province, City, Recurring_availability_school,Recurring_Day,Date_avail_school, Restriction_School, Restriction
from forms import SchoolInfoForm, DaysForm,RestrictionForm
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


@schools_bp.route('/edit', methods=['GET'])
@check_is_school
@check_login
def edit_info():
    s=School.get_school(g.user.id)
    all_provinces=set_prov_choices()
    all_cities=set_city_choices()
    all_days=Recurring_Day.get_all_days()
    all_restrict=Restriction.get_all_restrict()
    pd=Recurring_availability_school.get_days(id=g.user.id) #all recurring availabilities with start and end dates
    prov_dates=Date_avail_school.get_dates(id=g.user.id) #all specific dates related to this school
    pr=Restriction_School.get_restrictions(id=g.user.id)
    
    
    if s[0] and all_restrict and all_provinces[0] and all_days and all_cities[0] and pd[0] and pr[0] and prov_dates[0]:
        s=s[1]
        all_provinces=all_provinces[1]
        all_cities=all_cities[1]
        all_restrict=all_restrict[1]
        all_days=all_days[1]
        pd=pd[1]
        pr=pr[1]
        prov_dates=prov_dates[1]
        
        form_days=DaysForm()
        days=[(d.id,d.day) for d in all_days]
        form_days.days.choices=days
        
        form_restrict=RestrictionForm()
        restrictions=[(r.id,r.name) for r in all_restrict]
        form_restrict.restrictions.choices=restrictions
        form_restrict.restrictions.data=[r.restriction_id for r in pr]
        
        form=SchoolInfoForm(obj=s)
        
        #populate select field with choices
        form.province_id.choices=all_provinces
        form.city_id.choices=all_cities
        
        return render_template("schools_edit_info.html",form=form,email=g.user.email,form_restrict=form_restrict,form_days=form_days,pd=pd, prov_dates=prov_dates)
    else:
        # this is a get request or the validation failed, or some error 
        flash(f'''An error occured getting data:
              s: {s[1]}
              all_provinces: {all_provinces[1]}
              all_cities: {all_cities[1]}
              all_days: {all_days[1]}
              pd: {pd[1]}
              prov_dates: {prov_dates[1]}''', 'failure_bkg')
        return redirect(url_for('schools_bp.home'))
        
@schools_bp.route('/save_info', methods=['POST'])
@check_is_school
@check_login
def save_info():
        s=School.get_school(g.user.id)
        
        all_provinces=set_prov_choices()
        all_cities=set_city_choices()
        all_days=Recurring_Day.get_all_days()
        all_restrict=Restriction.get_all_restrict()
        
        if all_provinces[0] and all_cities[0] and s[0] and all_days[0] and all_restrict[0]:
        # see if it has to register a new city
            s=s[1]
            all_days=all_days[1]
            all_restrict=all_restrict[1]
            
            form_restrict=RestrictionForm()
            restrictions=[(r.id,r.name) for r in all_restrict]
            form_restrict.restrictions.choices=restrictions
        
            form=SchoolInfoForm()
            form.province_id.choices=all_provinces
            form.city_id.choices=all_cities
            
            form_days=DaysForm()
            days=[(d.id,d.day) for d in all_days]
            form_days.days.choices=days
            
            c=register_new_city(city_id=form.city_id.data,city_name=request.form.get('newCity'))
            if c[0]:
                city_id=c[1]
            else:
                flash (f'An error occured saving the city name: {c[1]}.  The city was not saved. Please contact help@fftsl.ca', 'failure_bkg')
                
            if form.validate_on_submit() and form_days.validate_on_submit():
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
                list_of_recurring_days=form.recurring_dates.data.split(',')
            
                recurring_days_to_db=[]
                # now we have 4:2022-12-16:2022-12-17
                for d in list_of_recurring_days:
                    if not d == "":
                        list_of_data=d.split(':')
                        data={'school_id':g.user.id,
                            'recurring_day_id': list_of_data[0],
                            'start_date': list_of_data[1],
                            'end_date':list_of_data[2]}
                        recurring_days_to_db.append(data)
                
                # save recurring availabilties
                resd=Recurring_availability_school.set_days(id=g.user.id,fd=recurring_days_to_db)
                
                # save specific dates
                resdates=Date_avail_school.set_dates(id=g.user.id,add_dates=form.dates.data)
            
                #save restrictions
                resrestrict=Restriction_School.set_restrictions(id=g.user.id,fr=form_restrict.restrictions.data)
                
                if res[0] or resdates[0] or resrestrict[0]:
                    flash(f'Data saved!', 'success_bkg')
                else:
                    flash (f'''An error occured saving data: school info:{res[1]}, 
                           recurring: {resd[1]}, 
                           dates:{resdates[1]},
                           restrictions: {resrestrict[1]}
                           .  Please contact help@fftsl.ca''', 'failure_bkg')

                # have to get all the data again because the data was deleted from saving the data above, so the session doesn't have the newest info
                
                return redirect(url_for('schools_bp.edit_info'))
            else:
                flash(f'''An error getting provinces/cities/school information {s[1]}, 
                      {all_provinces[1]},
                      {all_cities[1]}, 
                      {all_days[1]}
                      {all_restrict[1]}''')
                return redirect(url_for('schools_bp.home'))
        else:
            # validation failed
            flash(f'''An error occured getting data: 
                  form: {form.errors}, 
                  form_days: {form_days.errors},
                  form_restrict: {form_restrict.errors}''', 'failure_bkg')
        return redirect(url_for("schools_bp.edit_info"))
        
        
@schools_bp.route('/delete', methods=['POST'])
@check_is_school
@check_login
def delete_school():
    # get provider info
    s=School.get_school(g.user.id)
    if s[0]:
        s=s[1]
        res=s.delete()
        if res[0]:
            flash(f'Profile deleted!', 'success_bkg')
            return redirect(url_for('general_bp.home'))
        else:
            flash(f'Error deleting profile: {res[1]}', 'failure_bkg')
            return redirect(url_for('schools_bp.edit_info'))
    else:
        flash(f'Error getting school data', 'failure_bkg')
        return redirect(url_for('schools_bp.edit_info'))
    