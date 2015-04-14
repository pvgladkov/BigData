__author__ = 'pavel'


import urlparse
import functools
import time
import logging
import re


__all__ = ['timed', 'get_domain', 'get_domains', 'get_domains_count']


def timed(logger_, level=None, form='%s: %s ms'):
    if level is None:
        level = logging.DEBUG

    def decorator(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            start = time.time()
            result = fn(*args, **kwargs)
            duration = time.time() - start
            logger_.log(level, form, repr(fn), duration * 1000)
            return result
        return inner

    return decorator


def get_domains_count(visits):
    _d = {}
    for _v in visits:
        url = _v.get('url', '').encode('utf-8')
        _domain = get_domain(url)
        if _domain is None:
            continue
        try:
            _d[_domain] += 1
        except KeyError:
            _d[_domain] = 1
    return _d


def get_domain(_url):
    re_http = re.compile(r"https?://")
    domain = urlparse.urlparse(
       "http://" + re_http.sub("", _url)
    ).hostname

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
