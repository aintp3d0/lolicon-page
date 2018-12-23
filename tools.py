#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-天底 ガジ'

from json import load
from models import Anime
from cli.config import JSWA


def load_file():

    with open(JSWA) as ftr:
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
