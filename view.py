#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from app import app, db
from flask import render_template, send_from_directory, redirect, url_for
from tools import load_file, remove_aid


@app.route('/')
def index():
    data = load_file(1)
    mg, lg = (4, 4) if len(data) < 4 else (3, 2)
    return render_template('lolicon-page.html', data=data, mg=mg, lg=lg)


@app.route('/all')
def anime_list():
    data = load_file(0)
    mg, lg = (4, 4) if len(data) < 4 else (3, 2)
    return render_template('lolicon-page.html', data=data, mg=mg, lg=lg)


@app.route('/remove/<aid>/')
def remove_link(aid):
    # http://exploreflask.com/en/latest/views.html
    # https://stackoverflow.com/questions/27158573/how-to-delete-a-record-by-id-in-flask-sqlalchemy
    if remove_aid(aid):
        db.session.commit()
    return redirect(url_for('anime_list'))


@app.route('/favicon.ico')
def favicon():
    # https://69.media.tumblr.com/7906f0bd45159a3d04758b7acf498c88/tumblr_oqu66cTZD31wqeriwo9_400.jpg
    # https://www.online-convert.com/
    # http://flask.pocoo.org/docs/1.0/patterns/favicon/
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'magane_chikujouin.ico', mimetype='image/vnd.microsoft.icon'
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
