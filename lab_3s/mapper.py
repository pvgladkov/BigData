#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Pavel Gladkov'


import sys
import urlparse
import urllib

if __name__ == "__main__":

    auto_domains = ['cars.ru', 'avto-russia.ru', 'bmwclub.ru']

    # файл со списком автомобилистов
    f = open('autousers_lab3S.txt', 'r')
    auto_users = []
    for user_id in f:
        auto_users.append(int(user_id.strip()))

    for line in sys.stdin:
        line = line.strip()
        fields = line.split('\t')
        try:
            uid = int(fields[0])
            timestamp = fields[1]
            url = fields[2]
        except (IndexError, ValueError):
            continue

        result = urlparse.urlparse(urllib.unquote(url))
        domain = result.netloc
        domain = domain.replace('www.', '')

        is_auto_user = 1 if uid in auto_users else 0

        print("%s\t%d" % (domain, is_auto_user))