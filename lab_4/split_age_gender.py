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

    train_file = open('age_gender/data/train.csv', 'w')
    test_file = open('age_gender/data/test.csv', 'w')
    data_file = open('age_gender/data/gender_age_dataset.txt', 'r')

    logger.info("get all domains")
    # домены-фичи, только хорошие
    all_domains = get_good_domains(domains_filename='/home/pgladkov/P/BigData/lab_4/age_gender/data/good_domains.txt',
                                   dataset_file=data_file)

    ages = ['18-24', '25-34', '35-44', '45-54', '>=55']
    genders = ['M', 'F']
    classes = []
    for a in ages:
        for g in genders:
            classes.append(a+g)

    train_writer = csv.DictWriter(train_file, ['cl'] + all_domains)
    train_writer.writeheader()

    test_writer = csv.DictWriter(test_file, ['uid'] + all_domains)
    test_writer.writeheader()

    logger.info("start split")

    def get_result_dict(_data):
        _d_count = get_domains_count(_data.get('visits', []))
        _total_visits = 0
        for _k, _v in _d_count.iteritems():
            _total_visits += _v
        _result_dict = {}
        for _domain in all_domains:
            _v = _d_count.get(_domain, 0)
            _result_dict[_domain] = _v

        return _result_dict

    # курсор в начало файла
    data_file = open('age_gender/data/gender_age_dataset.txt', 'r')
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

        if gender == '-':
            result_dict = get_result_dict(data)
            result_dict['uid'] = uid
            test_writer.writerow(result_dict)
        else:
            result_dict = get_result_dict(data)
            result_dict['cl'] = age + gender
            train_writer.writerow(result_dict)

    test_file.close()
    train_file.close()