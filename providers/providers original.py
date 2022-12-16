from flask import Blueprint, render_template, g, redirect, url_for, session, flash, request
from auth.auth import check_login, check_is_provider
from models import Provider, Province, City, Dish, Cuisine, Cuisine_Provider, Recurring_availability, Recurring_Day#, Date_avail
from forms import ProviderInfoForm, DishInfoForm, SettingsForm, CuisineForm, DaysForm
from util import register_new_city, set_city_choices,set_prov_choices
# have to import the model for this here

providers_bp = Blueprint('providers_bp', __name__,
    template_folder='templates', static_folder='static')
    # static_folder='static', static_url_path='assets')

# all go to the root of this, which is defined in app.py ('/products')
@providers_bp.route('/dashboard')
@check_is_provider
@check_login
def home():
    """ get info from db """
    p=Provider.get_provider(g.user.id)
    m=Dish.get_menu(g.user.id)

    if p[0] and m[0]: #no errors getting data but there is no provider yet
        p=p[1]
        m=m[1]
        if p: #if there was already a provider record in the db, get the city and province names
            city=City.get_name(id=p.city_id)
            province=Province.get_name(id=p.province_id)
            if city[0] and province[0]:
                # set city and province if possible
                city=city[1]
                province=province[1]
            menuDisable=''
     
        else:
            # disable menu button because there is no record of provider
            menuDisable='true'
            city=''
            province=''

        return render_template("providers_home.html", p=p, city=city,province=province,email=g.user.email, m=m, menuDisable=menuDisable)
    else:
        session['msg']=f"Sorry we couldn't find your information. Please contact help@fftsl.ca with the following error: {p[1]}"
        return redirect(url_for('general_bp.system_message'))

@providers_bp.route('/learn_more')
def learn_more():
    return render_template('providers_learn_more.html')


@providers_bp.route('/edit_info', methods=['GET'])
@check_login
@check_is_provider
def edit_info():
    p=Provider.get_provider(g.user.id) #get provider info 
    pc=Cuisine_Provider.get_cuisines(g.user.id) #get cuisine info related to provider
    all_provinces=set_prov_choices() #get list of all provinces
    all_cities=set_city_choices() #get list of all cities
    c=Cuisine.get_all_cuisines() #get list of all cuisines
    
    if p[0] and c[0] and pc[0] and all_provinces[0] and all_cities[0]:
        p=p[1]
        c=c[1]
        pc=pc[1]
        all_provinces=all_provinces[1]
        all_cities=all_cities[1]
        
        form=ProviderInfoForm(obj=p)
        form_c=CuisineForm()
        
        #populate the select fields with choices
        form.province_id.choices=all_provinces
        form.city_id.choices=all_cities   
        cuisines=[(cuisine.id,cuisine.name) for cuisine in c]
        form_c.cuisines.choices=cuisines
    
        return render_template("providers_edit_info.html",form=form,form_c=form_c,email=g.user.email,pc=pc)
    else: 
        flash(f'''An error occured getting data:
              pc: {pc[1]}
              c: {c[1]}
              p: {p[1]}
              all_provinces: {all_provinces[1]}
              all_cities: {all_cities[1]}''', 'failure_bkg')
        return redirect(url_for('providers_bp.home'))

@providers_bp.route('/save_info', methods=['POST'])
@check_is_provider
@check_login
def save_info():
        p=Provider.get_provider(g.user.id)
        
        all_provinces=set_prov_choices()
        all_cities=set_city_choices()
        c=Cuisine.get_all_cuisines()
        
        if all_provinces[0] and all_cities[0] and p[0] and c[0]:
        # see if it has to register a new city
            p=p[1]
            c=c[1]
            all_provinces=all_provinces[1]
            all_cities=all_cities[1]
            
            form=ProviderInfoForm()
            form_c=CuisineForm()
            
            #populate the select fields with choices
            form.province_id.choices=all_provinces
            form.city_id.choices=all_cities   
            cuisines=[(cuisine.id,cuisine.name) for cuisine in c]
            form_c.cuisines.choices=cuisines
            
            city=register_new_city(city_id=form.city_id.data,city_name=request.form.get('newCity'))
            if city[0]:
                city_id=city[1]
            else:
                #only flash message, we can continue saving the rest of the data
                flash (f'An error occured saving the city name: {city[1]}.  The city was not saved. Please contact help@fftsl.ca', 'failure_bkg')
                
            if form.validate_on_submit() and form_c.validate_on_submit():
                # write to database
                # create an object to pass
                p_form={
                'name':form.name.data,
                'address':form.address.data,
                'city_id':city_id,
                'province_id':form.province_id.data,
                'contact_name':form.contact_name.data,
                'phone':form.phone.data,
                'email':request.form['email'],
                'sales_pitch':form.sales_pitch.data,
                'active':form.active.data,
                'geocode_lat': form.geocode_lat.data,
                'geocode_long': form.geocode_long.data
            }
                
                res=Provider.set_provider(fp=p_form, id=g.user.id,p=p)
                # need to save cuisines
                resc=Cuisine_Provider.set_cuisines(fc=form_c.cuisines.data,id=g.user.id)
                
                if res[0] and resc[0]:
                    flash(f'Data saved!', 'success_bkg')
                else:
                    flash (f'An error occured saving data: {res[1]}, {resc[1]}.  Please contact help@fftsl.ca', 'failure_bkg')

                # have to get all the data again because the data was deleted from saving the data above, so the session doesn't have the newest info
                
                return redirect(url_for('providers_bp.edit_info'))
            else:
                flash(f'An error getting provinces/cities/provider information {p[1]}, {all_provinces[1]}, {all_cities[1]}')
                return redirect(url_for('providers_bp.home'))
        else:
            # validation failed
            flash(f'An error occured getting data: form:{form.errors}, form_cuisine:{form_c.errors}', 'failure_bkg')
        return redirect(url_for("providers_bp.edit_info"))
        
        
@providers_bp.route('/edit_menu', methods=['GET'])
@check_is_provider
@check_login
def edit_menu():
    m=Dish.get_menu(g.user.id)
    p=Provider.get_provider(g.user.id) #settings is in provider table
    all_days=Recurring_Day.get_all_days()
    pd=Recurring_availability.get_days(g.user.id) #all recurring availabilities with start and end dates
    #prov_dates=Date_avail.get_dates(id=g.user.id) #all specific dates related to this provider
    
    if m[0] and p[0] and all_days[0] and pd[0]: #and prov_dates[0]: # means there are no errors getting the info
        m=m[1] #could be a list
        p=p[1]
        all_days=all_days[1]
        pd=pd[1]
        #prov_dates=prov_dates[1]
        form_m=DishInfoForm(active=True) 
        form_p=SettingsForm(obj=p)
        form_days=DaysForm()
        
        days=[(d.id,d.day) for d in all_days]
        form_days.days.choices=days

        if m:
            # user can select which dish they want to link to (because we are adding a new dish)
            form_m.related_to_dish.choices=[("", "---")]+[(d.id, d.name) for d in m]
        else:
            form_m.related_to_dish.choices=[("", "---")]
        
        #return render_template("providers_edit_menu.html",form_m=form_m,form_p=form_p,form_days=form_days,m=m, pd=pd, prov_dates=prov_dates)
        return render_template("providers_edit_menu.html",form_m=form_m,form_p=form_p,form_days=form_days,m=m, pd=pd)
            
    else:
        flash(f"Error getting data. {m[1]}, {p[1]}, {all_days[1]}, {pd[1]}", 'failure_bkg')
        #flash(f"Error getting data. {m[1]}, {p[1]}, {all_days[1]}, {pd[1]}, {prov_dates[1]}", 'failure_bkg')
        return redirect('/dashboard') 
    
    
@providers_bp.route('/save_settings', methods=["POST"])
@check_is_provider
@check_login
def save_settings():
    p=Provider.get_provider(g.user.id)
    m=Dish.get_menu(g.user.id)
    all_days=Recurring_Day.get_all_days()
    
    
    if m[0] and p[0] and all_days[0]:
        m=m[1]
        p=p[1]
        all_days=all_days[1]
        form_p=SettingsForm(obj=p)
        form_days=DaysForm()
        days=[(d.id,d.day) for d in all_days]
        form_days.days.choices=days
        
        if form_p.validate_on_submit() and form_days.validate_on_submit():
            # write to database
            # create an object to pass

            p_form={
                'max_meals_per_day':form_p.max_meals_per_day.data,
                'min_meals':form_p.min_meals.data,
                'serve_num_org_per_day':form_p.serve_num_org_per_day.data
            }
            # save provider info
            res=p.set_settings(fp=p_form)
            # save recurring availability
            resd=Recurring_availability.set_days(id=g.user.id,fd=form_days.days.data,user_type=g.user.user_type)
            # save specific dates
            #resdates=Date_avail.set_dates(id=g.user.id,dates=form_p.dates.data)

            if res[0] and resd[0]: #and resdates[0]:
                flash(f'Data saved!', 'success_bkg')
            
            else:
                #flash (f'An error occured saving settings data: {res[1]}, {resd[1]}, {resdates[1]}.  Please contact help@fftsl.ca', 'failure_bkg')
                flash (f'An error occured saving settings data: {res[1]}, {resd[1]}.  Please contact help@fftsl.ca', 'failure_bkg')
            return redirect(url_for("providers_bp.edit_menu"))
    else:
        flash(f"Error getting data. {m[1]}, {p[1]}", 'failure_bkg')
        return redirect("/edit_menu")

@providers_bp.route('/save_dish', methods=["POST"])
@check_is_provider
@check_login
def save_dish():
    # need provider_id, name of dish to save a dish
    p=Provider.get_provider(g.user.id)
    m=Dish.get_menu(g.user.id)
    if p[0] and m[0]: #got provider
        p=p[1] 
        m=m[1]
        form_d=DishInfoForm() 
        if m:
            # user can select which dish they want to link to (because we are adding a new dish)
            form_d.related_to_dish.choices=[("", "---")]+[(d.id, d.name) for d in m]
        else:
            form_d.related_to_dish.choices=[("", "---")]
        d_form={
                'provider_id':g.user.id,
                'name':form_d.name.data,
                'recipe':form_d.recipe.data,
                'num_servings':form_d.num_servings.data,
                'ingred_disp':form_d.ingred_disp.data,
                'price':form_d.price.data,
                'sales_pitch':form_d.sales_pitch.data,
                'max_meals':form_d.max_meals.data,
                'related_to_dish':form_d.related_to_dish.data,
                'pass_guidelines':form_d.pass_guidelines.data,
                'active':form_d.active.data
            }

        if form_d.validate_on_submit():
            # write to database
            # create an object to pass
            d_form={
                'provider_id':g.user.id,
                'name':form_d.name.data,
                'recipe':form_d.recipe.data,
                'num_servings':form_d.num_servings.data,
                'ingred_disp':form_d.ingred_disp.data,
                'price':form_d.price.data,
                'sales_pitch':form_d.sales_pitch.data,
                'max_meals':form_d.max_meals.data,
                'related_to_dish':form_d.related_to_dish.data,
                'pass_guidelines':form_d.pass_guidelines.data,
                'active':form_d.active.data
            }
           
            res=Dish.set_dish(fd=d_form)

            if res[0]:
                flash(f'Data saved!', 'success_bkg')

            else:
                flash (f'An error occured saving settings data: {res[1]}.  Please contact help@fftsl.ca', 'failure_bkg')


        return redirect(url_for("providers_bp.edit_menu"))       
        
    else:
        flash(f"Error getting data. {p[1]}", 'failure_bkg')
        return redirect(url_for("providers_bp.edit_menu"))