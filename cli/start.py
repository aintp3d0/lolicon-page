#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-築城院 真鍳'

import re
import click
from bs4 import BeautifulSoup as bs
from json import dump, load
from config import JSON_FILE, DB_FILE, RU_EN
from sqlite3 import connect
from os.path import exists
from datetime import datetime
from functools import partial
from urllib.request import urlopen, urlparse, urlunparse
from multiprocessing import Pool


class Animevost:
    __slots__ = ('soup', 'flag')

    def __init__(self, soup, flag):
        self.soup = soup
        self.flag = flag

    def get_nwa(self):
        return self.soup.find('h1').text

    def get_pwa(self):
        return self.soup.find('img', 'imgRadius').get('src')

    def gen_data(self):
        return (
            self.get_nwa(), self.get_pwa()
        ) if self.flag else self.get_nwa()


class CheckLinks:

    def __init__(self):
        # execute script in the top level
        self.parsers = [Animevost, ]

        if not exists(DB_FILE):
            self.first_run()

        self.conn = connect(DB_FILE)
        self.curr = self.conn.cursor()
        self.one_split = partial(str.split, maxsplit=1)
        self.comma_join = partial(",".join)
        self.find_digits = partial(re.findall, re.compile(r'\d+'))

        # https://github.com/hhiki/isshuukan_friends/blob/master/Kaori_.py
        self.days = [
            '月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日'
        ][datetime.weekday(datetime.now())]
        self.time = datetime.today().strftime(f"{self.days}%Y年%m月%d日")

        self.parser = None
        self.database = None
        self.jsondata = None
        self.links_to_parse = None

    def first_run(self):
        with connect(DB_FILE) as conn:
            curr = conn.cursor()
            curr.execute("""CREATE TABLE
            anime (aid integer PRIMARY KEY,
            name text, link text, pic text, parser integer, updates text)""")

    def get_parser(self, lwa):
        # https://stackoverflow.com/questions/15799696/library-to-build-urls-in-python
        clwa = list(urlparse(lwa))
        for cid, cname in enumerate(self.parsers):
            if cname.__name__.lower() in clwa[1]:
                clwa[2] = ''
                return (cid, self.parsers[cid], urlunparse(clwa))

    def to_json(self, data):
        with open(JSON_FILE, 'w', encoding='utf-8') as ftw:
            dump(data, ftw)

    def from_json(self):
        with open(JSON_FILE, 'r') as ftr:
            return load(ftr)

    def get_soup(self, url):
        return bs(urlopen(url), 'lxml')

    def get_updates(self, db_and_json_data):
        """updates.json will save last updates,
        so web-app can show me updates EFT when imma running app, not cli.
        cli will overwrite it if i need new updates.
        """
        data_id, link, parser, series = db_and_json_data
        if not self.parser or self.parser != parser:
            self.parser = parser

        anime_name = self.parsers[
            self.parser
        ](self.get_soup(link), 0).gen_data()

        updated = self.parse_name(anime_name, 0)
        new_updates = 0
        for last, new in zip(*map(lambda x: x.split(','), (series, updated))):
            if last != new:
                new_updates += (int(new) - int(last))

        if new_updates:
            last_updated_to = self.jsondata[data_id][1][0]

            if last_updated_to != 0:
                self.curr.execute(
                    """UPDATE anime SET updates = ? WHERE aid = ?""",
                    (last_updated_to, data_id)
                )

            self.jsondata[data_id][1] = (new_updates, self.time)

    def with_multiprocessing(self):
        dbdata = self.curr.execute(
            'SELECT aid, link, parser FROM anime'
        ).fetchall()

        if dbdata:
            self.jsondata = self.from_json()

            pool = Pool()
            pool.map(
                self.get_updates,
                (
                    (
                        data_id, link, parser, self.jsondata[data_id][0]
                    ) for data_id, link, parser in dbdata
                )
            )
            pool.close()
            pool.join()

    def parse_name(self, anime_name_from_h1, flag):
        """Return name in one of language and number of series
        """
        RU, EN = anime_name_from_h1.split('/')

        name_series_ova = self.one_split(EN, '[')
        series, ova = self.one_split(name_series_ova[-1], ']')
        series_list = self.find_digits(series)

        ova = self.find_digits(ova)
        anime_name = RU if not RU_EN else name_series_ova[0]
        series_and_ova = ["0,0", "0,0"]

        series_and_ova[0] = self.comma_join(
            series_list[1:] if len(series_list) > 2 else series_list
        )

        series_and_ova[1] = self.comma_join(
            ova if ova else ["0", "0"]
        )

        series_and_ova = self.comma_join(series_and_ova)
        return (anime_name, series_and_ova) if flag else series_and_ova

    def add_link(self, link):
        """Parsing web-page, save to json file and the database
        """
        etwa = self.curr.execute(
            'SELECT updates FROM anime WHERE link = ?', (link,)
        ).fetchone()

        if etwa:
            # continue for *add_loop
            print('INFO> This url already exists')
            return None

        parser, aid, base_url = self.get_parser(link)
        name, pic = self.parsers[parser](self.get_soup(link), 1).gen_data()
        pic = pic if pic.startswith(base_url) else f'{base_url}{pic}'
        hashed_url = hash(link)

        if not exists(JSON_FILE):
            self.to_json({})

        json_data = self.from_json()

        # https://stackoverflow.com/questions/4288089/reuse-identity-value-after-deleting-rows
        for data_id, (*_, exist_hash) in json_data.items():
            if exist_hash == hashed_url:
                json_data.pop(data_id)

        # https://stackoverflow.com/questions/29086705/sqlite-get-max-id-not-working
        max_data_id = self.curr.execute(
            'SELECT aid FROM anime ORDER BY aid DESC LIMIT 1'
        ).fetchone()

        name, series = self.parse_name(name, 1)
        name = name.strip()
        updates = 0

        json_data[
            max_data_id[0]+1 if max_data_id else 1
        ] = [series, (updates, self.time), hashed_url]

        self.to_json(json_data)

        self.curr.execute(
            """INSERT INTO anime (name, link, pic, parser, updates) VALUES
            (?, ?, ?, ?, ?)""", (name, link, pic, parser, updates)
        )
        self.conn.commit()


@click.command()
@click.option(
    '--link', default='link',
    help='Parsing url and storing it in the database for checking later'
)
@click.option(
    '--add_loop', default='0',
    help='Use it if you have more than 1 urls to add, [ stop ] to break'
)
def main(link, add_loop):
    """Middle Function between *add_link* and *get_updates*
    """
    # https://www.youtube.com/watch?v=kNke39OZ2k0
    chl = CheckLinks()
    if link != 'link':
        chl.add_link(link)
    else:
        chl.with_multiprocessing()
    # for test (just add data faster), adding new data to json file
    if add_loop != '0':
        while True:
            url = input('LINK> ')

            if not url or url == 'stop':
                break

            chl.add_link(url)


if __name__ == '__main__':
    main()
