#!/usr/bin/env python3
# coding:utf-8

import os


JSWA = 'updates.json'
DBWA = 'lolicon.db'
RUEN = 1


class Configuration:
    DEBUG = True
    SECRET_KEY = 'LOLI_RULES'
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), DBWA)
    # POSTGRES = { 'user': '', 'pw': '', 'db': '', 'host': '', 'port': '', }
    # mysql+drayver://user:pass@server/name_of_databese
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1@localhost/test1'
    db_uri = 'sqlite:///{}'.format(db_path)
    # SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
    #     %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
