# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

from flask import Flask, make_response, json
from flask_restful import Api
from flask_jwt_extended import JWTManager
import redis
from flask_sqlalchemy import SQLAlchemy
from geopy.geocoders import Nominatim
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)


app.config.from_object('config')
api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

redis_store = redis.Redis(host=app.config['REDIS_HOST'], port=int(app.config['REDIS_PORT']),
                          password=app.config['REDIS_PASSWORD'], db=int(app.config['REDIS_DB']), decode_responses=True)
# print("************", redis_store)

cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})

# mysql_conn = mysql.connector.connect(
#         host=app.config['SERVER'],
#         user=app.config['USERNAME'],
#         passwd=app.config['PASSWORD'],
#         database=app.config['DATABASE'])

# def init_db():
#     mysql_conn = mysql.connector.connect(
#         host=app.config['SERVER'],
#         user=app.config['USERNAME'],
#         passwd=app.config['PASSWORD'],
#         database=app.config['DATABASE'])
#     return mysql_conn


# def get_cursor(mysql_conn):
#     try:
#         mysql_conn.ping(reconnect=True, attempts=3, delay=5)
#     except mysql.connector.Error as err:
#         # reconnect your cursor
#         mysql_conn = init_db()
#     return mysql_conn


# mysql_conn = get_cursor(mysql_conn)  # mysql cursor

# geoLoc = Nominatim(user_agent="GetLoc")  # To get the lat an long of the location

import micro_fin.routes.routes

@api.representation('application/json')
def output_json(data, code, headers=None):
    if code == 400 or code == 401:
        data['status'] = 0
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp


@jwt.expired_token_loader
def jwt_expired_token_loader(jwt_header, jwt_payload):
    token_type = jwt_header['typ']
    resp = make_response(json.dumps(
        {'status': 0, app.config['JWT_ERROR_MESSAGE_KEY']: 'The {} token has expired'.format(token_type)}), 401)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@jwt.unauthorized_loader
def jwt_unauthorized_loader(t):
    resp = make_response(json.dumps({'status': 0, app.config['JWT_ERROR_MESSAGE_KEY']: t}), 401)
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.before_first_request
def crate_tables():
    # cursor = mysql_conn.cursor()
    # db_exists_query = "Select schema_name From information_schema.schemata Where schema_name = 'micro_finance'"
    # cursor.execute(db_exists_query)
    # exists = cursor.fetchone()
    # if not exists:
    #     create_db = "Create micro_finance"
    #     cursor.execute(create_db)
    
    from micro_fin.models.user_model import UserModel
    db.create_all()