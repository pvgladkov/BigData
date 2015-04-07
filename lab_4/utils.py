__author__ = 'pavel'


import urlparse
import urllib
import json
import os


def get_domain(_url):
    result = urlparse.urlparse(urllib.unquote(_url))
    domain = result.hostname

    if domain == 'http' or domain == 'https':
        _url = _url.replace(domain + '://', '', 1)
        return get_domain(_url)
    domain = domain.replace('www.', '')
    # a_d = domain.split('.')
    # if len(a_d) > 2:
    #     domain = '.'.join(a_d[-2:])
    return domain


def get_domains(visits):
    _d = []
    for _v in visits:
        url = _v.get('url', '').encode('utf-8')
        _domain = get_domain(url)
        if _domain is not None:
            _d.append(_domain)
    return _d


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


def get_good_domains():
    path = 'data/good_domains.txt'
    if os.path.exists(path):
        domain_file = open(path, 'r')
        good_domains = []
        for line in domain_file:
            good_domains.append(line.strip())

    else:
        domain_file = open(path, 'w')
        f = open('gender_dataset.txt', 'r')
        all_domains = _get_all_domains_count(f)

        good_domains = []
        for k, v in all_domains.iteritems():
            if v > 6:
                good_domains.append(k)

        map(lambda x: domain_file.write(x+'\n'), good_domains)

    domain_file.close()
    return good_domains