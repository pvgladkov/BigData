#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Pavel Gladkov'

import sys

if __name__ == "__main__":

    def print_result(a_count, t_count, _d):
        if t_count == 0:
            return False
        _rel = a_count * a_count / (t_count * AUTO_COUNT)
        print("%s\t%.10f" % (_d, _rel))

    # Общее кол-во посещений, которое совершили автомобилисты
    AUTO_COUNT = 172767.

    last_domain = None

    # сколько раз домен посещали автомобилисты
    auto_domain_count = 0

    # сколько раз всего посещали домен
    total_domain_count = 0

    for line in sys.stdin:

        line = line.strip()
        fields = line.split('\t')
        try:
            domain = fields[0]
            is_auto_user = int(fields[1])
        except (IndexError, ValueError):
            continue

        if last_domain is None:
            last_domain = domain

        if last_domain == domain:
            total_domain_count += 1
            auto_domain_count += is_auto_user
        else:
            print_result(auto_domain_count, total_domain_count, last_domain)
            last_domain = domain
            total_domain_count = 0
            auto_domain_count = 0

    print_result(auto_domain_count, total_domain_count, last_domain)