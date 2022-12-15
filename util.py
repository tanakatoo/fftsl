from models import City, Province

"""Functions used across blueprints"""

def register_new_city(city_id, city_name):
    """If there is a new city name on the form,
        makes new record in city table
        Returns new city id
        otherwise returns the original city_id"""
        
    if city_name:
        # add the new city first 
        c=City.set_city(name=city_name)
        if c[0]:
            city_name=c[1].name
            city_id=c[1].id
            return (True,city_id)
        else:
            return(False, c[1])
    else:
        return (True,city_id)

def set_prov_choices():
    all_provinces=Province.get_provinces()
    
    if all_provinces[0]:
        all_provinces=all_provinces[1]
        provinces=[(pro.id,pro.name) for pro in all_provinces]
        
        return (True, provinces)
    else:
        return (False,all_provinces[1])

def set_city_choices():
    all_cities=City.get_cities()
    
    if all_cities[0]:
        all_cities=all_cities[1]
        cities=[(c.id,c.name) for c in all_cities]
        
        return (True,cities)
    else:
        return (False,all_cities[1])
