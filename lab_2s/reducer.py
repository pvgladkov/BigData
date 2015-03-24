#!/usr/bin/env python
__author__ = 'Pavel Gladkov'

import sys

res = {}

for line in sys.stdin:
    line = line.strip()

    try:
        url, val = line.split('\t', 1)
        val = int(val)
    except ValueError:
        continue

    try:
        res[url] = res[url] + val
    except:
        res[url] = val

for url in res.keys():
    print('%s\t%s' % (url, res[url]))