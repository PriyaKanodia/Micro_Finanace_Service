# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

import os


#https://pypi.org/project/Flask-SQLAlchemy/
USERNAME = os.getenv("DB_USERNAME", "root")
PASSWORD = os.getenv("DB_PASSWORD", "root123")
SERVER = os.getenv("DB_HOST", "localhost")
DATABASE = os.getenv("DB_NAME", "micro_finance")
POOL_NAME = os.getenv("MYSQL_POOL_NAME", "mysql_pool")
POOL_SIZE = os.getenv("MYSQL_POOL_SIZE", 10)

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(USERNAME, PASSWORD, SERVER, DATABASE)
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False


#https://flask-jwt-extended.readthedocs.io/en/latest/options.html#configuration-options
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "7ILl{Xmm+c>v.OUD7V&#OPAl9<8RWn")
JWT_ACCESS_TOKEN_EXPIRES = 1*60*60
JWT_REFRESH_TOKEN_EXPIRES = 6*30*24*60*60
JWT_ERROR_MESSAGE_KEY = 'message'


# Redis
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_TTL = 1*60*60*60

