#!/usr/bin/python
__author__ = 'Pavel Gladkov'

import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split(',')

    try:
        print("%s\t%s" % (fields[0], fields[1]))
    except IndexError:
        pass