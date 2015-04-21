#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Pavel Gladkov'


import logging
import json
from vk_lib import Vk

if __name__ == '__main__':

    GROUP_ID = 62425030

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d-%y %H:%M:%S')

    logger = logging.getLogger(__name__)

    result = {'gender': {}, 'age': {}, 'top_interest': ''}

    vk_api = Vk()
    members = vk_api.get_members(GROUP_ID)
    logger.info('count: %s' % members.get('count', 0))

    member_list = members.get('items', [])

    # результат
    with open('lab5statistics.json', 'w') as f:
        f.write(json.dumps(result))
        f.close()

    logger.info('finish')