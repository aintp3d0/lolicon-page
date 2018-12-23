#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-築城院 真鍳'

from bs4 import BeautifulSoup as bs
from sqlite3 import connect
from os.path import exists
from urllib.request import urlopen
# from webbrowser import open_new_tab


class CheckLinks:

    def __init__(self):
        pass

    def parse_animevost(self):
        if exists('kkkupdates.json')
        nwa =
        for anime_name in self.soup.find_all('h1'):
            name = self._helper("repl", anime_name)
            if check:
                self._helper("print", (link_item, name))
                if link_name != name:
                    self._helper('dict', (link_item, link_name, name))
            else:
                self._print_shorter(name, True)
                return name

    def _add_link(self):
        name = None
        while True:
            _link = input('GIVE ME LINK: ')
            if _link:
                self.soup = get_soup(_link)
                if 'anidub.com' in _link:
                    name = self._anidub(False, None, None)
                elif 'anilibria.tv' in _link:
                    name = self._anilibria(False, None, None)
                else:
                    name = self._other_links(False, None, None)
                if name:
                    self.cur.execute("""INSERT INTO links VALUES (?, ?)""", (_link, name))
                    self.db.commit()
                    print(f'+ {_link} : ADDED!')
            else:
                break

    def _check_link(self):
        data = self.cur.execute("""SELECT * FROM links""")
        for link_item, link_name in data:
            self.soup = get_soup(link_item)
            if 'anidub.com' in str(link_item):
                self._anidub(True, link_item, link_name)
            elif 'anilibria.tv' in str(link_item):
                self._anilibria(True, link_item, link_name)
            else:
                self._other_links(True, link_item, link_name)
        self._diffs()

    def _give_me_links_from_tables(self):
        tab = self.cur.execute('''SELECT items FROM links''')
        fet = tab.fetchall()
        if fet:
            result = {}
            for idx, itm in enumerate(fet):
                print(f'{idx}: {itm[0]}')
                result[f'{idx}'] = itm[0]
            return result
        print('\n                NO LINKES YET')

    def _delete_link(self):
        """
        0: https://online.anidub.com/ ... .html
        1: https://www.anilibria.tv/ ... .html
        2: http://animevost.org/ ... .html
        """
        try:
            while True:
                dct = self._give_me_links_from_tables()
                li = input('\n?: ')
                if li in dct.keys():
                    data = self.cur.execute(f'''SELECT * FROM links WHERE items="{dct[li]}"''')
                    print('> FOUND LINK AT: ', data)
                    de = input('                _DELETE IT [y/n]:_ ')
                    if de.lower() == 'y':
                        self.cur.execute(f'''DELETE FROM links WHERE items="{dct[li]}"''')
                        self.db.commit()
                        print('                _DONE!')
                else: break
        except Exception: pass

    def _update_link(self, _item, _name):
        self.cur.execute(f'''UPDATE links SET name = "{_name}" WHERE items = "{_item}"''')
        self.db.commit()

    def _diffs(self):
        if self._new:
            print('\n                DIFFERENCES IN THIS LINKS:')
            for link, (last, new) in self._new.items():
                print('+-----------------------------------------------+')
                print('   link: ', link)
                print('   last: ', last, '\n')
                print('   new_: ', new)
                print('+-----------------------------------------------+')
                self._update_link(link, new)
            print('                LINKS UPDATED\n')
        else: print('                NO CHANGES IN LINKS\n')

    def _readme(self):
        sho = '../README/check_anime_links_0.txt'
        readme(sho)

    def _call_func(self, que):
        return {
            '1': self._add_link,
            '2': self._delete_link,
            '3': self._check_link
        }.get(que, exit)()

    def main(self):
        self._readme()
        if exists(self._db_name):
            self.db = connect(self._db_name)
            self.cur = self.db.cursor()
            while True:
                print("""
1: ADD NEW LINKS    [ ДОБАВИТЬ АНИМЕ ССЫЛКУ ]
2: DELETE LINKS     [ УДАЛИТЬ АНИМЕ ССЫЛКУ ]
3: CHECK LINKS      [ ПРОВЕРИТЬ ССЫЛКИ НА НОВЫЕ СЕРИИ ]
            """)
                que = input('?: ')
                self._call_func(que)
            self.db.close()
        else:
            if not exists(self.up_folder):
                mkdir(self.up_folder)
            with connect(self._db_name) as conn:
                cur = conn.cursor()
                cur.execute("""CREATE TABLE links (items text, name text)""")
                conn.commit()
            self.main()


if __name__ == '__main__':
    chl = CheckLinks()
    chl.main()
