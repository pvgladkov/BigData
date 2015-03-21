#!/usr/bin/python
__author__ = 'Pavel Gladkov'


import sys
import happybase
import happybase.hbase


if __name__ == '__main__':

    N = 138

    connection = happybase.Connection('ec2-52-16-15-152.eu-west-1.compute.amazonaws.com')
    connection.open()

    try:
        connection.create_table(
            'pavel.gladkov',
            {'data': dict()}
        )
    except happybase.hbase.ttypes.AlreadyExists:
        pass

    table = connection.table('pavel.gladkov')
    row = table.row('2662148490', include_timestamp=True)
    print row
    # for key, data in table.scan():
    #     print key, data
    #     break