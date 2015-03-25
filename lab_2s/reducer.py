#!/usr/bin/env python
__author__ = 'Pavel Gladkov'

import sys

res = {}

last_url = None
count = 0

for line in sys.stdin:
    line = line.strip()

    try:
        url, val = line.split('\t', 1)
        val = int(val)
    except ValueError:
        continue

    if last_url is None:
        last_url = url

    if last_url == url:
        count += val
    else:
        print('%s\t%s' % (last_url, count))
        count = val
        last_url = url

print('%s\t%s' % (last_url, count))