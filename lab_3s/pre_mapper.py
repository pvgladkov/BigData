#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Pavel Gladkov'

import sys


# ищем кол-во посещений автомобилистов

if __name__ == "__main__":

    # файл со списком автомобилистов
    f = open('autousers_lab3S.txt', 'r')
    auto_users = []
    for user_id in f:
        auto_users.append(int(user_id.strip()))

    print auto_users

    for line in sys.stdin:
        line = line.strip()
        fields = line.split('\t')
        try:
            uid = int(fields[0])
            timestamp = fields[1]
            url = fields[2]
        except (IndexError, ValueError):
            continue

        if uid in auto_users:
            print("auto\t1")