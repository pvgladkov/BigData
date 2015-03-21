#!/usr/bin/python
__author__ = 'Pavel Gladkov'


import sys
import happybase
import happybase.hbase


def load(table_, uid_, timestamp_, url_):

    n = 138
    try:
        uid_ = int(uid_)
        timestamp_ = float(timestamp_) * 1000
    except ValueError:
        return False

    if uid_ % 256 == n:
        table_.put(str(uid_), {'data:url': url_}, timestamp=int(timestamp_))

    return True


if __name__ == '__main__':

    connection = happybase.Connection('ec2-52-16-15-152.eu-west-1.compute.amazonaws.com')
    connection.open()

    try:
        connection.create_table(
            'pavel.gladkov',
            {'data': dict(max_versions = 10000)}
        )
    except happybase.hbase.ttypes.AlreadyExists:
        pass

    table = connection.table('pavel.gladkov')

    for line in sys.stdin:
        fields = line.split('\t')
        try:
            uid = fields[0]
            timestamp = fields[1]
            url = fields[2]
        except IndexError:
            continue

        load(table, uid, timestamp, url)