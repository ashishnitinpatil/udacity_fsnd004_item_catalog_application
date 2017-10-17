#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_migrate import Migrate
from item_catalog_app.settings import Config
from item_catalog_app.models import db, login_manager
from item_catalog_app.views.users import routes as user_routes
from item_catalog_app.views.catalog import routes as catalog_routes


def create_app():
    # instantiate app and load settings
    app = Flask(__name__)
    app.config.from_object(Config)
    initialize_apps(app)
    register_blueprints(app)
    return app


def initialize_apps(app):
    # https://flask-login.readthedocs.io/en/latest/#configuring-your-application
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    db.init_app(app)
    Migrate(app, db)


def register_blueprints(app):
    app.register_blueprint(user_routes)
    app.register_blueprint(catalog_routes)
