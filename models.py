from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
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
        try:
            c=City.query.order_by('name').all()
            return (True,c)
        except Exception as e:
            return (False, e)
        
    @classmethod
    def get_name(cls,id):
        try:
            c=City.query.get(id)
            return (True,c.name)
        except Exception as e:
            return (False, e)

    
    @classmethod
    def set_city(cls,name):
        try: 
            c=City(name=name)
            db.session.add(c)
            db.session.commit()
            return (True, c)
        except Exception as e:
            return (False, e)

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
        try:
            p=Province.query.get(id)
            return (True,p.name)
        except Exception as e:
            return (False, e)
    
    @classmethod
    def get_provinces(cls):
        try:
            p=Province.query.order_by('name').all()
            return (True,p)
        except Exception as e:
            return (False, e)


class School(db.Model):
    __tablename__='schools'
    def __repr__(self):
        return f"""<id={self.user_id}, name={self.name},
            address={self.address},
            city_id={self.city_id},
            province_id={self.province_id},
            geocode_lat={self.geocode_lat},
            geocode_long={self.geocode_long},
            contact_name={self.contact_name},
            phone={self.phone},
            principal_name={self.principal_name},
            active={self.active}>>"""
    
    user_id= db.Column(db.Integer,
                  db.ForeignKey('users.id'),
                  primary_key=True)
    name=db.Column(db.String(200),
                   nullable=False, unique=True)
    address=db.Column(db.Text)
    geocode_lat=db.Column(db.Numeric(11,6))
    geocode_long=db.Column(db.Numeric(11,6))
    city_id=db.Column(db.Integer, db.ForeignKey('cities.id'))
    province_id=db.Column(db.Integer,db.ForeignKey('provinces.id'))
    principal_name=db.Column(db.String(100))
    contact_name=db.Column(db.String(100))
    phone=db.Column(db.String(50))
    active=db.Column(db.Boolean, nullable=False,default=True)
    
    user=db.relationship('User',back_populates="school", cascade='save-update, merge, delete')
    city=db.relationship('City', back_populates="school")
    province=db.relationship('Province', back_populates="school")
    dates_avail=db.relationship('Date_avail_school',back_populates="schools", cascade='save-update, merge, delete')
    recurring_days=db.relationship("Recurring_Day",
                                   secondaryjoin="Recurring_availability_school.recurring_day_id == Recurring_Day.id",
                                   secondary="recurring_availabilities_schools",back_populates="schools", cascade='save-update, merge, delete')
    restrictions=db.relationship("Restriction", secondaryjoin="Restriction_School.restriction_id == Restriction.id",
                                 secondary="restrictions_schools",back_populates="schools", cascade='save-update, merge, delete')
    
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
    
    @classmethod
    def get_school(cls, id):
        try:
            s=School.query.filter_by(user_id=id).first()
            return (True,s)
        except Exception as e:
            return (False,e)

   
    @classmethod
    def set_school(cls, fs, id, s):
        
        try:

           # change geocode to null if it is empty string
            if fs['geocode_lat']=='':
                geocode_lat=None
            else:
                geocode_lat=Decimal(fs['geocode_lat'])
            if fs['geocode_long']=='':
                geocode_long=None
            else:
                geocode_long=Decimal(fs['geocode_long'])
            # there is data, so they are updating
            s.name=fs['name']
            s.address=fs['address']
            s.city_id=fs['city_id']
            s.province_id=fs['province_id']
            s.contact_name=fs['contact_name']
            s.principal_name=fs['principal_name']
            s.phone=fs['phone']
            s.active=fs['active']
            s.geocode_lat=geocode_lat
            s.geocode_long=geocode_long

            # also need to update email in user table
            # get the user first
            u=User.query.get(id)
            u.email=fs['email']
            
            db.session.add(u)
            db.session.add(s)
            db.session.commit()
            return (True, s)
        except Exception as e:
            db.session.rollback()
            return (False,e)
        
    def delete(self):
        try:
            # set to null all of the dishes that have this dish as a related dish
            
            db.session.delete(self)
            db.session.commit()
            return (True, "deleted")
        except Exception as e:
            db.session.rollback()
            return (False,e)
            
    
class Recurring_Day(db.Model):
    __tablename__='recurring_days'
    def __repr__(self):
        return f"<id={self.id}, day={self.day}>"
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    day=db.Column(db.String(10),
                   nullable=False, 
                   unique=True)
    
    providers=db.relationship("Provider", 
                                   secondaryjoin="Recurring_availability.provider_id == Provider.user_id",
                                   secondary="recurring_availabilities",back_populates="recurring_days")
    schools=db.relationship("School", 
                            secondaryjoin="Recurring_availability_school.school_id == School.user_id",
                            secondary="recurring_availabilities_schools",back_populates="recurring_days")

    
    @classmethod
    def get_all_days(cls):
        try:
            d=Recurring_Day.query.all()
            return (True,d)
        except Exception as e:
            return (False,e)

class Recurring_availability(db.Model):
    __tablename__='recurring_availabilities'
    def __repr__(self):
        return f"""provider_id={self.provider_id},
            recurring_day_id={self.recurring_day_id},
            start_date={self.start_date},
            end_date={self.end_date}>"""

    provider_id= db.Column(db.Integer,
                           db.ForeignKey('providers.user_id'),
                           primary_key=True)
    
    recurring_day_id= db.Column(db.Integer,
                                db.ForeignKey('recurring_days.id'),
                                nullable=False,
                                primary_key=True)
    start_date=db.Column(db.Date,
                         primary_key=True)
    end_date=db.Column(db.Date,
                       primary_key=True)
    
    @classmethod
    def get_days(cls,id):
        """returns day of week (not id, the word), start date and end date"""
        try:
            d=db.session.query(Recurring_Day.day, Recurring_availability.recurring_day_id,Recurring_availability.start_date,Recurring_availability.end_date).join(Recurring_Day).filter(Recurring_availability.provider_id==id).order_by('start_date').all()
           
            return (True, d)
        except Exception as e:
            return (False, e)
    
    
    @classmethod
    def set_days(cls,id,fd):
        try:
            # fd is list of the days IDs
            # delete all the records associated with user first
            Recurring_availability.query.filter_by(provider_id=id).delete()
            db.session.commit()
            
            # then add all the records again
            for data in fd:
                d=Recurring_availability(provider_id=data['provider_id'],
                                            recurring_day_id=data['recurring_day_id'],
                                            start_date=data['start_date'],
                                            end_date=data['end_date'])
                db.session.add(d)
                db.session.commit()

            return (True, fd)
        except Exception as e:
            db.session.rollback()
            return (False, e)
        
class Recurring_availability_school(db.Model):
    __tablename__='recurring_availabilities_schools'
    def __repr__(self):
        return f"""
            school_id={self.school_id},
            recurring_day_id={self.recurring_day_id},
            start_date={self.start_date},
            end_date={self.end_date}>"""

    school_id= db.Column(db.Integer,
                           db.ForeignKey('schools.user_id'),
                            primary_key=True)
    
    recurring_day_id= db.Column(db.Integer,
                                db.ForeignKey('recurring_days.id'),
                                nullable=False,
                                primary_key=True)
    start_date=db.Column(db.Date,
                         primary_key=True)
    end_date=db.Column(db.Date,
                       primary_key=True)
    
    @classmethod
    def get_days(cls,id):
        """returns day of week (not id, the word), start date and end date"""
        try:
            d=db.session.query(Recurring_Day.day, Recurring_availability_school.recurring_day_id,Recurring_availability_school.start_date,Recurring_availability_school.end_date).join(Recurring_Day).filter(Recurring_availability_school.school_id==id).all()
            return (True, d)
        except Exception as e:
            return (False, e)
    
    
    @classmethod
    def set_days(cls,id,fd):
        try:
            # fd is list of the days IDs
            # delete all the records associated with user first
            Recurring_availability_school.query.filter_by(school_id=id).delete()
            db.session.commit()
            
            # then add all the records again
            for data in fd:
                d=Recurring_availability_school(school_id=data['school_id'],
                                            recurring_day_id=data['recurring_day_id'],
                                            start_date=data['start_date'],
                                            end_date=data['end_date'])
                db.session.add(d)
                db.session.commit()

            return (True, fd)
        except Exception as e:
            db.session.rollback()
            return (False, e)

class Date_avail(db.Model):
    __tablename__='dates_avail'
    def __repr__(self):
        return f"<date={self.date}, provider_id={self.provider_id}>"

    provider_id= db.Column(db.Integer,
                           db.ForeignKey('providers.user_id'),
                           primary_key=True)
                           
    date = db.Column(db.Date,
                     nullable=False,
                     primary_key=True)
    
    providers=db.relationship('Provider',back_populates="dates_avail")

    
    @classmethod
    def set_dates(cls,id,add_dates):
        try:
            # remove all the dates first and then add it back
            dates=Date_avail.query.filter_by(provider_id=id).all()
          
            for d in dates:
                db.session.delete(d)
                db.session.commit()
            # parse add_dates into list if more than 1 date
            if ',' in add_dates:
                list_dates=add_dates.split(',')
                for d in list_dates:
                    d_add=Date_avail(provider_id=id,date=d)
                    db.session.add(d_add)
                    db.session.commit()
            # if not all the dates are delete, add just one date
            elif not add_dates == '':
                d=Date_avail(provider_id=id,date=add_dates)
               
                db.session.add(d)
                db.session.commit()

            return (True,dates)
        except Exception as e:
            return (False, e)
    
    @classmethod
    def get_dates(cls,id):
        try:
            # delete the ones that are before today
            res=cls.remove_old_dates(id)
            if res:
                dates=Date_avail.query.filter_by(provider_id=id).order_by('date').all()
                
                return (True,dates)
            else:
                return (False,'Error in getting available dates')
            
        except Exception as e:
            return (False, e)
        
    def remove_old_dates(id):
        try:
          
            dates=Date_avail.query.filter_by(provider_id=id).all()
            
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

class Date_avail_school(db.Model):
    __tablename__='dates_avail_schools'
    def __repr__(self):
        return f"<date={self.date}, school_id={self.school_id}>"

    school_id=db.Column(db.Integer, 
                        db.ForeignKey('schools.user_id'),
                        primary_key=True)           
    date = db.Column(db.Date,
                     nullable=False,
                     primary_key=True)
    
    schools=db.relationship('School',back_populates="dates_avail")

    
    @classmethod
    def set_dates(cls,id,add_dates):
        try:
            # remove all the dates first and then add it back
            dates=Date_avail_school.query.filter_by(school_id=id).all()
            for d in dates:
                db.session.delete(d)
                db.session.commit()
            # parse add_dates into list if more than 1 date
            if ',' in add_dates:
                list_dates=add_dates.split(',')
                for d in list_dates:
                    d_add=Date_avail_school(school_id=id,date=d)
                    db.session.add(d_add)
                    db.session.commit()
            # if not all the dates are delete, add just one date
            elif not add_dates == '':
                d=Date_avail_school(school_id=id,date=add_dates)
                db.session.add(d)
                db.session.commit()

            return (True,dates)
        except Exception as e:
            return (False, e)
    
    @classmethod
    def get_dates(cls,id):
        # try:
            # delete the ones that are before today
            res=cls.remove_old_dates(id)
            if res:
                dates=Date_avail_school.query.filter_by(school_id=id).all()
                return (True,dates)
            else:
                return (False,'Error in getting available dates')
            
        # except Exception as e:
        #     return (False, e)
        
    def remove_old_dates(id):
        try:
            dates=Date_avail_school.query.filter_by(school_id=id).all()
            
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
        return f"""<user_id={self.user_id}, name={self.name}, 
            website={self.website},
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
            inspection_report={self.inspection_report},
            submit_inspection={self.submit_inspection},
            reviewed={self.reviewed},
            submit_inspection_date={self.submit_inspection_date},
            active={self.active},
            display={self.display}>
            """
    
    user_id= db.Column(db.Integer,
                  db.ForeignKey('users.id'),
                  primary_key=True)
    name=db.Column(db.String(200),
                   nullable=False, 
                   unique=True)
    website=db.Column(db.String(300))
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
    inspection_report=db.Column(db.String(200))
    submit_inspection=db.Column(db.Boolean,
                                nullable=False,
                                default=False)
    reviewed=db.Column(db.Boolean,
                       nullable=False,
                       default=False)
    submit_inspection_date=db.Column(db.Date)
    active=db.Column(db.Boolean, 
                     nullable=False,
                     default=True)
    display=db.Column(db.Boolean,
                      nullable=False,
                      default=False)
    
    city=db.relationship("City", back_populates="provider")
    province=db.relationship("Province", back_populates="provider")
    recurring_days=db.relationship("Recurring_Day",
                                   secondaryjoin="Recurring_availability.recurring_day_id == Recurring_Day.id",
                                   secondary="recurring_availabilities",back_populates="providers", cascade='save-update, merge, delete')
    user=db.relationship('User', back_populates="provider", cascade='save-update, merge, delete')
    dishes=db.relationship('Dish',back_populates="provider", cascade='save-update, merge, delete')
    cuisines=db.relationship("Cuisine", secondary="cuisine_providers",back_populates="providers", cascade='save-update, merge, delete')
    dates_avail=db.relationship('Date_avail',back_populates="providers", cascade='save-update, merge, delete')
    
    
    @classmethod
    def get_provider(cls, id):
        try:
            p=Provider.query.filter_by(user_id=id).first()
            return (True,p)
        except Exception as e:
            return (False,e)

    @classmethod
    def get_to_review(cls):
        ps=Provider.query.filter_by(submit_inspection=True,reviewed=False).all()
        return ps
   
    @classmethod
    def set_provider(cls, fp, id,p=None):
            
        try:
       
            if p:
                # there is data, so they are updating
                p.name=fp['name']
                p.website=fp['website']
                p.address=fp['address']
                p.city_id=fp['city_id']
                p.province_id=fp['province_id']
                p.contact_name=fp['contact_name']
                p.phone=fp['phone']
                p.sales_pitch=fp['sales_pitch']
                p.active=fp['active']
                p.display=fp['display']
                p.geocode_lat=fp['geocode_lat']
                p.geocode_long=fp['geocode_long']
                p.max_meals_per_day=fp['max_meals_per_day']
                p.min_meals=fp['min_meals']
                p.serve_num_org_per_day=fp['serve_num_org_per_day']
                p.submit_inspection=fp['submit_inspection']
                p.submit_inspection_date=fp['submit_inspection_date']

            else:
  
                # they are creating a record for the first time, make a new provider
                p=Provider(user_id=id,
                           name=fp['name'],
                           website=fp['website'],
                        address=fp['address'],
                        city_id=fp['city_id'],
                        province_id=fp['province_id'],
                        contact_name=fp['contact_name'],
                        phone=fp['phone'],
                        sales_pitch=fp['sales_pitch'],
                        active=fp['active'],
                        geocode_lat=fp['geocode_lat'],
                        geocode_long=fp['geocode_long'],
                        max_meals_per_day=fp['max_meals_per_day'],
                        min_meals=fp['min_meals'],
                        serve_num_org_per_day=fp['serve_num_org_per_day'],
                        submit_inspection=fp['submit_inspection'],
                        submit_inspection_date=fp['submit_inspection_date']         
                )
            
            
            # also need to update email in user table
            # get the user first
            u=User.query.get(id)
            u.email=fp['email']

            db.session.add(u)
            db.session.add(p)
            db.session.commit()
            #need to refresh p as p has changed
            db.session.refresh(p)

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
            # once committed, self is gone, so we have to use this so it won't expire and can return self
            # db.session.expire_on_commit = False
            db.session.commit()
            
            return (True,fp)
        except Exception as e:
             return (False,e)
        
    def delete(self):
        try:
            # set to null all of the dishes that have this dish as a related dish
            
            db.session.delete(self)
            db.session.commit()
            return (True, "deleted")
        except Exception as e:
            db.session.rollback()
            return (False,e)
            
        
   
class Dish(db.Model):
    __tablename__="dishes"
    
    def __repr__(self):
        return f"""<id={self.id}, name={self.name}, 
            provider_id={self.provider_id},
            category={self.category_id},
            recipe={self.recipe},
            num_servings={self.num_servings},
            ingred_disp={self.ingred_disp},
            price={self.price},
            sales_pitch={self.sales_pitch},
            max_meals={self.max_meals},
            related_to_dish={self.related_to_dish},
            active={self.active},
            pass_guidelines={self.pass_guidelines},
            dish_image={self.dish_image}>"""
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    provider_id=db.Column(db.Integer,
                          db.ForeignKey('providers.user_id'),
                          nullable=False)
    name=db.Column(db.String(200),
                   nullable=False)
    category_id=db.Column(db.Integer,
                          db.ForeignKey('categories.id'))
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
    dish_image=db.Column(db.String(200))
    active=db.Column(db.Boolean,
                     nullable=False,
                     default=True)
    
    provider=db.relationship("Provider", back_populates="dishes")
    restrictions=db.relationship("Restriction", secondaryjoin="Restriction_Dish.restriction_id == Restriction.id",
                                 secondary="restrictions_dishes",back_populates="dishes", cascade='save-update, merge, delete')
    category=db.relationship("Category", primaryjoin="Category.id==Dish.category_id", back_populates="dishes")
    
    @classmethod
    def get_menu(cls,id):
        try:
            m=Dish.query.filter_by(provider_id=id).all()
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
    def get_name(cls,id):
        try:
            d=Dish.query.get(id)
            return (True,d.name)
        except Exception as e:
            return (False,e)
   
    def update_as_is(self, property,data):
        setattr(self,property,data)

        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        return (True,self)
    
    def update_dish(self,fd):
        """update an existing dish"""
        
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
            self.name=fd['name']
            self.recipe=fd['recipe']
            self.num_servings=num_servings
            self.ingred_disp=fd['ingred_disp']
            self.price=price
            self.category_id=fd['category_id']
            self.sales_pitch=fd['sales_pitch']
            self.max_meals=max_meals
            self.related_to_dish=related_to_dish
            self.pass_guidelines=fd['pass_guidelines']
            self.active=fd['active']
            
            db.session.add(self)
            db.session.commit()
            db.session.refresh(self)
            return (True, self)
        except Exception as e:
            db.session.rollback()
            return (False,e)
        
    @classmethod
    def insert_dish(cls, fd):
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
                        category_id=fd['category_id'],
                        related_to_dish=related_to_dish,
                        pass_guidelines=fd['pass_guidelines'],
                        active=fd['active']
                   )
            db.session.add(d)
            db.session.commit()
            return (True, d)
        except Exception as e:
            db.session.rollback()
            return (False,e)

    def delete_dish(self):
        try:
            # set to null all of the dishes that have this dish as a related dish
            dishes=Dish.query.filter_by(related_to_dish=self.id).all()
            for d in dishes:
                d.related_to_dish = None
            
            db.session.delete(self)
            db.session.commit()
            return (True, "deleted")
        except Exception as e:
            db.session.rollback()
            return (False,e)
        
class Category(db.Model):
    __tablename__="categories"
    
    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    name=db.Column(db.String(50), 
                   unique=True)
     
    dishes=db.relationship("Dish", primaryjoin="Dish.category_id==Category.id", back_populates="category")

    @classmethod
    def get_all_cat(cls):
        try:
            c=Category.query.all()
            return (True,c)
        except Exception as e:
            return (False,e)
    
    @classmethod
    def get_name(cls, id):
        try:
            c=Category.query.get(id)
            return (True,c.name)
        except Exception as e:
            return (False,e)
    
    """In the future if setting categories is a feature"""
    # @classmethod
    # def set_cat(cls, name):
    #     try:
    #         c=Category(name=name)
    #         db.session.add(c)
    #         db.session.commit()
    #         return (True,c)
    #     except Exception as e:
    #         db.session.rollback()
    #         return (False,e)

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
    
    """In the future if setting cuisines is a feature"""
    # @classmethod
    # def set_cuisine(cls, name):
    #     try:
    #         c=Cuisine(name=name)
    #         db.session.add(c)
    #         db.session.commit()
    #         return (True,c)
    #     except Exception as e:
    #         db.session.rollback()
    #         return (False,e)

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
    def get_cuisines(cls,id):
        try:
            c=Cuisine_Provider.query.filter_by(provider_id=id).all()
            return (True, c)
        except Exception as e:
            return (False, e)
    
    @classmethod
    def set_cuisines(cls,id,fc):
        # try:
            
            # fc is list of the cuisine IDs
            # delete all the records associated with user first
            Cuisine_Provider.query.filter_by(provider_id=id).delete()
            db.session.commit()
            # then add all the records again
            for fid in fc:
                c=Cuisine_Provider(provider_id=id,cuisine_id=fid)
                db.session.add(c)
                db.session.commit()

            return (True, fc)
        # except Exception as e:
            db.session.rollback()
            return (False, e)

class Restriction(db.Model):
    __tablename__='restrictions'
    
    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"

    id= db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name=db.Column(db.String(200),
                    nullable=False)
    
    dishes=db.relationship("Dish", secondary="restrictions_dishes",back_populates="restrictions")
    schools=db.relationship("School", secondary="restrictions_schools",back_populates="restrictions")
    
    @classmethod
    def get_restriction_name(cls,id):
        try:
            r=cls.query.filter_by(id=id).first()
            return (True, r)
        except Exception as e:
            return (False, e)
        
    @classmethod
    def get_all_restrict(cls):
        try:
            r=cls.query.all()
            return (True, r)
        except Exception as e:
            return (False, e)
    
        
class Restriction_Dish(db.Model):
    __tablename__='restrictions_dishes'
    
    def __repr__(self):
        return f"<dish_id={self.dish_id}, restriction_id={self.restriction_id}>"
    
    dish_id= db.Column(db.Integer,
                        db.ForeignKey('dishes.id'),
                        primary_key=True)
    restriction_id= db.Column(db.Integer,
                            db.ForeignKey('restrictions.id'),
                            primary_key=True)
    
    
    @classmethod
    def get_restrictions(cls,id):
        try:
            r=Restriction_Dish.query.filter_by(dish_id=id).all()
            return (True, r)
        except Exception as e:
            return (False, e)
    
    @classmethod
    def set_restrictions(cls,id,fr):
        # try:
            # fc is list of the restriction IDs
            # delete all the records associated with user first
            
            Restriction_Dish.query.filter_by(dish_id=id).delete()
            db.session.commit()
            # then add all the records again
            for fid in fr:
                r=Restriction_Dish(dish_id=id,restriction_id=fid)
                db.session.add(r)
                db.session.commit()

            return (True, fr)
        # except Exception as e:
            db.session.rollback()
            return (False, e)


class Restriction_School(db.Model):
    __tablename__='restrictions_schools'
    
    def __repr__(self):
        return f"<school_id={self.school_id}, restriction_id={self.restriction_id}>"
    
    school_id= db.Column(db.Integer,
                        db.ForeignKey('schools.user_id'),
                        primary_key=True)
    restriction_id= db.Column(db.Integer,
                            db.ForeignKey('restrictions.id'),
                            primary_key=True)
    
    @classmethod
    def get_restrictions(cls,id):
        try:
            r=Restriction_School.query.filter_by(school_id=id).all()
            return (True, r)
        except Exception as e:
            return (False, e)
    
    @classmethod
    def set_restrictions(cls,id,fr):
        try:
            # fc is list of the restriction IDs
            # delete all the records associated with user first
            Restriction_School.query.filter_by(school_id=id).delete()
            db.session.commit()
            # then add all the records again
            for fid in fr:
                r=Restriction_School(school_id=id,restriction_id=fid)
                db.session.add(r)
                db.session.commit()

            return (True, fr)
        except Exception as e:
            db.session.rollback()
            return (False, e)
