#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-築城院 真鍳'

import click
from os import getcwd, chdir
from bs4 import BeautifulSoup as bs
from json import dump, load
from config import JSWA, DBWA
from sqlite3 import connect
from os.path import exists, dirname
from urllib.request import urlopen
# from webbrowser import open_new_tab


class Animevost:

    def __init__(self, soup):
        self.soup = soup

    def get_name(self):
        return self.soup.find('h1').text.split('/')[-1].strip()

    def get_pic(self):
        return self.soup.find('img', 'imgRadius').get('src')

    def gen_data(self):
        return (self.get_name(), self.get_pic())


class CheckLinks:

    def __init__(self):
        # execute script in the top level
        chdir(dirname(getcwd()))
        self.pswa = [Animevost, None]

        if not exists(DBWA):
            self.first_run()

        self.conn = connect(DBWA)
        self.curr = self.conn.cursor()

    def first_run(self):
        with connect(DBWA) as conn:
            curr = conn.cursor()
            curr.execute("""CREATE TABLE lwa (iwa integer PRIMARY KEY,
                nwa text, lwa text, pwa text, cwa integer)""")

    def get_soup(self, url):
        return bs(urlopen(url), 'lxml')

    def get_updates(self):
        dbdata = self.curr.execute('SELECT * FROM lwa').fetchall()
        if dbdata:
            for i in dbdata:
                print(i)
            # with open(JSWA) as ftr:
            #     pass
            # jsdata = load(ftr)

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

    def parse_name(self):
        pass

    def to_json(self, data):
        with open(JSWA, 'w') as ftw:
            dump(data, ftw)

    def add_link(self, lwa):
        cwa = 0 if 'animevost' in lwa else None
        nwa, pwa = self.pswa[cwa](self.get_soup(lwa)).gen_data()
        self.curr.execute(
            """INSERT INTO lwa (nwa, lwa, pwa, cwa) VALUES (?, ?, ?, ?)""",
            (nwa, lwa, pwa, cwa)
        )
        self.conn.commit()

        if not exists(JSWA):
            self.to_json({})

        with open(JSWA, 'r') as ftr:
            ndwa = self.curr.execute(
                'SELECT iwa FROM lwa ORDER BY iwa DESC LIMIT 1'
            ).fetchone()[0]
            jdwa = load(ftr)
            jdwa = jdwa[ndwa] = self.parse_name(nwa)

            self.to_json(jdwa)


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
    # chl = CheckLinks()
    # chl.add_link()
    # 'http://animevost.org/tip/tv/2174-uchi-no-maid-ga-uzasugiru.html'
    # )
