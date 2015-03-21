#!/usr/bin/python
__author__ = 'Pavel Gladkov'

import sys

res = {}

for line in sys.stdin:
    line = line.strip()

    key, val = line.split('\t')
    try:
        val = float(val)
    except ValueError:
        continue

    try:
        res[key] += val
    except KeyError:
        res[key] = val

for key in res.keys():
    print('%s\t%s' % (key, res[key]))