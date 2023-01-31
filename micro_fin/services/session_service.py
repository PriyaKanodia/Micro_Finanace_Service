# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

from micro_fin import app
from flask_jwt_extended import create_access_token
from micro_fin.helper.redis_base import RedisBase
from micro_fin.helper.rest_response import RestResponse
from micro_fin.models.user_model import UserModel



class SessionService:

    def user_login(self, email, password):
        app.logger.info("SessionService:user_login: User login with email {}".format(email))
        try:
            user = UserModel.find_by_email(email)
            if user:
                print("paaaaas", email, password)
                if not user.password:
                    return RestResponse(err="Password cannot be blank!").to_json(), 400
                if UserModel.verify_hash(password, user.password):
                    token = create_access_token(identity=str(email), expires_delta=False)
                    RedisBase.set(token, str(email))
                    user_data = user.to_json()
                    user_data['aacess_token'] = token
                    return RestResponse(user_data, message='You are logged in successfully', status=1).to_json(), 200
                else:
                    return RestResponse(err="Invalid Password!").to_json(), 400
            else:
                return RestResponse(err="User does not exist").to_json(), 400
        except Exception as e:
            print("llllll")
            app.logger.error("SessionService:user_login:error:{}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500

    def user_logout(self, user_id, token):
        app.logger.info("SessionService:user_logout: {}".format(user_id))
        try:
            user = UserModel.find_by_id(user_id)
            if user:
                access_token = RedisBase.get(token)
                if access_token:
                    RedisBase.remove(token)
                    return RestResponse(message='You are logged out successfully', status=1).to_json(), 200
                else:
                    return RestResponse(err="Invalid session!").to_json(), 400
            else:
                return RestResponse(err="User does not exist").to_json(), 400
        except Exception as e:
            app.logger.error("SessionService:user_logout:error:{}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500
