# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

from flask_restful import Resource, reqparse
from micro_fin import app
from micro_fin.decorators.authenticated import authenticated
from micro_fin.services.user_service import UserService
from micro_fin.helper.rest_response import RestResponse



class Users(Resource):
    
    #Sign Up
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Name can not be blank', required=True)
            parser.add_argument('password', type=str, help='Password can not be blank', required=True)
            parser.add_argument('user_data', type=dict, help='User data cannot be blank', required=True)
            args = parser.parse_args()
            
            app.logger.debug("Users::post::payload:{}".format(args))

            return UserService().user_signup(args['email'], args['password'], args['user_data'])
        
        except Exception as e:
            app.logger.error("Users::post::error:{}".format(e))
            return RestResponse(err='Something went wrong! {}'.format(str(e))).to_json(), 500

    @authenticated()
    def get(self, current_user_id):
        try:
            app.logger.info("Users::get::current_user_id:{}".format(current_user_id))

            app.logger.info("Users::put::user_id:{}".format(current_user_id))
            return UserService().get_user(current_user_id)
            
        except Exception as e:
            app.logger.error("Users::get::error:{}".format(str(e)))
            return RestResponse(err='Something went wrong! {}'.format(str(e))).to_json(), 500

    @authenticated()
    def put(self, current_user_id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_data', type=dict, help='User data can not be blank', required=True)
            args = parser.parse_args()

            app.logger.info("Users::put::user_id:{}".format(current_user_id))
            return UserService().update_user(current_user_id, args['user_data'])

        except Exception as e:
            app.logger.error("Users:put::error {}".format(e))
            return RestResponse(err='Something went wrong! {}'.format(str(e))).to_json(), 500

    @authenticated()
    def delete(self, current_user_id):
        try:
            app.logger.info("Users::delete:current_user_id:{}".format(current_user_id))
            return UserService().delete_user(current_user_id)
        except Exception as e:
            app.logger.error("Users::delete:error: {}".format(e))
            return RestResponse(err='Something went wrong! {}'.format(str(e))).to_json(), 500

