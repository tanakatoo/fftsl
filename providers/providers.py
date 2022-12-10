from flask import Blueprint, render_template, g, redirect, url_for, session, flash, request
from auth.auth import check_login
from models import Provider, Province, City, Dish, Cuisine, Cuisine_Provider, Recurring_availability, Recurring_Days, Date_provider_avail
from forms import ProviderInfoForm, DishInfoForm, SettingsForm, CuisineForm, DaysForm
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
    m=Dish.get_menu(g.user)

    if p[0] and m[0]: #no errors getting data but there is no provider yet
        p=p[1]
        m=m[1]
        if p: #if there was already a provider record in the db, get the city and province names
            city=City.get_name(id=p.city_id)
            province=Province.get_name(id=p.province_id)
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
    return render_template('learn_more.html')


@providers_bp.route('/edit_info', methods=['GET','POST'])
@check_login
def edit_info():
    p=Provider.get_provider(g.user)
    c=Cuisine.get_all_cuisines()
    pc=Cuisine_Provider.get_cuisines(g.user)

    if p[0] and c[0] and pc[0]:
        p=p[1]
        c=c[1]
        pc=pc[1]

        form=ProviderInfoForm(obj=p)
        form_c=CuisineForm()

        cuisines=[(cuisine.id,cuisine.name) for cuisine in c]
        form_c.cuisines.choices=cuisines
        
        provinces=[(pro.id,pro.name) for pro in Province.get_provinces()]
        cities=[(c.id,c.name) for c in City.get_cities()]
        form.province_id.choices=provinces
        form.city_id.choices=cities
        
    if form.validate_on_submit() and form_c.validate_on_submit():
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
        # need to save cuisines
        resc=Cuisine_Provider.set_cuisines(fc=form_c.cuisines.data,u=g.user)
        
        if res[0] and resc[0]:
            flash(f'Data saved!', 'success_bkg')
        else:
            flash (f'An error occured saving data: {res[1]}, {resc[1]}.  Please contact help@fftsl.ca', 'failure_bkg')

        # have to get this again because the data was deleted from saving the data above, so the session doesn't have the newest info
        pc=Cuisine_Provider.get_cuisines(g.user)[1] 

        return render_template("providers_edit_info.html",form=form, form_c=form_c, email=g.user.email, pc=pc)
    else:
        # this is a get request or the validation failed
        flash(f'An error occured getting data: {form.errors}, {form_c.errors}', 'failure_bkg')
        return render_template("providers_edit_info.html",form=form, form_c=form_c,email=g.user.email, pc=pc)
        
@providers_bp.route('/edit_menu', methods=['GET'])
@check_login
def edit_menu():
    m=Dish.get_menu(g.user)
    p=Provider.get_provider(g.user) #settings is in provider table
    all_days=Recurring_Days.get_all_days()
    pd=Recurring_availability.get_days(g.user)
    prov_dates=Date_provider_avail.get_dates(u=g.user)

    if m[0] and p[0] and all_days[0] and pd[0] and prov_dates[0]: # means there are no errors getting the info
        m=m[1] #could be a list
        p=p[1]
        all_days=all_days[1]
        pd=pd[1]
        prov_dates=prov_dates[1]
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
            
    else:
        flash(f"Error getting data. {m[1]}, {p[1]}, {all_days[1]}, {pd[1]}", 'failure_bkg')
    
    return render_template("providers_edit_menu.html",form_m=form_m,form_p=form_p,form_days=form_days,m=m, pd=pd, prov_dates=prov_dates)
    
@providers_bp.route('/save_settings', methods=["POST"])
@check_login
def save_settings():
    p=Provider.get_provider(g.user)
    m=Dish.get_menu(g.user)
    all_days=Recurring_Days.get_all_days()
    
    
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
            resd=Recurring_availability.set_days(u=g.user,fd=form_days.days.data)
            # save specific dates
            resdates=Date_provider_avail.set_dates(u=g.user,dates=form_p.dates.data)

            if res[0] and resd[0] and resdates[0]:
                flash(f'Data saved!', 'success_bkg')
            
            else:
                flash (f'An error occured saving settings data: {res[1]}, {resd[1]}, {resdates[1]}.  Please contact help@fftsl.ca', 'failure_bkg')
                
            return redirect(url_for("providers_bp.edit_menu"))
    else:
        flash(f"Error getting data. {m[1]}, {p[1]}", 'failure_bkg')
        return redirect("/edit_menu")

@providers_bp.route('/save_dish', methods=["POST"])
@check_login
def save_dish():
    # need provider_id, name of dish to save a dish
    p=Provider.get_provider(g.user)
    m=Dish.get_menu(g.user)
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