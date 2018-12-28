#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from app import app
from flask import render_template, send_from_directory
from tools import load_file


@app.route('/')
def index():
    data = load_file()
    mg, lg = (4, 6) if len(data) < 4 else (3, 2)
    return render_template('lolicon-page.html', data=load_file(), mg=mg, lg=lg)


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
