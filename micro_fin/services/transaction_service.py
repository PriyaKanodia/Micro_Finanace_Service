# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

import uuid
from datetime import datetime
import decimal

from micro_fin.helper.rest_response import RestResponse
from micro_fin.models.user_model import UserModel
from micro_fin.models.transaction_model import AccountModel, TransactionHistoryModel
from micro_fin import app


class TransactionService:
    
    def create_user_account(self, user_id):
        try:
            user = UserModel.find_by_id(user_id)
            if user:
                msg = self._check_user_data(user)
                if msg['status']:
                    existing_account = AccountModel.find_by_user_id(user_id)
                    if not existing_account:
                        print("xxxxxxx")
                        new_account = AccountModel(user_id=user_id)
                        new_account.created_by = new_account.updated_by = user.id
                        new_account.save()
                        data = {}
                        data['user_id'] = user_id
                        data['account_no'] = new_account.id
                        data['balance'] = new_account.balance
                        print(data)
                    else:
                        return RestResponse(err="Account already exists for this user!").to_json(), 400
                    
                    return RestResponse(data, message='Account has been created successfully!', status=1).to_json(), 201
                else:
                    return RestResponse(err="Some fields are missing in user data: {}".format(msg['err'])).to_json(), 403
            else:
                return RestResponse(err="User does not exists!").to_json(), 403
        except Exception as e:
            app.logger.error("TransactionService:create_user_account:: {}".format(str(e)))
            return RestResponse(err='Something went wrong').to_json(), 500

    def get_user_account(self, user_id):
        try:
            user = UserModel.find_by_id(user_id)
            if user:
                existing_account = AccountModel.find_by_user_id(user_id)
                if existing_account:
                    account_details = {
                        "user_id": user.id,
                        "account_no": existing_account.id,
                        "balance": existing_account.balance
                    }
                    return RestResponse(account_details, status=1).to_json(), 201
                else:
                    return RestResponse(err="Account does not exists for this user!").to_json(), 400
            else:
                return RestResponse(err="User does not exists!").to_json(), 403
        except Exception as e:
            app.logger.error("TransactionService:create_user_account:: {}".format(str(e)))
            return RestResponse(err='Something went wrong').to_json(), 500

    def _check_user_data(self, user):
        if not user.pan_number:
            return {'err': "PAN Number is not updated", 'status': 0}
        if not user.address:
            return {'err': "Address is not updated", 'status': 0}
        if not user.country:
            return {'err': "Country is not updated", 'status': 0}
        if not user.city:
            return {'err': "City is not updated", 'status': 0}
        if not user.state:
            return {'err': "State is not updated", 'status': 0}
        if not user.zip_code:
            return {'err': "Zip Code is not updated", 'status': 0}
        return {'err': '', 'status': 1}

    def get_user_transactions(self, user_id):
        try:
            user = UserModel.find_by_id(user_id)
            if user:
                app.logger.info("TransactionService:get_user_transactions:user_id:{}".format(user_id))

                account_data = AccountModel.find_by_user_id(user_id)
                data = {"account_description": {}, "data": []}
                if account_data:
                    data["account_description"]["amount"] = account_data.balance
                    data["account_description"]["created_at"] = account_data.created_at.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                    data["account_description"]["updated_at"] = account_data.updated_at.strftime("%Y-%m-%dT%H:%M:%S.000Z")

                    all_transactions = TransactionHistoryModel.query.order_by(
                        TransactionHistoryModel.created_at.desc()).filter_by(account_id=account_data.id, valid=True).all()
                    
                    trans_data = []
                    for transation in all_transactions:
                        transaction_history_data = {}
                        transaction_history_data['id'] = transation.id
                        transaction_history_data['transaction_type'] = transation.transaction_type
                        transaction_history_data['amount'] = transation.amount
                        transaction_history_data['transaction_id'] = transation.transaction_id
                        transaction_history_data['user_id'] = transation.user_id
                        trans_data.append(transaction_history_data)
                    data['data'] = trans_data

                    return RestResponse(data, status=1).to_json(), 200
                else:
                    app.logger.info(
                        "TransactionService:get_user_transactions:user_id:{}:No account found for this user!".format(
                            user_id))
                    return RestResponse(err="No account found for this user!").to_json(), 400
            else:
                app.logger.info(
                    "TransactionService:get_user_transactions:user_id:{} is not found".format(user_id))
                return RestResponse(err="User is not found!!").to_json(), 400
        except Exception as e:
            app.logger.error("TransactionService:get_user_transactions:error:{}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500

    def user_transaction(self, user_id, transaction_type, amount):
        try:
            user = UserModel.find_by_id(user_id)
            if user:
                app.logger.info("TransactionService:user_transaction:user_id:{}".format(user_id))
                account_data = AccountModel.find_by_user_id(user_id)
                if account_data:
                    balance = account_data.balance
                    
                    # If debit operation
                    if transaction_type == 'debit':
                        tran = 'DR'
                        temp = balance
                        account_data.balance -= decimal.Decimal(amount)
                        if account_data.balance < 0:
                            return RestResponse(
                                err="Low Balance! Your current balance is {} and you are trying to deduct {}".format(
                                    temp, amount)).to_json(), 400
                        account_data.updated_at = datetime.now()
                        account_data.updated_by = user_id
                        cur_balance = account_data.balance
                        account_data.save()
                    
                    # If credit operation
                    if transaction_type == 'credit':
                        tran = 'CR'
                        account_data.balance += decimal.Decimal(amount)
                        account_data.updated_at = datetime.now()
                        account_data.updated_by = user_id
                        cur_balance = account_data.balance
                        account_data.save()
                    
                    transaction_history_obj = TransactionHistoryModel(
                        transaction_type=transaction_type, amount=amount,
                        account=account_data, cur_balance=cur_balance,
                        valid=True, transaction_id='RADISYS/' + tran + '/' + uuid.uuid4().hex[:12],
                        created_by=user_id,
                        updated_by=user_id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    transaction_history_obj.save()
                    return RestResponse(
                        {"user_id": user_id, "amount": amount, "transaction_type": transaction_type},
                        message="{} operation has been done successfully!!!".format(transaction_type.capitalize()),
                        status=1).to_json(), 201
                else:
                    app.logger.info("TransactionService:user_transaction:user_id:{} No acccount found for this user!"
                                    .format(user_id))
                    return RestResponse(err="No acccount found for this user!").to_json(), 400
            else:
                app.logger.info(
                    "TransactionService:user_transaction:user_id:{} is not found".format(
                        user_id))
                return RestResponse(err="User Not Found").to_json(), 400

        except Exception as e:
            app.logger.info(
                "TransactionService:user_transaction:error:{}".format(str(e)))
            return RestResponse(err=f"Erroroccurred : {str(e)}").to_json(), 500