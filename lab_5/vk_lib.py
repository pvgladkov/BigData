# -*- coding: utf-8 -*-
__author__ = 'Pavel Gladkov'


import requests


class Vk(object):

    def __init__(self):
        self._url = 'http://ec2-52-17-77-210.eu-west-1.compute.amazonaws.com/method/'

    def get_members(self, group_id, field):
        method = 'groups.getMembers'
        _fields = [field]
        r = requests.get(self._url + method, params={'group_id': group_id, 'fields': _fields})
        return r.json().get('response', {})