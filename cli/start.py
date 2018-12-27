#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-築城院 真鍳'

import re
import click
from os import getcwd, chdir
from bs4 import BeautifulSoup as bs
from json import dump, load
from config import JSWA, DBWA, RUEN
from sqlite3 import connect
from os.path import exists, dirname
from functools import partial
from urllib.request import urlopen, urlparse, urlunparse
# from webbrowser import open_new_tab

"""
TODO:
    update variables name
    move updates.json and lolicon.db to this directory
"""


class Animevost:
    __slots__ = ('swa', 'fwa')

    def __init__(self, swa, fwa):
        self.swa = swa
        self.fwa = fwa

    def get_nwa(self):
        return self.swa.find('h1').text

    def get_pwa(self):
        return self.swa.find('img', 'imgRadius').get('src')

    def gen_data(self):
        return (self.get_nwa(), self.get_pwa()) if self.fwa else self.get_nwa()


class CheckLinks:

    def __init__(self):
        # execute script in the top level
        chdir(dirname(getcwd()))
        self.pswa = [Animevost, ]

        if not exists(DBWA):
            self.first_run()

        self.conn = connect(DBWA)
        self.curr = self.conn.cursor()
        self.spwa = partial(str.split, maxsplit=1)
        self.jnwa = partial(",".join)
        self.fawa = partial(re.findall, re.compile(r'\d+'))

    def first_run(self):
        with connect(DBWA) as conn:
            curr = conn.cursor()
            curr.execute("""CREATE TABLE lwa (iwa integer PRIMARY KEY,
                nwa text, lwa text, pwa text, cwa integer, uwa text)""")

    def get_parser(self, lwa):
        # https://stackoverflow.com/questions/15799696/library-to-build-urls-in-python
        clwa = list(urlparse(lwa))
        for cid, cname in enumerate(self.pswa):
            if cname.__name__.lower() in clwa[1]:
                clwa[2] = ''
                return (cid, self.pswa[cid], urlunparse(clwa))

    def to_json(self, data):
        with open(JSWA, 'w') as ftw:
            dump(data, ftw)

    def from_json(self):
        with open(JSWA, 'r') as ftr:
            return load(ftr)

    def get_soup(self, url):
        return bs(urlopen(url), 'lxml')

    def get_updates(self):
        """updates.json will save last updates,
        so web-app can show me updates eft when imma running app, not cli
        cli will overwrite it if i need new updates. (tak sebe english)
        """
        dbdata = self.curr.execute(
            'SELECT iwa, lwa, nwa, cwa, uwa FROM lwa'
        ).fetchall()
        if dbdata:
            jdwa = self.from_json()
            for (iwa, lwa, nwa, cwa) in dbdata:
                lswa = jdwa[iwa]
                print(lswa)

            # for item in data:
            #     pass
            # for anime_name in self.soup.find_all('h1'):
            #     name = self._helper("repl", anime_name)
            #     if check:
            #         self._helper("print", (link_item, name))
            #         if link_name != name:
            #             self._helper('dict', (link_item, link_name, name))
            #     else:
            #         self._print_shorter(name, True)
            #         return name

    def parse_name(self, nwa):
        """Return name in one of language and number of series
        """
        RU, EN = nwa.split('/')
        ENWA = self.spwa(EN, '[')
        STWA, SPWA = self.spwa(ENWA[-1], ']')
        cpwa = self.fawa(STWA)
        lgwa = RU if not RUEN else ENWA[0]

        if not cpwa:
            return (lgwa, 0)
        elif not SPWA or 'OVA' not in SPWA:
            return (lgwa, ",".join(cpwa[1:]))
        elif SPWA and 'OVA' in SPWA:
            return (
                lgwa,
                f'{self.jnwa(cpwa[1:])}:{self.jnwa(self.fawa(SPWA))}'
            )

    def add_link(self, lwa):
        """Parsing web-page, save to json file and the database
        """
        etwa = self.curr.execute(
            'SELECT uwa FROM lwa WHERE lwa = ?', (lwa,)
        ).fetchone()

        if etwa:
            exit(print('This url already exists'))

        cwa, iwa, swa = self.get_parser(lwa)
        nwa, pwa = self.pswa[cwa](self.get_soup(lwa), 1).gen_data()
        pwa = pwa if pwa.startswith(swa) else f'{swa}{pwa}'
        hashed_url = hash(lwa)

        if not exists(JSWA):
            self.to_json({})

        jdwa = self.from_json()

        # https://stackoverflow.com/questions/4288089/reuse-identity-value-after-deleting-rows
        for data_id, (*_, exist_hash) in jdwa.items():
            if exist_hash == hashed_url:
                jdwa.pop(data_id)

        # https://stackoverflow.com/questions/29086705/sqlite-get-max-id-not-working
        ndwa = self.curr.execute(
            'SELECT iwa FROM lwa ORDER BY iwa DESC LIMIT 1'
        ).fetchone()

        nwa, uwa = self.parse_name(nwa)
        nwa = nwa.strip()
        jdwa[ndwa[0]+1 if ndwa else 1] = [nwa, uwa, hashed_url]

        self.to_json(jdwa)

        self.curr.execute(
            """INSERT INTO lwa (nwa, lwa, pwa, cwa, uwa) VALUES
            (?, ?, ?, ?, ?)""", (nwa, lwa, pwa, cwa, uwa)
        )
        self.conn.commit()


@click.command()
@click.option(
    '--link', default='lwa',
    help='Parsing url and storing it in the database for checking later'
)
def main(link):
    """Middle Function between *add_link* and *get_updates*
    """
    # https://www.youtube.com/watch?v=kNke39OZ2k0
    chl = CheckLinks()
    if link != 'lwa':
        chl.add_link(link)
    else:
        chl.get_updates()


if __name__ == '__main__':
    main()
