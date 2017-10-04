#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from flask import Blueprint, url_for, redirect, \
    render_template, session, request
from requests.exceptions import HTTPError
from requests_oauthlib import OAuth2Session
from item_catalog_app import settings, models
from flask_login import login_required, current_user, login_user, logout_user


routes = Blueprint('users', __name__)


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(settings.Config.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            settings.Config.CLIENT_ID,
            redirect_uri=settings.Config.REDIRECT_URI,
            state=state
        )
    else:
        return OAuth2Session(
            settings.Config.CLIENT_ID,
            redirect_uri=settings.Config.REDIRECT_URI,
            scope=settings.Config.SCOPE
        )


@routes.route('/')
@login_required
def index():
    return render_template('index.html')


@routes.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        settings.Config.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)


@routes.route('/oauth2callback')
def callback():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        google = get_google_auth(state=session.get('oauth_state', None))
        try:
            token = google.fetch_token(
                settings.Config.TOKEN_URI,
                client_secret=settings.Config.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(settings.Config.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = models.User.query.filter_by(email=email).first()
            if user is None:
                user = models.User()
                user.email = email
            user.name = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            models.db.session.add(user)
            models.db.session.commit()
            login_user(user)
            return redirect(url_for('users.index'))
        return 'Could not fetch your information.'


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.index'))
