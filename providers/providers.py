from flask import Blueprint, render_template, g, redirect, url_for, session, request
from auth.auth import check_login, check_is_provider
from models import Provider, Province, City, Dish, Cuisine, Cuisine_Provider, Recurring_availability, Recurring_Day, Date_avail, Restriction,Restriction_Dish, Category
from forms import ProviderInfoForm, DishInfoForm, CuisineForm, DaysForm, RestrictionForm, CategoryForm
from util import register_new_city, set_city_choices,set_prov_choices, save_image, path_to_file, remove_image
from datetime import date
from general.general import flash_error, flash_success
from decimal import Decimal

providers_bp = Blueprint('providers_bp', __name__,
    template_folder='templates', static_folder='static')

# CORS(providers_bp)

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
        if not p[0]:
            flash_error(f'Trouble locating profile: {p[1]}')
        if not m[0]:
            flash_error(f'Trouble getting menu: {m[1]}')
        return redirect(url_for('general_bp.home'))

@providers_bp.route('/learn_more')
def learn_more():
    return render_template('providers_learn_more.html')

def get_info():
    p=Provider.get_provider(g.user.id) #get provider info 
    pc=Cuisine_Provider.get_cuisines(g.user.id) #get cuisine info related to provider
    all_provinces=set_prov_choices() #get list of all provinces
    all_cities=set_city_choices() #get list of all cities
    c=Cuisine.get_all_cuisines() #get list of all cuisines
    all_days=Recurring_Day.get_all_days()
    pd=Recurring_availability.get_days(id=g.user.id)
    prov_dates=Date_avail.get_dates(id=g.user.id)
    
    if prov_dates[0] and p[0] and pd[0] and c[0] and pc[0] and all_provinces[0] and all_cities[0] and all_days[0]:
        p=p[1]
        c=c[1]
        pc=pc[1]
        pd=pd[1]
        prov_dates=prov_dates[1]
        all_provinces=all_provinces[1]
        all_cities=all_cities[1]
        all_days=all_days[1]
        
        form=ProviderInfoForm(obj=p)
        form.province_id.choices=all_provinces
        form.city_id.choices=all_cities
        
        form_c=CuisineForm()
        cuisines=[(cuisine.id,cuisine.name) for cuisine in c]
        form_c.cuisines.choices=cuisines
        checked_cuisines=[c.cuisine_id for c in pc]
        
                
        form_days=DaysForm()
        days=[(d.id,d.day) for d in all_days]
        form_days.days.choices=days
                
        return (True,p,c,checked_cuisines,pc,pd,all_provinces, all_cities, all_days,form,form_days,form_c,prov_dates)
    else:   
        if not pc[0]:
            flash_error(f'Trouble getting selected cuisine(s): {pc[1]}')
        if not c[0]:
            flash_error(f'Trouble getting cuisine names: {c[1]}')
        if not p[0]:
            flash_error(f'Trouble getting profile: {p[1]}')
        if not pd[0]:
            flash_error(f'Trouble getting recurring availability: {pd[1]}')
        if not all_provinces[0]:
            flash_error(f'Trouble getting province names: {all_provinces[1]}')
        if not all_cities[0]:
            flash_error(f'Trouble getting city names: {all_cities[1]}')
        if not prov_dates[0]:
            flash_error(f'Trouble getting specific availability dates: {prov_dates[1]}')
        if not all_days[0]:
            flash_error(f'Trouble getting days of the week: {all_days[1]}')
        
        return (False,p,c,checked_cuisines,pc,pd,all_provinces, all_cities, all_days,form,form_days,form_c,prov_dates)
        
        
    
@providers_bp.route('/details', methods=['GET'])
@check_login
@check_is_provider
def info_details():
    data=get_info()
         
    if data[0]:
        resp,p,c,checked_cuisines,pc,pd,all_provinces, all_cities, all_days,form,form_days,form_c,prov_dates=data
        form_c.cuisines.data=checked_cuisines
        province=Province.get_name(p.province_id)
        city=City.get_name(p.city_id)
        
        form.display.data=p.display
        # display the thumbnail of the report
        if p.inspection_report and not p.inspection_report is None:
            p.inspection_report=path_to_file(saved_file=p.inspection_report, folder='inspection')
        
        if province[0] and city[0]:
            province=province[1]
            city=city[1]
        else:
            if not province[0]:
                flash_error(f'Trouble getting province: {province[1]}')
            if not city[0]:
                flash_error(f'Trouble getting city: {city[1]}')
            return redirect(url_for('providers_bp.home'))
    
        return render_template("providers_details.html",p=p, prov=province,city=city,form_c=form_c,pd=pd,email=g.user.email, pc=pc,prov_dates=prov_dates)
    else:
        # error getting info
        # errors flashed in get_info function
       return redirect(url_for('providers_bp.home'))



@providers_bp.route('/edit', methods=['GET'])
@check_login
@check_is_provider
def edit_info():
    data=get_info()
    
    if data[0]:
        resp,p,c,checked_cuisines,pc,pd,all_provinces, all_cities, all_days,form,form_days,form_c,prov_dates=data
    
        form_c.cuisines.data=checked_cuisines
        # display the thumbnail of the report 
        
        if form.inspection_report.data:
            form.inspection_report.data=path_to_file(saved_file=p.inspection_report, folder='inspection')
        
        return render_template("providers_edit_info.html",pd=pd,form=form,form_days=form_days,form_c=form_c,email=g.user.email, prov_dates=prov_dates)
    else:
        return redirect(url_for('providers_bp.home'))

@providers_bp.route('/save_info', methods=['POST'])
@check_is_provider
@check_login
def save_info():
    data=get_info()
    
    if not data[0]:        
        # cannot get basic data, so we abort
        return redirect(url_for('providers_bp.edit_info'))
    
    resp,p,c,checked_cuisines,pc,pd,all_provinces, all_cities, all_days,form,form_days,form_c,prov_dates=data
    
     # if request.form has removeImage, it means the user only clicked to delete image but we need to also save the data
    if(request.form.get('removeImage')):
        if p.inspection_report and not p.inspection_report is None:
            res_image=remove_image(file_name_old=p.inspection_report,folder='inspection')
            if res_image[0]:
                res_image_data=p.update_one(property='inspection_report',data=None)
                if not res_image_data[0]:
                    flash_error(f'Removed image but had trouble removing image name from profile: {res_image_data[1]}')
            else:
                flash_error(f'Trouble deleting image: {res_image[1]}')
    
    city=register_new_city(city_id=form.city_id.data,city_name=request.form.get('newCity'))
    if city[0]:
        city_id=city[1]
    else:
        #only flash message, we can continue saving the rest of the data
        flash_error (f'Trouble saving city name: {city[1]}')
        
    if form.validate_on_submit() and form_c.validate_on_submit() and form_days.validate_on_submit():
        
         # change geocode to null if it is empty string
        if form.geocode_lat.data=='' or form.geocode_lat.data is None:
            geocode_lat=None
        else:
            geocode_lat=Decimal(form.geocode_lat.data)
        if form.geocode_long.data=='' or form.geocode_long.data is None:
            geocode_long=None
        else:
            geocode_long=Decimal(form.geocode_long.data)

        if(form.submit_inspection.data == "True"):  

            submit_inspection = True
            submit_inspection_date= date.today().strftime("%Y-%m-%d")
        else:
            submit_inspection=False
            submit_inspection_date=None
        
        # write to database
        # create an object to pass
        p_form={
        'name':form.name.data,
        'website':form.website.data,
        'address':form.address.data,
        'city_id':city_id,
        'province_id':form.province_id.data,
        'contact_name':form.contact_name.data,
        'phone':form.phone.data,
        'email':request.form['email'],
        'sales_pitch':form.sales_pitch.data,
        'active':form.active.data,
        'display': form.display.data,
        'geocode_lat': geocode_lat,
        'geocode_long': geocode_long,
        'max_meals_per_day':form.max_meals_per_day.data,
        'min_meals':form.min_meals.data,
        'serve_num_org_per_day':form.serve_num_org_per_day.data,
        'submit_inspection': submit_inspection,
        'submit_inspection_date': submit_inspection_date,
        
        }
        
         # save pic of inspection report if uploaded
        file=save_image(form_file='inspectionFile', remove=True, folder='inspection', file_name=f'{str(g.user.id)}',file_name_old=p.inspection_report)
        
        if file[0] and not file[1] == 'not submitted':
            p.inspection_report=file[1]
        elif not file[0]:
            flash_error(f'Trouble saving file: {file[1]}')
                 

        # save provider info
        res=Provider.set_provider(fp=p_form, id=g.user.id,p=p)
        # save cuisines
        resc=Cuisine_Provider.set_cuisines(fc=form_c.cuisines.data,id=g.user.id)
        
        """save recurring availability
        parse it before passing it in
        this what it looks like coming in 4:2022-12-16:2022-12-17,6:2022-12-16:2022-12-17
        records separated by ',' and data by ':'
        need to make it a list like: [{provider_id:XX, recurring_day_id:XX, start_date:XX,end_date:xx}]
        """
        list_of_recurring_days=form.recurring_dates.data.split(',')
        
        recurring_days_to_db=[]
        # now we have 4:2022-12-16:2022-12-17
        for d in list_of_recurring_days:
            if not d == "":
                list_of_data=d.split(':')
                data={'provider_id':g.user.id,
                    'recurring_day_id': list_of_data[0],
                    'start_date': list_of_data[1],
                    'end_date':list_of_data[2]}
                recurring_days_to_db.append(data)
        
        resd=Recurring_availability.set_days(id=g.user.id,fd=recurring_days_to_db)
        
        # save specific dates
        resdates=Date_avail.set_dates(id=g.user.id,add_dates=form.dates.data)  
        
        if res[0] and resc[0] and resd[0] and resdates[0] and file[0]:
            flash_success(f'Data saved')
        else:
            if not res[0]:
                flash_error(f'Trouble saving profile: {res[1]}')
            if not resc[0]:
                flash_error(f'Trouble saving cuisine: {resc[1]}')
            if not resd[0]:
                flash_error(f'Trouble saving recurring availability: {resd[1]}')
            if not resdates[0]:
                flash_error(f'Trouble saving specific availability dates: {resdates[1]}')
            if not file[0]:
                flash_error(f'Trouble saving file: {file[1]}')

        return redirect(url_for('providers_bp.edit_info'))
    else:
        if not form.errors:
            flash_error(f'Trouble saving profile data: {form.errors}')
        if not form_c.errors:
            flash_error(f'Trouble saving cuisine: {form_c.errors}')
        if not form_days.errors:
            flash_error(f'Trouble getting days of the week: {form_days.errors}')
        
        return redirect(url_for('providers_bp.home'))
    
def get_empty_dish_info():
    m=Dish.get_menu(g.user.id)
    all_restrict=Restriction.get_all_restrict()
    all_categories=Category.get_all_cat()
    
    if m[0] and all_restrict[0] and all_categories[0]:
        m=m[1]
        all_restrict=all_restrict[1]
        all_categories=all_categories[1]
        
        form_d=DishInfoForm() 
        form_cat=CategoryForm()
        categories=[(c.id,c.name) for c in all_categories]
        form_cat.categories.choices=categories
        form_cat.categories.data=1 #set entree as the default type of meal
        
        if m:
            # user can select which dish they want to link to (because we are adding a new dish)
            form_d.related_to_dish.choices=[("", "---")]+[(d.id, d.name) for d in m]
        else:
            form_d.related_to_dish.choices=[("", "---")]
            
        form_restrict=RestrictionForm()
        restrictions=[(r.id,r.name) for r in all_restrict]
        form_restrict.restrictions.choices=restrictions

        return (True,m,all_restrict,all_categories,form_d,form_cat,form_restrict)
    
    else:
        if not m[0]:
            flash_error(f"Error getting menu: {m[1]}")
        if not all_restrict[0]:
            flash_error(f"Error getting restrictions: {all_restrict[1]}")
        if not all_categories[0]:
            flash_error(f"Error getting dish categories: {all_categories[1]}")
        return (False,m,all_restrict,all_categories,form_d,form_cat,form_restrict)
        

@providers_bp.route('/dishes/add', methods=["GET","POST"])
@check_is_provider
@check_login
def add_dish():
    # need provider_id, name of dish to save a dish
    p=Provider.get_provider(g.user.id)
    
    data=get_empty_dish_info()
    
    if p[0] and data[0]: 
        p=p[1] 
        resp,m,all_restrict,all_categories,form_d,form_cat,form_restrict=data
        
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
                'category_id':form_cat.categories.data,
                'max_meals':form_d.max_meals.data,
                'related_to_dish':form_d.related_to_dish.data,
                'pass_guidelines':form_d.pass_guidelines.data,
                'active':form_d.active.data
            }
           
            res=Dish.insert_dish(fd=d_form)
            
            if res[0]:
                # get dish id from here
                d=res[1]
                #save restrictions
                
                resrestrict=Restriction_Dish.set_restrictions(id=d.id,fr=form_restrict.restrictions.data)
                
                # save pic of dish if uploaded
                
                file=save_image(form_file='dishImage', remove=False, folder='dishes', file_name=f'{str(g.user.id)}-{d.id}')
                
                if file[0]:
                    #if file was saved successfully, update the dish 
                    d.dish_image=file[1]
                    res_d=d.update_one(property='dish_image', data=file[1])
                    
                else:
                    flash_error (f'''Trouble saving file: {file[1]}''')
                    return redirect(url_for("providers_bp.add_dish")) 
                
                if resrestrict[0] and res_d[0]:
                    flash_success(f'Data saved')
                    return redirect(url_for("providers_bp.home"))
                    
                else: 
                    if not resrestrict[0]:
                        flash_error (f'''Trouble saving restrictions: {resrestrict[1]}''')
                    if not res_d[0]:
                        flash_error (f'''Trouble saving image name: {res_d[1]}''')    
                    return redirect(url_for("providers_bp.add_dish")) 
            else:
                flash_error (f'Trouble saving dish information: {res[1]}')
                return redirect(url_for("providers_bp.add_dish"))   
        else:        
            return render_template("providers_add_dish.html",form_d=form_d,form_restrict=form_restrict, form_cat=form_cat)
    else:
        if not p[0]:
            flash_error(f"Trouble getting profile: {p[1]}")
        return redirect(url_for('providers_bp.home'))


@providers_bp.route('/dishes/<int:id>', methods=['GET'])    
@check_is_provider
@check_login
def view_dish(id):
    d=Dish.get_dish(id)
    data=get_empty_dish_info()
    
    if d[0] and not d[1] is None and data[0]: 
        d=d[1]
        resp,m, all_restrict,all_categories,form_d,form_cat,form_restrict=data
        # get saved related to dish
        related_to_dish=""
        if d.related_to_dish:
            related_to_dish=Dish.get_name(d.related_to_dish)
            if related_to_dish[0]:
                related_to_dish=related_to_dish[1]
            else:
                flash_error(f'Trouble getting related dish name: {related_to_dish[1]}')
                return redirect(url_for('providers_bp.home'))
        
        # get saved category
        category=Category.get_name(id=d.category_id)
        if category[0]:
            category=category[1]
        else:
            flash_error(f"""Trouble getting category of dish: {category[1]}""")

        # get saved restrictions
        restrict=Restriction_Dish.get_restrictions(id=d.id)
        if restrict[0]:
            restrict=restrict[1]
        else:
            flash_error(f'Trouble getting restrictions: {restrict[1]}')
            return redirect(url_for('providers_bp.home'))
      
        form_restrict.restrictions.data=[r.restriction_id for r in restrict]

        if d.dish_image and not d.dish_image is None:
            d.dish_image=path_to_file(saved_file=d.dish_image, folder='dishes')
            
        return render_template("providers_display_dish.html",category=category,related_to_dish=related_to_dish,d=d,form_restrict=form_restrict)
            
    else:
        if not d[0]:
            flash_error(f"Trouble getting dish information: {d[1]}")
        return redirect(url_for('providers_bp.home')) 

# for editing - new
@providers_bp.route('/dishes/<int:id>/edit', methods=['GET'])
@check_is_provider
@check_login
def edit_dish(id):
    d=Dish.get_dish(id)
    
    if d[0] and not d[1] is None: 
        data=get_empty_dish_info()
        d=d[1]
        if data[0]:
            resp,m,all_restrict,all_categories,form_d,form_cat,form_restrict=data
        else:
            flash_error(f""" m: {m[1]}
              restrictions: {all_restrict[1]}
              categories: {all_categories[1]}""")
            
        restrict=Restriction_Dish.get_restrictions(id=d.id)
        if restrict[0]:
            restrict=restrict[1]
        else:
            flash_error(f'Trouble getting restrictions: {restrict[1]}')
            return redirect(url_for('providers_bp.home'))
        
        form_d=DishInfoForm(obj=d)  #redefine and overwrite the existing form_d that is empty
        form_restrict.restrictions.data=[r.restriction_id for r in restrict]
        form_cat.categories.data=d.category_id
        form_d,d=related_dish_dropdown(m,form_d,d)
      
        if form_d.dish_image.data and not form_d.dish_image.data is None:
            form_d.dish_image.data=path_to_file(saved_file=d.dish_image, folder='dishes')
            
        return render_template("providers_edit_dish.html",form_cat=form_cat,form_d=form_d,form_restrict=form_restrict, id=d.id)
            
    else:
        if not d[0]:
            flash_error(f"""Trouble getting dish information: {d[1]}""")
        return redirect(url_for('providers_bp.home')) 
    
def related_dish_dropdown(m,form_d,d):
    if m:
        # user can select which dish they want to link to (because we are adding a new dish)
        form_d.related_to_dish.choices=[("", "---")]+[(di.id, di.name) for di in m if not di.id is d.id]
    else:
        form_d.related_to_dish.choices=[("", "---")]
    return (form_d,d)

@providers_bp.route('/dishes/<int:id>/edit', methods=["POST"])
@check_is_provider
@check_login
def update_dish(id):

    d=Dish.get_dish(id)
    if(request.form.get('removeImage')):
        if d[0] and not d[1] is None:
            if d[1].dish_image and not d[1].dish_image is None:
                res_image=remove_image(file_name_old=d[1].dish_image,folder='dishes')
                if res_image[0]:
                    res_dish_image_data=d[1].update_one(property='dish_image',data=None)
                    if not res_dish_image_data[0]:
                        flash_error(f'Removed image but had trouble removing image name from profile: {res_dish_image_data[1]}')
                else:
                    flash_error(f'Trouble deleting image: {res_image[1]}')
    
    
    data=get_empty_dish_info()
    
    if d[0] and not d[1] is None and data[0]:
        d=d[1]
        resp,m, all_restrict,all_categories,form_d,form_cat,form_restrict=data
        form_d=DishInfoForm(obj=d) #overwrite form with form that has data
        form_d,d=related_dish_dropdown(m,form_d,d)
                      
        if form_d.validate_on_submit() and form_restrict.validate_on_submit() and form_cat.validate_on_submit():
            
            # save pic of dish if uploaded
            # file=save_image(form_file='dishImage', remove=True, folder='dishes', file_name=f'{str(g.user.id)}-{d.id}')
            
            # write to database
            # create an object to pass
            
            d_form={
                'provider_id':g.user.id,
                'name':form_d.name.data,
                'recipe':form_d.recipe.data,
                'num_servings':form_d.num_servings.data,
                'ingred_disp':form_d.ingred_disp.data,
                'category_id':form_cat.categories.data,
                'price':form_d.price.data,
                'sales_pitch':form_d.sales_pitch.data,
                'max_meals':form_d.max_meals.data,
                'related_to_dish':form_d.related_to_dish.data,
                'pass_guidelines':form_d.pass_guidelines.data,
                'active':form_d.active.data
            }
            
            res=d.update_dish(fd=d_form)
            
            #save restrictions
            resrestrict=Restriction_Dish.set_restrictions(id=d.id,fr=form_restrict.restrictions.data)
            
             # save pic of dish if uploaded
             
            file=save_image(form_file='dishImage', remove=True, folder='dishes', file_name=f'{str(g.user.id)}-{d.id}', file_name_old=d.dish_image)
            if file[0] and not file[1]=='not submitted':
                d.dish_image=file[1]
                res_d=d.update_one(property='dish_image', data=file[1])
                if not res_d[0]:
                    flash_error (f'''Trouble saving image name: {res_d[1]}''')    
            
            if resrestrict[0] and file[0] and res[0]:
                flash_success(f'Data saved')
                return redirect(url_for("providers_bp.edit_dish", id=d.id))
                
            else: 
                if not file[0]:
                    flash_error (f'''Trouble saving image: {file[1]}''')    
                if not res[0]:
                    flash_error(f'Trouble saving dish information: {res[1]}')
                if not resrestrict[0]:
                    flash_error(f'Trouble saving restrictions: {resrestrict[1]}')
        
        # return render_template("providers_edit_dish.html",form_cat=form_cat,form=form,form_restrict=form_restrict, id=d.id)
                return redirect(url_for("providers_bp.edit_dish", id=d.id))
        else:
            if not form_d.errors:
                flash_error (f'''Trouble with dish form: {form_d.errors}''')    
            if not form_restrict[0]:
                flash_error(f'Trouble saving dish information: {form_restrict.errors}')
            if not form_cat[0]:
                flash_error(f'Trouble saving restrictions: {form_cat.errors}')
            
    else:
        return redirect(url_for('providers_bp.view_dish',id=id)) 
    
@providers_bp.route('/dishes/<int:id>/delete', methods=['POST'])
@check_is_provider
@check_login
def delete_dish(id):
    d=Dish.get_dish(id)
    if d[0] and not d[1] is None:
        d=d[1]
        # remove file if available
        if d.dish_image and not d.dish_image is None:
            res_image=remove_image(file_name_old=d.dish_image,folder='dishes')
            if not res_image[0]:
                flash_error(f'Trouble deleting image: {res_image[1]}')
                
        res=d.delete_dish()
        if res[0]:
            flash_success(f'Dish deleted')
            return redirect(url_for('providers_bp.home'))
        else:
            flash_error(f'Trouble deleting dish: {res[1]}')
            return redirect(url_for('providers_bp.edit_dish', id=id))
    else:
        flash_error(f'Trouble getting dish data: {d[1]}')
        return redirect(url_for('providers_bp.edit_dish', id=id))
    
@providers_bp.route('/delete', methods=['POST'])
@check_is_provider
@check_login
def delete_prov():
    # get provider
    p=Provider.get_provider(g.user.id)

    if p[0]:
        p=p[1]
        m=Dish.get_menu(g.user.id)
        if m[0]:
            m=m[1]
            for d in m:
                if d.dish_image and not d.dish_image is None:
                    res_image=remove_image(file_name_old=d.dish_image,folder='dishes')
                    if not res_image[0]:
                        flash_error(f'Trouble deleting image: {res_image[1]}')
        else:
            flash_error(f'Trouble loading all the dishes: {m[1]}')
        res=p.delete()
        if res[0]:
            flash_success(f'Sorry to see you go! Your profile has been deleted.')
            return redirect(url_for('general_bp.home'))
        else:
            flash_error(f'Trouble deleting profile: {res[1]}')
            return redirect(url_for('providers_bp.edit_info'))
    else:
        flash_error(f'Trouble getting profile: {p[1]}')
        return redirect(url_for('providers_bp.edit_info'))
    