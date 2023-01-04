from models import City, Province
from flask import request
from general.general import flash_error, flash_success
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, BASEDIR
import os
from PIL import Image

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

def remove_image(file_name_old, folder):
    try:
        if not file_name_old =='' and not file_name_old is None:
            # remove file if file was already there
            path_old = os.path.join(BASEDIR, UPLOAD_FOLDER, folder, file_name_old)
            os.remove(path_old)
            file_ext_old = os.path.splitext(file_name_old)
            path_old = os.path.join(BASEDIR, UPLOAD_FOLDER, folder, f'{file_ext_old[0]}-thumb{file_ext_old[1]}')
            os.remove(path_old)
            return (True,'removed')
        else:
            return (False, 'File name is empty or None')
    except Exception as e:
        return (False,e)
                

def save_image(form_file, remove, folder, file_name, file_name_old=''):
    """ form_file: name of field from the form to get the file
        remove: does a file need to be removed (only True if it is editing a form) 
        folder: which folder in the upload directory should this file be saved in
        file_name: what name should the file be saved as?
        file_name_old
    """
    try:
        if form_file in request.files:
            the_image=request.files[form_file]

            if not the_image.filename == '':
                file_split = os.path.splitext(the_image.filename)
                if file_split[1] in ALLOWED_EXTENSIONS:
                    if remove:
                        res=remove_image(file_name_old, folder)
                        if not res[0]:
                            return (False,res[1])
                    
                    file_name_new=file_name + file_split[1] #make our own file name using userid, dishid
                    path = os.path.join(BASEDIR, UPLOAD_FOLDER, folder,file_name_new)
                    the_image.save(path)
                    
                    """Following code obtained from
                    https://stackoverflow.com/questions/10607468/how-to-reduce-the-image-file-size-using-pil
                    """
                    # optimize photo for saving
                    photo = Image.open(path) #open the image and save a smaller version of it
                    width, height = photo.size
                    TARGET_WIDTH = 500
                    coefficient = width / 500
                    new_height = height / coefficient
                    photo = photo.resize((int(TARGET_WIDTH),int(new_height)),Image.ANTIALIAS)
                    photo.save(path,quality=50)
                    """end of copied code"""
                    
                    # save a small version of it for displaying on frontend
                    thumb_pic=Image.open(path)
                    file_name_thumb=f'{file_name}-thumb{file_split[1]}'
                    thumb_path=os.path.join(BASEDIR, UPLOAD_FOLDER, folder,file_name_thumb)
                    thumb_size=(75,75)
                    thumb_pic.thumbnail(thumb_size)
                    thumb_pic.save(thumb_path)
                    
                    return (True,file_name_new)
                else: 
                    return (False,f"File extension must be one of .pdf, .png, .jpg, .jpeg, .gif. Your file extension was {file_split[1]}")
            else:
                return (True,'not submitted')
        else:
            return (True,'not submitted')
    except Exception as e:
        return (False,e)

def path_to_file(saved_file, folder):
        # display the thumbnail of the report
        file_name_split = os.path.splitext(saved_file)
        filename=os.path.join('/',UPLOAD_FOLDER, folder,f'{file_name_split[0]}-thumb{file_name_split[1]}')
        return filename