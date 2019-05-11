#!/usr/bin/env python3
# coding:utf-8

import os


JSON_FILE = os.path.join(os.path.dirname(__file__), 'updates.json')
REM_FILE = os.path.join(os.path.dirname(__file__), 'removed_aid.txt')
DB_FILE = 'lolicon.db'
RU_EN = 1


class Configuration:
    HOST = '0.0.0.0'
    DEBUG = True
    SECRET_KEY = 'LOLI_RULES'
    db_path = os.path.join(os.path.dirname(__file__), DB_FILE)
    # POSTGRES = { 'user': '', 'pw': '', 'db': '', 'host': '', 'port': '', }
    # mysql+drayver://user:pass@server/name_of_databese
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1@localhost/test1'
    db_uri = 'sqlite:///{}'.format(db_path)
    # SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
    #     %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
