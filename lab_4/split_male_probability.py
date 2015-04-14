__author__ = 'pavel'
# -*- coding: utf-8 -*-

import csv
import json
from utils.male_probability import get_all_domains, get_good_domains, get_domains_stat
from utils.utils import get_domain, get_domains_count
import logging


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d-%y %H:%M:%S')

    logger = logging.getLogger(__name__)

    logger.info("get all domains")

    f = open('male_probability/data/gender_dataset.txt', 'r')

    # домены-фичи, только хорошие
    all_domains = get_good_domains(
        domains_filename='/home/pavel/P/BigData/lab_4/male_probability/data/good_domains.txt',
        dataset_file=f)

    logger.info('domains count %d' % len(all_domains))

    logger.info("start split")

    train_file = open('male_probability/data/train_2.csv', 'w')
    test_file = open('male_probability/data/test_2.csv', 'w')

    train_writer = csv.DictWriter(train_file, ['male', 'uid', 'total_visits', 'unique_domains'] + all_domains)
    train_writer.writeheader()

    test_writer = csv.DictWriter(test_file, ['uid', 'total_visits', 'unique_domains'] + all_domains)
    test_writer.writeheader()

    def get_result_dict(_data):
        _d_count = get_domains_count(_data.get('visits', []))
        _total_visits = 0
        for _k, _v in _d_count.iteritems():
            _total_visits += _v
        _result_dict = {'total_visits': _total_visits, 'unique_domains': len(_d_count)}
        for _domain in all_domains:
            _v = _d_count.get(_domain, 0)
            _result_dict[_domain] = _v
        return _result_dict

    f = open('male_probability/data/gender_dataset.txt', 'r')
    for line in f:
        line = line.strip()
        fields = line.split('\t')
        try:
            gender = fields[0]
            uid = fields[1]
            data = json.loads(fields[2])
        except (IndexError, ValueError):
            continue

        if gender == '-':
            result_dict = get_result_dict(data)
            result_dict['uid'] = uid
            test_writer.writerow(result_dict)
        else:
            if gender == 'M':
                male = 1
            else:
                male = 0
            result_dict = get_result_dict(data)
            result_dict['uid'] = uid
            result_dict['male'] = male
            train_writer.writerow(result_dict)

    test_file.close()
    train_file.close()