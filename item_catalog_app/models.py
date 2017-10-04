#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import datetime
from flask_login.mixins import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Model for storing User details"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    avatar = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
