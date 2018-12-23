#!/usr/bin/env python3
# coding:utf-8

from app import db


class Anime(db.Model):
    __tablename__ = 'anime'

    iwa = db.Column(db.Integer, primary_key=True)
    nwa = db.Column(db.String(50)
    lwa = db.Column(db.String(100))
    pwa = db.Column(db.String(100))
    cwa = db.Column(db.Integer, nullable=False)
