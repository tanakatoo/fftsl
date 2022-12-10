from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
from jwt.exceptions import ExpiredSignatureError
import os
from datetime import datetime, timedelta
from flask import flash
import random
from decimal import Decimal
from datetime import date, datetime

db=SQLAlchemy()
bcrypt=Bcrypt()

def connect_db(app):
    db.app=app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    __tablename__='users'
    def __repr__(self):
        return f"<id={self.id}, email={self.email}, user_type={self.user_type}, active={self.active}>"
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    email=db.Column(db.String(100),
                   nullable=False) #NEED TO MAKE THIS UNIQUE IN PRODUCTION
    password=db.Column(db.Text, nullable=False)
    user_type=db.Column(db.String(10), nullable=False)
    active=db.Column(db.Boolean,nullable=False,default=False)
    
    school = db.relationship("School", back_populates="user")
    provider=db.relationship("Provider", back_populates="user")
    
    @classmethod
    def register(cls,email,user_type,pwd=""):
        # this is to register schools or providers only
        # no need for user to set password yet until they are authorized manually
        # we set a fake random generated password first
        try:
            if user_type == "provider" or user_type=="school":
                random_password=""
                for num in range(10):
                    random_password += str(random.randint(0,9))
                hashed=bcrypt.generate_password_hash(random_password)
                pwd=hashed.decode("utf8")
            
            u=cls(email=email,password=pwd, user_type=user_type)
            db.session.add(u)
            db.session.commit()
            return (True,u)
        except Exception as e:
            db.session.rollback()
            return (False,e)
    
    @classmethod
    def authenticate(self, email, pwd):
        u=User.query.filter_by(email=email).first()
        if u and bcrypt.check_password_hash(u.password,pwd):
            return u
        return False
    
    @classmethod
    def set_password(self, email, pwd):
        hashed=bcrypt.generate_password_hash(pwd)
        hashed_utf8=hashed.decode("utf8")
        u=User.query.filter_by(email=email).first()
        u.password=hashed_utf8
        try:
            db.session.add(u)
            db.session.commit()
            return (True,u)
        except Exception as e:
            return (False,e)
    
    @classmethod
    def get_user(cls, email=None, id=None):
        if id:
            u=User.query.get(id)
        else:
            u=User.query.filter_by(email=email).first()
        return u
    
    def get_secret_key(self):
        # this is the code (link) we send via email to user
        key=jwt.encode({'email':self.email, 'exp': datetime.now() + timedelta(days=5)},os.environ.get("SECRET_KEY"))
        return key
    
            
    @classmethod
    def confirm_secret_key(self,key):
        try:
            al=jwt.get_unverified_header(key)
            res=jwt.decode(key,key=os.environ.get("SECRET_KEY"),algorithms=[al['alg'], ])
            return (True,res)
        except ExpiredSignatureError as e:
            flash('Password set/reset has been expired. Please input email to obtain a new one', 'failure_bkg')
            return (False,e)
        

class City(db.Model):
    __tablename__='cities'
    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    name=db.Column(db.String(100),
                   nullable=False)
    
    school=db.relationship('School', back_populates='city')
    provider=db.relationship('Provider', back_populates='city')
    
    @classmethod
    def get_cities(cls):
        return City.query.all()
    
    @classmethod
    def get_name(cls,id):
        c=City.query.get(id)
        return c.name

class Province(db.Model):
    __tablename__='provinces'
    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    name=db.Column(db.String(80),
                   nullable=False)
    
    school=db.relationship('School', back_populates='province')
    provider=db.relationship('Provider', back_populates='province')
    
    @classmethod
    def get_name(cls,id):
        p=Province.query.get(id)
        return p.name
    
    @classmethod
    def get_provinces(cls):
        p=Province.query.all()
        return p

class School(db.Model):
    __tablename__='schools'
    def __repr__(self):
        return f"<id={self.user_id}, name={self.name}>"
    
    user_id= db.Column(db.Integer,
                  db.ForeignKey('users.id'),
                  primary_key=True)
    name=db.Column(db.String(200),
                   nullable=False, unique=True)
    address=db.Column(db.Text)
    city_id=db.Column(db.Integer, db.ForeignKey('cities.id'))
    province_id=db.Column(db.Integer,db.ForeignKey('provinces.id'))
    principal_name=db.Column(db.String(100))
    contact_name=db.Column(db.String(100))
    phone=db.Column(db.String(50))
    active=db.Column(db.Boolean, nullable=False,default=True)
    
    user=db.relationship('User',back_populates="school")
    city=db.relationship('City', back_populates="school")
    province=db.relationship('Province', back_populates="school")
    
    @classmethod
    def register(cls,name, user_id):
        s=cls(name=name, user_id=user_id)
        try:
            db.session.add(s)
            db.session.commit()
            return (True,s)
        except Exception as e:
            db.session.rollback()
            return (False,e)
    
class Recurring_Days(db.Model):
    __tablename__='recurring_days'
    def __repr__(self):
        return f"<id={self.id}, days={self.day}>"
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    day=db.Column(db.String(10),
                   nullable=False, 
                   unique=True)
    
    providers=db.relationship("Provider", secondary="recurring_availabilities",back_populates="recurring_days")
    
    @classmethod
    def get_all_days(cls):
        try:
            d=Recurring_Days.query.all()
            return (True,d)
        except Exception as e:
            return (False,e)

class Recurring_availability(db.Model):
    __tablename__='recurring_availabilities'
    def __repr__(self):
        return f"provider_id={self.provider_id}, recurring_day_id={self.recurring_day_id}>"
    
    provider_id= db.Column(db.Integer,
                           db.ForeignKey('providers.user_id'),
                           primary_key=True)
    recurring_day_id= db.Column(db.Integer,
                                db.ForeignKey('recurring_days.id'),
                                primary_key=True)
    
    @classmethod
    def get_days(cls,u):
        try:
            d=Recurring_availability.query.filter_by(provider_id=u.id).all()
            return (True, d)
        except Exception as e:
            return (False, e)
    
    @classmethod
    def set_days(cls,u,fd):
        try:
            # fd is list of the days IDs
            # delete all the records associated with user first
            Recurring_availability.query.filter_by(provider_id=u.id).delete()
            db.session.commit()
            # then add all the records again
            for id in fd:
                d=Recurring_availability(provider_id=u.id,recurring_day_id=id)
                db.session.add(d)
                db.session.commit()

            return (True, fd)
        except Exception as e:
            db.session.rollback()
            return (False, e)

class Date_provider_avail(db.Model):
    __tablename__='dates_provider_avail'
    def __repr__(self):
        return f"<provider_id={self.provider_id}, date={self.date}>"

    provider_id= db.Column(db.Integer,
                           db.ForeignKey('providers.user_id'),
                           primary_key=True)
    date = db.Column(db.Date,
                     primary_key=True,
                     nullable=False)
    
    providers=db.relationship('Provider',back_populates="dates_provider_avail")
    
    @classmethod
    def set_dates(cls,u,dates):
        try:
            # parse into list
            list_dates=dates.split(',')
            for d in list_dates:
                date=Date_provider_avail(provider_id=u.id,date=d)
                db.session.add(date)
                db.session.commit()
            return (True,dates)
        except Exception as e:
            return (False, e)
    
    @classmethod
    def get_dates(cls,u):
        try:
            # delete the ones that are before today
            res=cls.remove_old_dates(u)
            if res:
                dates=Date_provider_avail.query.filter_by(provider_id=u.id).order_by(Date_provider_avail.date.asc).all()
                return (True,dates)
            else:
                return (False,'Error in getting provider dates')
            
        except Exception as e:
            return (False, e)
        
    def remove_old_dates(u):
        try:
            dates=Date_provider_avail.query.filter_by(provider_id=u.id).all()

            # get today's date
            # compare and if it's older, delete from db
            today=date.today().strftime("%Y-%m-%d")
            t=datetime.strptime(today,"%Y-%m-%d").date()

            for d in dates:
                if d.date < t:
                    db.session.delete(d)
                    db.session.commit()
            return True
        except Exception as e:
            return False


class Provider(db.Model):
    __tablename__='providers'
    
    def __repr__(self):
        return f"""<id={self.user_id}, name={self.name}, 
            address={self.address},
            city_id={self.city_id},
            province_id={self.province_id},
            geocode_lat={self.geocode_lat},
            geocode_long={self.geocode_long},
            contact_name={self.contact_name},
            phone={self.phone},
            sales_pitch={self.sales_pitch},
            max_meals_per_day={self.max_meals_per_day}
            min_meals={self.min_meals},
            serve_num_org_per_day={self.serve_num_org_per_day},
            active={self.active}>
            """
    
    user_id= db.Column(db.Integer,
                  db.ForeignKey('users.id'),
                  primary_key=True)
    name=db.Column(db.String(200),
                   nullable=False, 
                   unique=True)
    address=db.Column(db.Text)
    city_id=db.Column(db.Integer,
                      db.ForeignKey('cities.id'))
    province_id=db.Column(db.Integer,
                          db.ForeignKey('provinces.id'))
    geocode_lat=db.Column(db.Numeric(11,6))
    geocode_long=db.Column(db.Numeric(11,6))
    contact_name=db.Column(db.String(100))
    phone=db.Column(db.String(50))
    sales_pitch=db.Column(db.Text)
    max_meals_per_day=db.Column(db.String(50))
    min_meals=db.Column(db.String(50))
    serve_num_org_per_day=db.Column(db.String(50))
    active=db.Column(db.Boolean, 
                     nullable=False,
                     default=True)
    
    city=db.relationship("City", back_populates="provider")
    province=db.relationship("Province", back_populates="provider")
    recurring_days=db.relationship("Recurring_Days", secondary="recurring_availabilities",back_populates="providers", cascade='save-update, merge, delete')
    user=db.relationship('User', back_populates="provider")
    dishes=db.relationship('Dish',back_populates="provider", cascade='save-update, merge, delete')
    cuisines=db.relationship("Cuisine", secondary="cuisine_providers",back_populates="providers", cascade='save-update, merge, delete')
    dates_provider_avail=db.relationship('Date_provider_avail',back_populates="providers", cascade='save-update, merge, delete')
    
    @classmethod
    def get_provider(cls, u):
        try:
            p=Provider.query.filter_by(user_id=u.id).first()
            return (True,p)
        except Exception as e:
            return (False,e)

   
    @classmethod
    def set_provider(cls, fp, u,p=None):
        try:
             # change geocode to null if it is empty string
            if fp['geocode_lat']=='':
                geocode_lat=None
            else:
                geocode_lat=Decimal(fp['geocode_lat'])
            if fp['geocode_long']=='':
                geocode_long=None
            else:
                geocode_long=Decimal(fp['geocode_long'])
            if p:
                # there is data, so they are updating
                p.name=fp['name']
                p.address=fp['address']
                p.city_id=int(fp['city_id'])
                p.province_id=int(fp['province_id'])
                p.contact_name=fp['contact_name']
                p.phone=fp['phone']
                p.sales_pitch=fp['sales_pitch']
                p.active=fp['active']
                p.geocode_lat=geocode_lat
                p.geocode_long=geocode_long

            else:
  
                # they are creating a record for the first time, make a new provider
                p=Provider(user_id=u.id,
                           name=fp['name'],
                      address=fp['address'],
                      city_id=int(fp['city_id']),
                      province_id=int(fp['province_id']),
                      contact_name=fp['contact_name'],
                      phone=fp['phone'],
                      sales_pitch=fp['sales_pitch'],
                      active=fp['active'],
                geocode_lat=geocode_lat,
                geocode_long=geocode_long)

            # also need to update email in user table
            # get the user first
            u=User.query.get(u.id)
            u.email=fp['email']

            db.session.add(u)
            db.session.add(p)
            db.session.commit()
            return (True, p)
        except Exception as e:
            db.session.rollback()
            return (False,e)

    def set_settings(self,fp):
        try:
            self.max_meals_per_day=fp['max_meals_per_day']
            self.min_meals=fp['min_meals']
            self.serve_num_org_per_day=fp['serve_num_org_per_day']
            
            db.session.add(self)
            db.session.commit()
            return (True,self)
        except Exception as e:
            return (False,e)
   
class Dish(db.Model):
    __tablename__="dishes"
    
    def __repr__(self):
        return f"<id={self.id}, name={self.name}, pass_guidelines={self.pass_guidelines}>"
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    provider_id=db.Column(db.Integer,
                          db.ForeignKey('providers.user_id'),
                          nullable=False)
    name=db.Column(db.String(200),
                   nullable=False, 
                   unique=True)
    recipe=db.Column(db.Text)
    num_servings=db.Column(db.Integer)
    ingred_disp=db.Column(db.Text)
    price=db.Column(db.Numeric(5,2))
    sales_pitch=db.Column(db.Text)
    pass_guidelines=db.Column(db.Boolean,
                              nullable=False,
                              default=False)
    max_meals=db.Column(db.Integer)
    related_to_dish=db.Column(db.Integer)
    active=db.Column(db.Boolean,
                     nullable=False,
                     default=True)
    
    provider=db.relationship("Provider", back_populates="dishes")
    
    @classmethod
    def get_menu(cls,u):
        try:
            m=Dish.query.filter_by(provider_id=u.id).all()
            return (True,m)
        except Exception as e:
            return (False,e)

    @classmethod
    def get_dish(cls,id):
        try:
            d=Dish.query.get(id)
            return (True,d)
        except Exception as e:
            return (False,e)
        
    @classmethod
    def set_dish(cls, fd):
        """make a record of a new dish"""

        if fd['related_to_dish']=='':
            related_to_dish=None
        else:
            related_to_dish=int(fd['related_to_dish'])
        if fd['num_servings']=='' or fd['num_servings'] is None:
            num_servings=None
        else:
            num_servings=int(fd['num_servings'])
        if fd['price']=='' or fd['price'] is None:
            price=None
        else:
            price=Decimal(fd['price'])
        if fd['max_meals']=='' or fd['max_meals'] is None:
            max_meals=None
        else:
            max_meals=int(fd['max_meals'])
        
        try:
            d=Dish(provider_id=fd['provider_id'],
                        name=fd['name'],
                        recipe=fd['recipe'],
                        num_servings=num_servings,
                        ingred_disp=fd['ingred_disp'],
                        price=price,
                        sales_pitch=fd['sales_pitch'],
                        max_meals=max_meals,
                        related_to_dish=related_to_dish,
                        pass_guidelines=fd['pass_guidelines'],
                        active=fd['active']
                   )
            print(d)
            db.session.add(d)
            db.session.commit()
            return (True, d)
        except Exception as e:
            db.session.rollback()
            return (False,e)

class Cuisine(db.Model):
    __tablename__="cuisines"
    
    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    name=db.Column(db.String(50), 
                   unique=True)
     
    providers=db.relationship("Provider", secondary="cuisine_providers",back_populates="cuisines")

    @classmethod
    def get_all_cuisines(cls):
        try:
            c=Cuisine.query.all()
            return (True,c)
        except Exception as e:
            return (False,e)
    
    @classmethod
    def set_cuisine(cls, name):
        try:
            c=Cuisine(name=name)
            db.session.add(c)
            db.session.commit()
            return (True,c)
        except Exception as e:
            db.session.rollback()
            return (False,e)

class Cuisine_Provider(db.Model):
    __tablename__='cuisine_providers'
    def __repr__(self):
        return f"<provider_id={self.provider_id}, cuisine_id={self.cuisine_id}>"
    
    provider_id= db.Column(db.Integer,
                           db.ForeignKey('providers.user_id'),
                           primary_key=True)
    cuisine_id= db.Column(db.Integer,
                                db.ForeignKey('cuisines.id'),
                                primary_key=True)
    
    @classmethod
    def get_cuisines(cls,u):
        try:
            c=Cuisine_Provider.query.filter_by(provider_id=u.id).all()
            return (True, c)
        except Exception as e:
            return (False, e)
    
    @classmethod
    def set_cuisines(cls,u,fc):
        try:
            # fc is list of the cuisine IDs
            # delete all the records associated with user first
            Cuisine_Provider.query.filter_by(provider_id=u.id).delete()
            db.session.commit()
            # then add all the records again
            for id in fc:
                c=Cuisine_Provider(provider_id=u.id,cuisine_id=id)
                db.session.add(c)
                db.session.commit()

            return (True, fc)
        except Exception as e:
            db.session.rollback()
            return (False, e)