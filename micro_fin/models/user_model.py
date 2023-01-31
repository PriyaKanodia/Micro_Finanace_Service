# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

import bcrypt as bcrypt
from micro_fin import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    gender = db.Column(db.String(64))
    country_code = db.Column(db.String(8))
    mobile_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    country = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(32))
    pan_number = db.Column(db.String(120))
    location = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)
    
    transaction = db.relationship("TransactionHistoryModel", backref="user_transaction")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def temp_save(self):
        db.session.add(self)
        db.session.flush()

    def to_json(self):
        not_convert_into_str = ['id', 'active', 'created_by', 'updated_by']
        user_data = {col.name: (str(getattr(self, col.name)) if (
                getattr(self, col.name) is not None and col.name not in not_convert_into_str) else getattr(self,
                                                                                                           col.name))
                     for col in self.__table__.columns if col.name != 'password'}
        return user_data

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id, is_active=True):
        if is_active:
            return cls.query.filter_by(id=user_id, active=True).first()
        return cls.query.get(user_id)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_mobile(cls, country_code, mobile):
        return cls.query.filter_by(country_code=country_code, mobile_number=mobile).first()

    @classmethod
    def find_all(cls):
        return [user.to_json() for user in cls.query.all()]

    @staticmethod
    def generate_password_hash(password):
        return str(bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(10)).decode('utf8'))

    @staticmethod
    def verify_hash(password, hashed):
        return bcrypt.checkpw(password.encode('utf8'), hashed.encode('utf8'))
