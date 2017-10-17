#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask_login import login_required, current_user
from item_catalog_app.models import db, User, Category, Item
from flask import Blueprint, url_for, render_template, jsonify
from flask import request, flash, redirect, abort

routes = Blueprint('catalog', __name__)


def get_or_abort(Model, object_id, exception=404):
    """Helper class to fetch a resource, and if not found, raise exception"""
    object = Model.query.get(object_id)
    if not object:
        abort(exception)
    else:
        return object


@routes.route('/')
def index():
    latest_items = Item.query.order_by(Item.created_at.desc()).limit(10).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template('index.html', **locals())


# Category routes
@routes.route('/category/new/', methods=['GET', 'POST'])
@login_required
def new_category():
    if request.method == 'POST':
        category = Category(name=request.form['name'],
                            created_by=current_user)
        db.session.add(category)
        db.session.commit()
        flash('New Category %s Successfully Created' % category.name)
        return redirect(url_for('catalog.index'))
    else:
        return render_template('category_form.html')


@routes.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        flash('Wrong category_id given, do you want to create one?')
        return redirect(url_for('catalog.new_category'))
    if not category.has_perm(current_user, 'edit'):
        flash('Sorry, but only the creater of the category can edit it!')
        return redirect(url_for('catalog.category_display',
                                category_id=category.id))
    if request.method == 'POST':
        if request.form['name']:
            category.name = request.form['name']
            db.session.add(category)
            db.session.commit()
            flash('Category Successfully Edited %s' % category.name)
            return redirect(url_for('catalog.index'))
    else:
        return render_template('category_form.html', **locals())


@routes.route('/category/JSON/')
def categories_json():
    categories = Category.query.all()
    return jsonify([c.serialize(False) for c in categories])


@routes.route('/category/<int:category_id>/')
def category_display(category_id):
    category = get_or_abort(Category, category_id)
    return render_template('category_display.html', **locals())


@routes.route('/category/<int:category_id>/JSON/')
def category_json(category_id):
    category = get_or_abort(Category, category_id)
    return jsonify(category.serialize())


# Item routes
@routes.route('/item/new/', methods=['GET', 'POST'])
@routes.route('/item/new/<int:category_id>/', methods=['GET', 'POST'])
@login_required
def new_item(category_id=None):
    if request.method == 'POST':
        item = Item(category_id=request.form['category'],
                    name=request.form['name'],
                    description=request.form['description'],
                    created_by=current_user)
        db.session.add(item)
        db.session.commit()
        flash('New Item %s Successfully Created' % item.name)
        return redirect(url_for('catalog.index'))
    else:
        categories = Category.query.all()
        return render_template('item_form.html', **locals())


@routes.route('/item/<int:item_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        flash('Wrong item_id given, do you want to create one?')
        return redirect(url_for('catalog.new_item'))
    if not item.has_perm(current_user, 'edit'):
        flash('Sorry, but only the creater of the item can edit it!')
        return redirect(url_for('catalog.item_display', item_id=item.id))
    if request.method == 'POST':
        item.name = request.form['name']
        item.category_id = request.form['category']
        item.description = request.form['description']
        db.session.add(item)
        db.session.commit()
        flash('Item Successfully Edited %s' % item.name)
        return redirect(url_for('catalog.index'))
    else:
        categories = Category.query.all()
        return render_template('item_form.html', **locals())


@routes.route('/item/<int:item_id>/')
def item_display(item_id):
    item = get_or_abort(Item, item_id)
    return render_template('item_display.html', **locals())


@routes.route('/item/<int:item_id>/JSON/')
def item_json(item_id):
    item = get_or_abort(Item, item_id)
    return jsonify(item.serialize(True))


def delete_object(Model, object_id):
    """Helper function to handle object deletion given it's type & id"""
    object = get_or_abort(Model, object_id)
    if not object.has_perm(current_user, 'edit'):
        flash('Sorry, but you can only delete objects that you have created!')
        return redirect(url_for('catalog.index'))
    if request.method == 'POST':
        db.session.delete(object)
        db.session.commit()
        flash('{} {} Successfully Deleted'.format(Model.__name__, object.name))
        return redirect(url_for('catalog.index'))
    else:
        return render_template('delete.html', object=object)


# Deletion routes
@routes.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    return delete_object(Category, category_id)


@routes.route('/item/<int:item_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    return delete_object(Item, item_id)
