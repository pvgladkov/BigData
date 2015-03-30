#!/usr/bin/env python
__author__ = 'Pavel Gladkov'

import sys
import urlparse
import urllib

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

        result = urlparse.urlparse(urllib.unquote(url))
        domain = result.netloc
        domain = domain.replace('www.', '')

        print("%s\t%s" % (uid, domain))