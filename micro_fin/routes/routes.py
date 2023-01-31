# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

from micro_fin.controllers.transaction_controller import Account
from micro_fin.controllers.session_controller import LoginSession, LogoutSession
from micro_fin.controllers.transaction_controller import Transaction
from micro_fin.controllers.user_controller import Users
from micro_fin import api

# users
api.add_resource(Users, '/api/user')


# Transaction
api.add_resource(Account, "/api/create_account", "/api/get_account")
api.add_resource(Transaction, "/api/transaction", "/api/transaction/<transaction_type>")


# Sessions
api.add_resource(LoginSession, "/api/session/login")
api.add_resource(LogoutSession, "/api/session/logout")