# -*- coding: utf-8 -*-

from os import path, environ

DEBUG = False
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

basicDir = path.abspath(path.dirname(__file__))
baseDir = path.join(basicDir, 'base')
SQLALCHEMY_DATABASE_URI = f"sqlite:///{path.join(baseDir, 'app.sqlite')}"
SQLALCHEMY_MIGRATE_REPO = path.join(basicDir, 'migrations')
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = '127.0.0.1'
MAIL_PORT = 25
MAIL_USE_SSL = False
MAIL_USE_TLS = False
MAIL_USERNAME = environ.get('MAIL_USERNAME')
MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
ADMINS = ['admin@email.com']

POSTS_PER_PAGE = 3

WHOOSH_BASE = path.join(baseDir, 'search.sqlite')
MAX_SEARCH_RESULTS = 50

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]
