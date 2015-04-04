#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Pavel Gladkov'

import sys

if __name__ == "__main__":

    # Общее кол-во посещений, которое совершили автомобилисты
    AUTO_COUNT = 0

    last_domain = None
    last_c = 0

    for line in sys.stdin:

        line = line.strip()
        fields = line.split('\t')
        try:
            domain = fields[0]
            values = fields[1]
        except IndexError:
            continue

        if last_domain is None:
            last_domain = domain

        is_auto_user, is_auto_domain = values.split(';')

