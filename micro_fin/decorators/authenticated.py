# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from micro_fin.helper.redis_base import RedisBase
from micro_fin.helper.rest_response import RestResponse
from micro_fin.models.user_model import UserModel
from flask import request

token_allow_list = ['/api/session/logout']

def authenticated(permission=None):
    def authorized(fn):
        @jwt_required()
        @wraps(fn)
        def _wrap(*args, **kwargs):
            auth_token = request.headers.get('Authorization')
            access_token = auth_token.split(" ")[1]
            token = RedisBase.get(access_token)
            if not token:
                return RestResponse(err='Token expired!!').to_json(), 401
            current_user_email = get_jwt_identity()
            if not current_user_email:
                return RestResponse(err='Unauthorized User!!').to_json(), 401
            print("#####", current_user_email)
            user = UserModel.find_by_email(current_user_email)
            if user:
                if not user.active:
                    return RestResponse(err='User profile is inactive!').to_json(), 401
            else:
                return RestResponse(err='User is not found!').to_json(), 400
            base_url = request.url
            is_send_token = False
            for token_url in token_allow_list:
                if token_url in base_url:
                    is_send_token = True
                    break
            if is_send_token:
                  return fn(current_user_id=user.id, token=access_token, *args, **kwargs)  
            return fn(current_user_id=user.id, *args, **kwargs)

        return _wrap

    return authorized
