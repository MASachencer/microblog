# -*- coding: utf-8 -*-

from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Chencer'}
    posts = [{'author': {'username': 'Matt'},
              'body': 'Beautiful day in Portland!'},
             {'author': {'username': 'Mira'},
              'body': 'The Avengers movie was so cool!'}]
    return render_template('index.html', title='Home', user=user, posts=posts)
