__author__ = 'Pavel Gladkov'
# -*- coding: utf-8 -*-


import logging
from utils.age_gender import *
from utils.utils import get_domains_count
import csv


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d-%y %H:%M:%S')

    logger = logging.getLogger(__name__)

    data_file = open('age_gender/data/gender_age_dataset.txt', 'r')
    result_file = open('age_gender/data/gender_age_stat.csv', 'w')
    test_result_file = open('age_gender/data/test_gender_age_stat.csv', 'w')

    ages = ['18-24', '25-34', '35-44', '45-54', '>=55']
    genders = ['M', 'F']

    writer = csv.DictWriter(result_file, ['domain', 'total'] + genders + ages)
    writer.writeheader()

    test_writer = csv.DictWriter(test_result_file, ['domain', 'total'])
    test_writer.writeheader()

    # статистика по доменам
    result = {}

    test_result = {}

    for line in data_file:
        line = line.strip()
        fields = line.split('\t')
        try:
            gender = fields[0]
            age = fields[1]
            uid = fields[2]
            data = json.loads(fields[3])
        except (IndexError, ValueError):
            continue

        if gender == '-' or age == '-':

            if gender != '-' or age != '-':
                logger.info(gender + ' ' + age)
            _d_count = get_domains_count(data.get('visits', []))
            for domain, domain_count in _d_count.iteritems():
                domain_stat = result.get(domain, {'total': 0})
                domain_stat['total'] += domain_count

                test_result[domain] = domain_stat
        else:
            # статистика по доменам
            _d_count = get_domains_count(data.get('visits', []))

            for domain, domain_count in _d_count.iteritems():
                domain_stat = result.get(domain, {'total': 0, '18-24': 0, '25-34': 0,
                                                  '35-44': 0, '45-54': 0, '>=55': 0, 'M': 0, 'F': 0})
                domain_stat[age] += domain_count
                domain_stat[gender] += domain_count
                domain_stat['total'] += domain_count

                result[domain] = domain_stat

    logger.info('write to file')

    for domain, stat in result.iteritems():
        row = {'domain': domain}
        for key, value in stat.iteritems():
            row[key] = value

        writer.writerow(row)

    for domain, count in test_result.iteritems():
        row = {'domain': domain, 'total': count.get('total', 0)}

        test_writer.writerow(row)