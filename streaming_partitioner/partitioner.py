#!/usr/bin/python
__author__ = 'Pavel Gladkov'

import sys

res = {}

for line in sys.stdin:
    line = line.strip()

    key, val = line.split('\t')

    print(val / 1)