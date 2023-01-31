# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

from flask_restful import Resource, reqparse
from micro_fin.decorators.authenticated import authenticated
from micro_fin.helper.rest_response import RestResponse
from micro_fin import app
from micro_fin.services.transaction_service import TransactionService

class Account(Resource):
    
    @authenticated()
    def post(self, current_user_id):
        try:
            app.logger.info("Account:post:user_id:{}".format(current_user_id))
            return TransactionService().create_user_account(current_user_id)
        except Exception as e:
            app.logger.error("Account:post:error:{}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500

    @authenticated()
    def get(self, current_user_id):
        try:
            app.logger.info("Account:get:user_id:{}".format(current_user_id))
            return TransactionService().get_user_account(current_user_id)
        except Exception as e:
            app.logger.error("Account:get:error:{}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500

class Transaction(Resource):

    @authenticated()
    def get(self, current_user_id):
        try:
            app.logger.info("Transaction:get:user_id:{}".format(current_user_id))
            return TransactionService().get_user_transactions(current_user_id)
        except Exception as e:
            app.logger.error("Transaction:get:error:{}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500

    @authenticated()
    def post(self, current_user_id, transaction_type):
        try:
            app.logger.info(
                "Transaction:post:user_id:{}".format(current_user_id))
            parse = reqparse.RequestParser()
            parse.add_argument("amount", type=float, required=True, help="Amount can not be blank")
            args = parse.parse_args()
            
            app.logger.debug("Transaction::post::payload::{}".format(args))
            return TransactionService().user_transaction(current_user_id, transaction_type, amount=args['amount'])
        except Exception as e:
            app.logger.error("Transaction:post:error:{}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500