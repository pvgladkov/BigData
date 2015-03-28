#!/usr/bin/env python
__author__ = 'Pavel Gladkov'

import sys

res = {}

if __name__ == '__main__':

    p = 1
    try:
        key = sys.argv[1]
        value = sys.argv[2]
        num_part = sys.argv[3]
        p = hash(key) % num_part
    except IndexError:
        pass

    print(p)