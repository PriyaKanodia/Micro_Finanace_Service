# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

from flask_restful import Resource, reqparse
from micro_fin.services.session_service import SessionService
from micro_fin.helper.rest_response import RestResponse
from micro_fin import app
from micro_fin.decorators.authenticated import authenticated
import pdb


class LoginSession(Resource):
    
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Name can not be blank', required=True)
            parser.add_argument('password', type=str, help='Password can not be blank', required=True)
            args = parser.parse_args()
            app.logger.debug("LoginSession::post::params::{}".format(args))
            
            return SessionService().user_login(args['email'], args['password'])

        except Exception as e:
            app.logger.error("LoginSession::post::error:{}".format(e))
            return RestResponse(err='Something went wrong').to_json(), 500

class LogoutSession(Resource):
    
    @authenticated()
    def post(self, current_user_id, token):
        try:
            print("######", current_user_id, token)
            app.logger.debug("LogoutSession::post::{}".format(current_user_id))
            
            return SessionService().user_logout(current_user_id, token)

        except Exception as e:
            app.logger.error("LogoutSession::post::error:{}".format(e))
            return RestResponse(err='Something went wrong').to_json(), 500
