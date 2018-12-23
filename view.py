#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template
from tools import load_file


@app.route('/')
def index():
    return render_template('lolicon-page.html'), {'data': load_file()}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
