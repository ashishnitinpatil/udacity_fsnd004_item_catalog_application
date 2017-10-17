#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime
from flask_login.mixins import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import backref
from sqlalchemy import MetaData


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))


class User(UserMixin, db.Model):
    """Model for storing User details"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    avatar = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Category(db.Model):
    """Model for category of items in the catalog"""
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return "<Category(name='%s')>" % self.name

    def __str__(self):
        return self.name

    def serialize(self, include_items=True):
        serialized_category = {
            'id': self.id,
            'name': self.name
        }
        if include_items:
            serialized_category['items'] = [i.serialize() for i in self.items]
        return serialized_category


class Item(db.Model):
    """Model for items in the catalog"""
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(256))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category, lazy=False,
                               backref=backref('items', cascade="all,delete"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return "<Item(name='%s', category='%s')>" % (self.name, self.category)

    def __str__(self):
        return self.name

    def serialize(self, include_category=False):
        serialized_item = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        if include_category:
            serialized_item['category'] = self.category.serialize(False)
        return serialized_item
