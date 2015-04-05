__author__ = 'pavel'


import urlparse
import urllib

def get_domain(_url):
    result = urlparse.urlparse(urllib.unquote(_url))
    domain = result.netloc
    domain = domain.replace('www.', '')
    return domain