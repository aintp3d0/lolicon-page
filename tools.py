#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-天底 ガジ'

from json import load
from models import Anime
from cli.config import JSON_FILE


def load_file():

    with open(JSON_FILE) as ftr:
        data = load(ftr)
        data_to_show = []
        if data:
            database = Anime.query.all()
            for item in database:
                aid = str(item.aid)
                updated, time = data[aid][1]
                updated -= int(item.updates)
                data_to_show.append((item, (updated, time)))
            return data_to_show
