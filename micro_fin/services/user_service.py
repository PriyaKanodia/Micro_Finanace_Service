# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

from datetime import datetime
from micro_fin import app
from micro_fin.helper.rest_response import RestResponse
from micro_fin.models.user_model import UserModel
from micro_fin.services.transaction_service import TransactionService


class UserService:

    def user_signup(self, email, password, user_data):
        try:
            print(email, password, user_data)
            user = UserModel.find_by_email(email)
            if not user:
                msg  = self._validate_user_data(user_data)
                if msg['status']:
                    country_code = user_data['country_code']
                    mobile_number = user_data['mobile_number']
                    first_name = user_data['first_name']
                    last_name = user_data['last_name']
                    username = user_data['username']
                    gender = user_data['gender']
                    
                    if UserModel.find_by_mobile(country_code.strip(), mobile_number.strip()):
                        return RestResponse(err="Mobile Number already exists.").to_json(), 400
                    password = UserModel.generate_password_hash(password)
                    user = UserModel(email=email, password=password, username=username, first_name=first_name,
                                    last_name=last_name, country_code=country_code, mobile_number=mobile_number,
                                    gender=gender, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
                    user.temp_save()
                    
                    avoid_list = ['email', 'password', 'username', 'first_name', 'last_name', 'country_code',
                                  'mobile_number']
                    columns = [col.name for col in user.__table__.columns if col.name not in avoid_list]
                    for u_data in user_data:
                        if u_data in columns:
                            setattr(user, u_data, user_data[u_data])
                    user.created_by = user.updated_by = user.id
                    user.save()
                    
                    TransactionService().create_user_account(user.id)
                    
                    return RestResponse(
                        {'email': email, 'username': username}, message='User has been created successfully!',
                        status=1).to_json(), 201
                else:
                    return RestResponse(err="Invalid data: {}".format(msg['err'])).to_json(), 400
            else:
                return RestResponse(err="User already exists!").to_json(), 403
        except Exception as e:
            app.logger.error("UserService:user_signup:: {}".format(str(e)))
            return RestResponse(err='Something went wrong').to_json(), 500

    def _validate_user_data(self, data):
        if 'country_code' not in data or not data['country_code']:
            return {'err': "Country Code can not be blank", 'status': 0}
        if 'mobile_number' not in data or not data['mobile_number']:
            return {'err': "Mobile Number can not be blank", 'status': 0}
        if 'first_name' not in data or not data['first_name']:
            return {'err': "First Name cannot be blank", 'status': 0}
        if 'last_name' not in data or not data['last_name']:
            return {'err': "Last Name cannot be blank", 'status': 0}
        if 'username' not in data or not data['username']:
            return {'err': "Username cannot be blank", 'status': 0}
        if 'gender' not in data or not data['gender']:
            return {'err': "Gender cannot be blank", 'status': 0}
        return {'err': '', 'status': 1}

    def get_user(self, user_id):
        app.logger.info("fetch user: {}".format(user_id))
        try:
            user = UserModel.find_by_id(user_id)
            if user:
                user = user.to_json()
                return RestResponse(user, status=1).to_json(), 200
            else:
                return RestResponse(err='User not found!').to_json(), 400
        except Exception as e:
            app.logger.error("UserService:get_user:: {}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500

    def update_user(self, user_id, user_data):
        try:
            app.logger.info("UserService:update_user:data: {}".format(str(user_data)))
            user = UserModel.find_by_id(user_id)
            if user:
                is_update = False
                columns = [col.name for col in user.__table__.columns if col.name != 'password']
                for u_data in user_data:
                    if u_data == 'mobile_number' and user_data['mobile_number']:
                        if 'country_code' not in user_data or not user_data['country_code']:
                            return RestResponse(err="Country Code can not be blank").to_json(), 400
                        ex_user = UserModel.find_by_mobile(user_data['country_code'], user_data['mobile_number'])
                        if ex_user and ex_user.id != user.id:
                            return RestResponse(
                                err="This mobile number does not belong to you, so can't update it.").to_json(), 400
                    if u_data == 'email' and user_data['email']:
                        ex_user = UserModel.find_by_email(user_data['email'])
                        if ex_user and ex_user.id != user.id:
                            return RestResponse(
                                err="This Email Id does not belong to you, so can't update it.").to_json(), 400
                    if u_data in columns:
                        setattr(user, u_data, user_data[u_data])
                        is_update = True
                if is_update:
                    user.updated_by = user.id
                    user.updated_at = datetime.utcnow()
                    user.save()
                
                user = user.to_json()
                return RestResponse(user, message="User profile has been updated successfully", status=1).to_json(), 200
            else:
                return RestResponse(err="User is not found!").to_json(), 400
        except Exception as e:
            app.logger.error("UserService:update_user:: {}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500

    def delete_user(self, user_id):
        app.logger.info("UserService:delete_user: {}".format(user_id))
        try:
            user = UserModel.find_by_id(user_id)
            if user:
                user.delete()
                return RestResponse(message="User deleted successfully", status=1).to_json(), 200
            else:
                return RestResponse(err='User not found!').to_json(), 400
        except Exception as e:
            app.logger.error("UserService:delete_user:: {}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500