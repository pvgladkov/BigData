#!/usr/bin/python
__author__ = 'Pavel Gladkov'

import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split(',')

    try:
        print(fields[2]+"\t"+fields[4])
    except IndexError:
        pass