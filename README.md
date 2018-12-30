# lolicon-page
parsing anime web-sites to get info about updates (new anime series), and show it in local web-site
```
1: Install modules :: Скачать необходимые библиотеки
(env) [/lolicon-page/]$ pip install -r requirements

2: add url to the database !required :: Добавить ссылку в базу, важно чтобы этот модуль запуспалься первым
(env) [/cli/]$ python start.py --link http://animevost.org/???

3: run the local server :: Запустить локальный сервер
(env) [/lolicon-page/]$ python main.py


@cli arguments :: по аргументам

    *plz run: (env) [/cli/] python start.py --help first :: для информации

    --link http.://.../...  - to add link :: Шаг №2
    --add_loop 1            - add links in while loop with input :: Чтобы не писать --link если у вас много ссылок

    *without arguments it will search updates*.
        new series (last state) in green color while script can't find new updates

    *скрипт без аргументов проверяет обновление. Осторожно! это может изменить данные (и сменить цвет).
        новые серии отмечаны Зеленым цветом Пока скрипт не найдет новые серии

I've edited <updates.json> to take a screenshot :)
```
![test-pic](https://raw.githubusercontent.com/hhiki/lolicon-page/dev/test-pic/lolicon-page.jpg)
![test-pic_version_1](https://raw.githubusercontent.com/hhiki/lolicon-page/dev/test-pic/lolicon-page_v_1.jpg)
