#!/usr/bin/env python3
# coding:utf-8

from app import db


class Anime(db.Model):
    __tablename__ = 'anime'

    aid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    link = db.Column(db.String(100))
    pic = db.Column(db.String(100))
    updates = db.Column(db.Integer, nullable=False)
