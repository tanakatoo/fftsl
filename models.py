from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
from jwt.exceptions import ExpiredSignatureError
import os
from datetime import datetime, timedelta
from flask import flash
import random

db=SQLAlchemy()
bcrypt=Bcrypt()

def connect_db(app):
    db.app=app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    __tablename__='users'
    def __repr__(self):
        return f"<id={self.id}, email={self.email}>"
    
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

class School(db.Model):
    __tablename__='schools'
    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"
    
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

class Recurring_availability(db.Model):
    __tablename__='recurring_availabilities'
    def __repr__(self):
        return f"<id={self.id}, provider_id={self.provider_id}, recurring_day_id={self.recurring_day_id}>"
    
    provider_id= db.Column(db.Integer,
                           db.ForeignKey('providers.user_id'),
                           primary_key=True)
    recurring_day_id= db.Column(db.Integer,
                                db.ForeignKey('recurring_days.id'),
                                primary_key=True)

class Provider(db.Model):
    __tablename__='providers'
    
    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"
    
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
    max_meals_per_day=db.Column(db.Integer)
    min_meals=db.Column(db.Integer)
    serve_num_org_per_day=db.Column(db.Integer)
    active=db.Column(db.Boolean, 
                     nullable=False,
                     default=True)
    
    city=db.relationship("City", back_populates="provider")
    province=db.relationship("Province", back_populates="provider")
    recurring_days=db.relationship("Recurring_Days", secondary="recurring_availabilities",back_populates="providers")
    user=db.relationship('User', back_populates="provider")
    
    @classmethod
    def get_provider(cls, u):
        try:
            p=Provider.query.filter_by(user_id=u.id)
            return (True,p)
        except Exception as e:
            return (False,e)
   
