#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-天底 ガジ'

from json import load
from models import Anime
from os.path import exists
from cli.config import JSON_FILE, REM_FILE


def from_json():
    if exists(JSON_FILE):
        with open(JSON_FILE) as ftr:
            return load(ftr)
    else:
        print('INFO> Please add link first')
        exit(0)


def load_file(flag):
    data = from_json()
    data_to_show = []
    if data:
        database = Anime.query.all()
        for item in database:
            aid = str(item.aid)
            updated, time = data[aid][1]
            updated -= int(item.updates)
            if flag:
                if updated:
                    data_to_show.append((item, (updated, time)))
            else:
                data_to_show.append((item, (updated, time)))
        return data_to_show


def remove_aid(aid):
    if from_json().get(aid, None):
        # https://stackoverflow.com/questions/27278755/unsupported-operation-not-writeable-python
        with open(REM_FILE, 'a') as fta:
            fta.write('\n' + aid)
        Anime.query.filter_by(aid=int(aid)).delete()
        return 1
    return 0
