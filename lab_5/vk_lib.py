# -*- coding: utf-8 -*-
__author__ = 'Pavel Gladkov'


import requests


class Vk(object):

    def __init__(self):
        self._url = 'http://ec2-52-17-77-210.eu-west-1.compute.amazonaws.com/method/'

    def get_members(self, group_id):
        method = 'groups.getMembers'
        r = requests.get(self._url + method, params={'group_id': group_id})
        return r.json().get('response', {})

    def get_profile(self, user_id):
        method = 'users.get'
        r = requests.get(self._url + method, params={'user_id': user_id})
        print r.url
        return r.text