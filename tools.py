#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-天底 ガジ'

from json import load
from models import Anime
from cli.config import JSWA


def load_file():

    with open(JSWA) as ftr:
        data = load(ftr)
        data_to_show = []
        if data:
            dwa = Anime.query.all()
            for item in dwa:
                iwa = str(item.iwa)
                if str(iwa) in data.keys():
                    data_to_show.append((item, data[iwa]))
                    data.pop(iwa)
            return (each for each in data_to_show)
