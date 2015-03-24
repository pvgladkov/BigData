#!/usr/bin/env python
__author__ = 'Pavel Gladkov'


import sys


if __name__ == '__main__':

    for line in sys.stdin:
        line = line.strip()
        fields = line.split('\t')
        try:
            uid = int(fields[0])
            timestamp = fields[1]
            url = fields[2]
        except (IndexError, ValueError):
            continue

        print("%s\t1" % url)