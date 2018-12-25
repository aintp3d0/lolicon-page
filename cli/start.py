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
from urllib.request import urlopen
# from webbrowser import open_new_tab


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
        self.inwa = ('http://animevost.org',)
        self.pswa = [Animevost, None]

        if not exists(DBWA):
            self.first_run()

        self.conn = connect(DBWA)
        self.curr = self.conn.cursor()
        self.spwa = partial(str.split, maxsplit=1)
        self.jnwa = partial(",".join)
        self.fawa = partial(re.findall, re.compile(r'\d+'))
        self.swwa = partial(str.startswith, self.inwa[inwa[0]])

    def first_run(self):
        with connect(DBWA) as conn:
            curr = conn.cursor()
            curr.execute("""CREATE TABLE lwa (iwa integer PRIMARY KEY,
                nwa text, lwa text, pwa text, cwa integer, uwa text)""")

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
        # ЦубаКума! / Uchi no Maid ga Uzasugiru! [1-12 из 12]

        # Девочки волшебницы: Специальная операция / Mahou Shoujo Tokushusen
        # Asuka [Анонс] [1 серия - 12 января]

        # Мастера меча онлайн (третий сезон) / Sword Art Online 3rd Season
        # [1-12 из 24+] [12 серия - 5 января]

        # В конечном счёте я стану твоей / Yagate Kimi ni Naru [1-12 из 13]

        # Как я и ожидал, моя школьная жизнь не задалась (второй сезон) /
        # OreGairu 2 [1-13 из 13] [OVA 1 из 1]

        RU, EN = nwa.split('/')
        ENWA = self.spwa(EN, '[')
        STWA, SPWA = self.spwa(ENWA[-1], ']')
        cpwa = self.fawa(STWA)
        lgwa = RU if not RUEN else ENWA[0]

        # anons
        if not cpwa:
            return (lgwa, 0)
        # completed series
        elif not SPWA or 'OVA' not in SPWA:
            return (lgwa, ",".join(cpwa[1:]))
        # series with ova
        elif SPWA and 'OVA' in SPWA:
            return (
                lgwa,
                f'{self.jnwa(cpwa[1:])}:{self.jnwa(self.fawa(SPWA))}'
            )
        else:
            for debug in (nwa, RU, EN, ENWA, STWA, SPWA, cpwa, lgwa):
                print(debug)

    def add_link(self, lwa):
        etwa = self.curr.execute(
            'SELECT uwa FROM lwa WHERE lwa = ?', (lwa,)
        ).fetchone()

        if etwa:
            exit(print('This url already exists'))

        # TODO: remove DRY, find better way to do it
        cwa = 0 if self.swwa(lwa) else None
        nwa, pwa = self.pswa[cwa](self.get_soup(lwa), 1).gen_data()
        pwa = pwa if self.swwa(pwa) else f'{self.inwa[0]}{pwa}'

        if not exists(JSWA):
            self.to_json({})

        jdwa = self.from_json()
        # https://stackoverflow.com/questions/29086705/sqlite-get-max-id-not-working
        ndwa = self.curr.execute(
            'SELECT iwa FROM lwa ORDER BY iwa DESC LIMIT 1'
        ).fetchone()

        nwa, uwa = self.parse_name(nwa)
        nwa = nwa.strip()
        jdwa[ndwa[0]+1 if ndwa else 1] = [nwa, uwa]

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
    # chl = CheckLinks()
    # chl.add_link()
    # 'http://animevost.org/tip/tv/2174-uchi-no-maid-ga-uzasugiru.html'
    # )
