#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Pavel Gladkov'

import sys

if __name__ == "__main__":

    count = 0
    for line in sys.stdin:
        line = line.strip()
        fields = line.split('\t')
        if fields[0] == 'auto':
            count += 1

    print("res\t%d" % count)