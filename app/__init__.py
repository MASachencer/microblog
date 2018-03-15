from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'login'
oid = OpenID(app, path.join(basedir, 'tmp'))

from app import views, models
