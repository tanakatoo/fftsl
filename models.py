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
    email=db.Column(db.Text,
                   nullable=False) #NEED TO MAKE THIS UNIQUE IN PRODUCTION
    password=db.Column(db.Text, nullable=False)
    user_type=db.Column(db.Text, nullable=False)
    
    db.relationship("School", back_populates="users", cascade='save-update, merge, delete')
    
    @classmethod
    def register(cls,email,user_type,pwd=""):
        # this is to register schools or providers only
        # no need for user to set password yet until they are authorized manually
        # we set a fake random generated password first
        
        if user_type == "provider" or user_type=="school":
            random_password=""
            for num in range(10):
                random_password += str(random.randint(0,9))
            hashed=bcrypt.generate_password_hash(random_password)
            pwd=hashed.decode("utf8")
           
        u=cls(email=email,password=pwd, user_type=user_type)
        
        try:
            db.session.add(u)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    
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
    def get_user(self, email):
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
            flash('Password set/reset has been expired. Please input email to obtain a new one')
            return (False,e)
        

class City(db.Model):
    __tablename__='cities'
    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    name=db.Column(db.Text,
                   nullable=False)

class Province(db.Model):
    __tablename__='provinces'
    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    name=db.Column(db.Text,
                   nullable=False)

class School(db.Model):
    __tablename__='schools'
    def __repr__(self):
        return f"<id={self.id}, name={self.name}>"
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    name=db.Column(db.Text,
                   nullable=False, unique=True)
    address=db.Column(db.Text)
    city_id=db.Column(db.Integer, db.ForeignKey('cities.id'))
    province_id=db.Column(db.Integer,db.ForeignKey('provinces.id'))
    principal_name=db.Column(db.Text)
    contact_name=db.Column(db.Text)
    phone=db.Column(db.Integer)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    active=db.Column(db.Boolean, nullable=False,default=True)
    
#     db.relationship('User', back_populates="schools", cascade='save-update, merge, delete')
    
    @classmethod
    def register(cls,name):
        print('**********')
        print('in  registering school')
        s=cls(name=name)
        print('**********')
        print('made school object ')
        print(s)
        try:
            db.session.add(s)
            db.session.commit()
            return s
        except Exception as e:
            db.session.rollback()
            return False
    
# class Recurring_Days(db.Model):
#     __tablename__='recurring_days'
#     def __repr__(self):
#         return f"<id={self.id}, days={self.day}>"
    
#     id= db.Column(db.Integer,
#                   primary_key=True,
#                   autoincrement=True)
#     day=db.Column(db.Text,
#                    nullable=False, unique=True)

# class Recurring_availability(db.Model):
#     __tablename__='recurring_availabilities'
#     def __repr__(self):
#         return f"<id={self.id}, provider_id={self.provider_id}, recurring_day_id={self.recurring_day_id}>"
    
#     provider_id= db.Column(db.Integer,
#                   primary_key=True)
#     recurring_day_id= db.Column(db.Integer,
#                   primary_key=True)

# class Provider(db.Model):
#     __tablename__='providers'
#     def __repr__(self):
#         return f"<id={self.id}, name={self.name}>"
    
#     id= db.Column(db.Integer,
#                   primary_key=True,
#                   autoincrement=True)
#     name=db.Column(db.Text,
#                    nullable=False, unique=True)
#     address=db.Column(db.Text)
#     city_id=db.Column(db.Integer, db.ForeignKey('cities.id'))
#     province_id=db.Column(db.Integer,db.ForeignKey('provinces.id'))
#     contact_name=db.Column(db.Text)
#     phone=db.Column(db.Integer)
#     user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
#     sales_pitch=db.Column(db.Text)
#     max_meals_per_day=db.Column(db.Integer)
#     serve_num_schools_per_day=db.Column(db.Integer)
#     active=db.Column(db.Boolean, nullable=False,default=True)
    
#     recurring_availabilities=db.relationship("Recurring_days", secondary="recurring_availabilities",back_populates="providers")
#     users=db.relationship('User', back_populates="schools", cascade='save-update, merge, delete')
