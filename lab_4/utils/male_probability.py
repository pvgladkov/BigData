__author__ = 'pavel'


from utils import get_domains
import json
import os
import operator


THRESHOLD = 6


def _get_all_domains(_file):
    _d = dict()
    for _l in _file:
        _l = _l.strip()
        _fields = _l.split('\t')
        try:
            _data = json.loads(_fields[2])
        except (IndexError, ValueError):
            continue
        dd = get_domains(_data.get('visits', []))
        for _dom in dd:
            _d[_dom] = 1
    return _d.keys()


def _get_all_domains_count(_file):
    _d = dict()
    for _l in _file:
        _l = _l.strip()
        _fields = _l.split('\t')
        try:
            _data = json.loads(_fields[2])
        except (IndexError, ValueError):
            continue
        dd = get_domains(_data.get('visits', []))
        for _dom in dd:
            try:
                _d[_dom] += 1
            except KeyError:
                _d[_dom] = 1

    return _d


def _get_all_domains_male_female_count(_file):
    _d = dict()
    for _l in _file:
        _l = _l.strip()
        _fields = _l.split('\t')
        try:
            _gender = _fields[0]
            _data = json.loads(_fields[2])
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


def get_all_domains():
    path = 'data/all_domains.txt'
    if os.path.exists(path):
        domain_file = open(path, 'r')
        all_domains = []
        for line in domain_file:
            all_domains.append(line.strip())

    else:
        domain_file = open(path, 'w')
        f = open('gender_dataset.txt', 'r')
        all_domains = _get_all_domains(f)
        map(lambda x: domain_file.write(x+'\n'), all_domains)

    domain_file.close()
    return all_domains


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


def get_domains_stat():
    path = 'data/domains_stat.txt'
    if os.path.exists(path):
        domain_file = open(path, 'r')
        good_domains = []
        for line in domain_file:
            good_domains.append(line.strip())

    else:
        domain_file = open(path, 'w')
        f = open('gender_dataset.txt', 'r')
        all_domains = _get_all_domains_male_female_count(f)

        val_metric = {}

        good_domains = []
        for k, v in all_domains.iteritems():
            male_count = float(v.get('M', 0))
            female_count = float(v.get('F', 0))
            if male_count + female_count > 0:
                val = abs(male_count - female_count) / (male_count + female_count)
            else:
                val = 0
            if 0 < val < 0.2 and male_count > THRESHOLD:
                val_metric[k] = val
            s = "%s\t%s\t%s\t%s\t%f" % (k, male_count, female_count, v.get('-', 0), val)
            good_domains.append(s)
            domain_file.write(s+'\n')

        import operator
        sorted_x = sorted(val_metric.items(), key=operator.itemgetter(1))
        for _i in sorted_x:
            print(_i)
    domain_file.close()
    return good_domains