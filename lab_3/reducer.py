#!/usr/bin/env python
__author__ = 'Pavel Gladkov'

import sys


def print_cats(_uid, _domains_count):

    classifier = [
        ['cars.ru', 'avto-russia.ru', 'bmwclub.ru'],
        ['zakon.kz', 'egov.kz', 'makler.md'],
        ['novayagazeta.ru', 'echo.msk.ru', 'inosmi.ru'],
        ['snowmobile.ru', 'nastroisam.ru', 'mobyware.ru'],
        ['postnauka.ru', 'plantarium.ru', 'lensart.ru']
    ]

    _classes = [0, 0, 0, 0, 0]

    for i, _class in enumerate(classifier):
        pages = 0
        _c = 0
        for _d in _class:
            v_count = _domains_count.get(_d, 0)
            pages += v_count
            if v_count > 0:
                _c += 1
        _classes[i] = 1 if pages >= 3 and _c >= 2 else 0

    _p = [_uid] + _classes
    print("%s\t%s\t%s\t%s\t%s\t%s" % tuple(_p))

if __name__ == '__main__':

    last_uid = None
    domains_count = {}

    for line in sys.stdin:
        line = line.strip()

        try:
            uid, domain = line.split('\t', 1)
            uid = int(uid)
        except ValueError:
            continue

        if last_uid is None:
            last_uid = uid

        if last_uid == uid:
            try:
                domains_count[domain] += 1
            except KeyError:
                domains_count[domain] = 1
        else:
            print_cats(last_uid, domains_count)
            domains_count = {domain: 1}
            last_uid = uid

    print_cats(last_uid, domains_count)