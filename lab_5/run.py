#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Pavel Gladkov'


import logging
import json
from vk_lib import Vk
from collections import Counter
from datetime import date, timedelta, datetime
import re
from dateutil.relativedelta import relativedelta

if __name__ == '__main__':

    GROUP_ID = 62425030

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d-%y %H:%M:%S')

    logger = logging.getLogger(__name__)

    result = {'gender': {}, 'age': {}, 'top_interest': ''}

    r_gender = {'male': 0, 'female': 0, '?': 0}
    r_age = {"<=10": 0, "11-20": 0, "21-30": 0, "?": 0, ">=31": 0}
    r_interests = []

    def num_years(begin, end):
        _num_years = int((end - begin).days / 365.25)
        if begin > yearsago(_num_years, end):
            return _num_years - 1
        else:
            return _num_years

    def yearsago(years, from_date):
        return from_date - relativedelta(years=years)

    def get_age_group(_date):
        if _date is None:
            return "?"
        try:
            day, month, year = _date.split('.')
            start_date = date(int(year), int(month), int(day))
        except ValueError:
            return "?"

        end_date = date(2015, 4, 1)
        years = num_years(start_date, end_date)
        if years <= 10:
            return '<=10'
        if 11 <= years <= 20:
            return '11-20'
        if 21 <= years <= 30:
            return '21-30'
        if years >= 31:
            return '>=31'

        return "?"

    vk_api = Vk()

    # пол
    for i in xrange(0, 1500, 500):
        members = vk_api.get_members(GROUP_ID, 'sex', 500, i)
        logger.info('count: %s' % members.get('count', 0))
        member_list = members.get('items', [])
        for member in member_list:
            gender = int(member.get('sex', 0))
            if gender == 1:
                r_gender['female'] += 1
            if gender == 2:
                r_gender['male'] += 1
            if gender == 0:
                r_gender['?'] += 1

        # возраст
        members = vk_api.get_members(GROUP_ID, 'bdate', 500, i)
        logger.info('count: %s' % members.get('count', 0))
        member_list = members.get('items', [])
        for member in member_list:
            r_age[get_age_group(member.get('bdate'))] += 1

        # интересы
        members = vk_api.get_members(GROUP_ID, 'interests', 500, i)
        logger.info('count: %s' % members.get('count', 0))
        member_list = members.get('items', [])
        p1 = re.compile("[\u0400-\u0500a-z\s\'\"]{4,}")
        for member in member_list:
            inter = member.get('interests', False)
            if inter:
                user_i = p1.findall(inter.encode('utf-8').lower())
                user_i = [i.strip() for i in user_i]
                user_i = list(set(user_i))
                r_interests += user_i

    # результат
    with open('lab5statistics.json', 'w') as f:
        counter = Counter(r_interests)
        print counter.most_common()
        result['top_interest'] = counter.most_common(1)[0][0]
        result['gender'] = r_gender
        result['age'] = r_age

        f.write(json.dumps(result))
        f.close()

    logger.info('finish')