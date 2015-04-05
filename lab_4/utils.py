__author__ = 'pavel'


import urlparse
import urllib


def get_domain(_url):
    result = urlparse.urlparse(urllib.unquote(_url))
    domain = result.hostname

    if domain == 'http' or domain == 'https':
        _url = _url.replace(domain + '://', '', 1)
        return None
    domain = domain.replace('www.', '')
    # a_d = domain.split('.')
    # if len(a_d) > 2:
    #     domain = '.'.join(a_d[-2:])
    return domain