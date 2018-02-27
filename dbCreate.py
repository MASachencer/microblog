#!/usr/bin/env python

from os.path import exists
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO


db.create_all()
if not exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
