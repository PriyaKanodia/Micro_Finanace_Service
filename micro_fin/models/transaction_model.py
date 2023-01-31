# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

from micro_fin import db
from datetime import datetime


class AccountModel(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    balance = db.Column(db.Numeric(19, 2), default=0.0)
    active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    transactions = db.relationship("TransactionHistoryModel", backref="account")


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete()
        db.session.commit()

    @classmethod
    def find_by_id(cls, wallet_id):
        return cls.query.get(wallet_id)

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, active=True).first()


class TransactionHistoryModel(db.Model):
    __tablename__ = 'transaction_history'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(32), unique=True, nullable=False)
    transaction_type = db.Column(db.String(7)) # credit or debit
    amount = db.Column(db.Numeric(19, 2))
    cur_balance = db.Column(db.Numeric(19, 2))
    valid = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete()
        db.session.commit()

    @classmethod
    def find_by_id(cls, wallet_trans_his_id):
        return cls.query.get(wallet_trans_his_id)
    
    @classmethod
    def find_by_transaction_id(cls, transaction_id):
        return  cls.query.filter_by(transaction_id=transaction_id).first()