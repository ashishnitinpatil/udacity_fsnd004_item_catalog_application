#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json


# Load secrets from json and overwrite the settings
with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

# oauthlib - oauth2 must utilize https workaround
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class Config(object):
    """Base configuration."""

    DEBUG = secrets['DEBUG'] or True
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    APP_NAME = 'Item Catalog Application'
    SECRET_KEY = secrets['SECRET_KEY'] or 'somethingsecret'
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_DATABASE_URI = secrets['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Google Auth related
    CLIENT_ID = '158639267879-1k5j5uhbk32cgv7cc26412kasd79qo3i.apps.googleusercontent.com'
    CLIENT_SECRET = secrets['GOOGLE_CLIENT_SECRET'] or 'top-secret'
    REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']
