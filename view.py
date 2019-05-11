#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from app import app, db

from flask import (
    render_template, send_from_directory,
    redirect, url_for, request
)

from tools import load_file, remove_aid
from urllib.request import urlparse


def data_loader(flag):
    data = load_file(flag)
    mg, lg = (4, 4) if len(data) < 4 else (3, 2)
    return data, mg, lg


def call_cli(command):
    os.chdir('cli')
    os.system(command)
    os.chdir(os.path.dirname(os.getcwd()))


@app.route('/', methods=['GET', 'POST'])
def index():

    flag = request.args['flag'] if len(request.args) else 'o'
    update = 'python3 start.py'

    if flag == 'u':
        call_cli(update)
        flag = False
    elif flag == 'a':
        flag = True
    else:
        flag = False

    if request.method == 'POST':
        url = request.form['value']
        if url:
            parsed = urlparse(url)
            if parsed.netloc == 'animevost.org' and parsed.path.endswith('.html'):
                call_cli(f'{update} --link {url}')
                return redirect(url_for('anime_list'))

    data, mg, lg = data_loader(1)

    return render_template(
        'lolicon-page.html', data=data, mg=mg, lg=lg, flag=flag
    )


@app.route('/all')
def anime_list():
    data, mg, lg = data_loader(0)
    return render_template('lolicon-page.html', data=data, mg=mg, lg=lg)


@app.route('/remove/<aid>/')
def remove_link(aid):
    if remove_aid(aid):
        db.session.commit()
    return redirect(url_for('anime_list'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'magane_chikujouin.ico', mimetype='image/vnd.microsoft.icon'
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
