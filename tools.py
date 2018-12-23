#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-天底 ガジ'

from json import dump, load
from config import FILE
from models import Anime
from os.path import exists


if not exists(FILE):
    with open(FILE, 'w') as ftw:
        dump({}, ftw)


def load_file():

    with open(FILE) as ftr:
        data = load(ftr)
        if data:
            dwa = Anime.query.all()
            iwa = dwa.iwa
            data_to_show = []
            for item in iwa:
                if item in data.keys():
                    data_to_show.append((item, data[item]))
                    data.pop(item)

            return (each for each in data_to_show)
