__author__ = 'pavel'

import os
import operator
import json
from utils import get_domains

THRESHOLD = 8


def _get_all_domains_male_female_count(_file):
    _d = dict()
    for _l in _file:
        _l = _l.strip()
        _fields = _l.split('\t')
        try:
            _gender = _fields[0]
            _data = json.loads(_fields[3])
        except (IndexError, ValueError):
            continue
        dd = get_domains(_data.get('visits', []))
        for _dom in dd:
            __d = _d.get(_dom, {})
            try:
                __d[_gender] += 1
            except KeyError:
                __d[_gender] = 1
            _d[_dom] = __d

    return _d


def _get_all_age_count(_file):
    result_ages = dict()
    for _l in _file:
        _l = _l.strip()
        _fields = _l.split('\t')
        try:
            _age = _fields[1]
            _data = json.loads(_fields[3])
        except (IndexError, ValueError):
            continue
        dd = get_domains(_data.get('visits', []))
        for _dom in dd:
            try:
                result_ages[_age] += 1
            except KeyError:
                result_ages[_age] = 1

    return result_ages


def get_all_age_count(_file):
    return _get_all_age_count(_file)


def get_good_domains(domains_filename, dataset_file):
    path = domains_filename
    if os.path.exists(path):
        domain_file = open(path, 'r')
        good_domains = []
        for line in domain_file:
            good_domains.append(line.strip())

    else:
        domain_file = open(path, 'w')

        all_domains_stat = _get_all_domains_male_female_count(dataset_file)
        good_domains = {}
        for k, gender_stat in all_domains_stat.iteritems():
            male_count = float(gender_stat.get('M', 0))
            female_count = float(gender_stat.get('F', 0))
            v = male_count + female_count
            if v > 0:
                val = abs(male_count - female_count) / (male_count + female_count)
            else:
                val = 0
            if v > THRESHOLD and val > 0.2:
                good_domains[k] = v

        sorted_x = sorted(good_domains.items(), key=operator.itemgetter(1), reverse=True)
        sorted_x = sorted_x[0:1000]
        good_domains = []
        map(lambda x: domain_file.write(x[0]+'\n'), sorted_x)
        map(lambda x: good_domains.append(x[0]), sorted_x)

    domain_file.close()
    return good_domains

