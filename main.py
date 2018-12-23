#!/usr/bin/env python3
# coding:utf-8

from app import app, db
from view import *
from models import Anime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(app)
admin.add_view(ModelView(Anime, db.session))


if __name__ == "__main__":
    app.run()
