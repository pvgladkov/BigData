#!/usr/bin/python
__author__ = 'Pavel Gladkov'

import sys

res = {}

for line in sys.stdin:
    line = line.strip()

    country, val = line.split('\t', 1)
    try:
        val = float(val)
    except ValueError:
        continue

    try:
        res[country] = res[country] + val
    except:
        res[country] = val

for country in res.keys():
    print('%s\t%s' % (country, res[country]))