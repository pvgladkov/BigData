__author__ = 'pavel'

import csv
import json

if __name__ == "__main__":

    f = open('gender_dataset.txt', 'r')
    train_file = open('train.csv', 'w')
    test_file = open('test.csv', 'w')
    train_writer = csv.DictWriter(train_file, ['male', 'uid', 'url', 'timestamp'])
    test_writer = csv.DictWriter(test_file, ['uid', 'url', 'timestamp'])
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
            for v in data.get('visits', []):
                test_writer.writerow(
                    {'uid': uid, 'url': v.get('url', '').encode('utf-8'), 'timestamp': v.get('timestamp', 0)}
                )
        else:
            if gender == 'M':
                male = 1
            else:
                male = 0
            for v in data.get('visits', []):
                train_writer.writerow(
                    {'male': male, 'uid': uid, 'url': v.get('url', '').encode('utf-8'), 'timestamp': v.get('timestamp', 0)}
                )

    test_file.close()
    train_file.close()