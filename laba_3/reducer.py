#!/usr/bin/env python
__author__ = 'Pavel Gladkov'

import sys

last_uid = None
domains_count = {}


def print_cats(_uid, _domains_count):
    pass

if __name__ == '__main__':

    for line in sys.stdin:
        line = line.strip()

        try:
            uid, domain = line.split('\t', 1)
            uid = int(domain)
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