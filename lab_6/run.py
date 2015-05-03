#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cPickle
import json
import time
import logging
import networkx as nx
from harmonic_centrality import harmonic_centrality as hc
from networkx.algorithms.link_analysis import pagerank
import operator
import requests
import requests.exceptions

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d-%y %H:%M:%S')

logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

MY_GROUP_ID = 90021065

SERVER_URL = "http://ec2-52-17-77-210.eu-west-1.compute.amazonaws.com/method/"
WINDOW_SIZE = 1000

COUNT = requests.get(
    SERVER_URL + "groups.getMembers?scope=super&group_id={0}".format(
        MY_GROUP_ID
    )
).json()["response"]["count"]

build_group_request = lambda d: SERVER_URL + (
    "groups.getMembers?scope=super&group_id={0}&{1}".format(
        MY_GROUP_ID,
        "&".join([
            "=".join([k, str(v)])
            for k, v in d.items()
        ])
    )
)

build_friends_request = lambda _user_id: SERVER_URL + (
    "friends.get?v=5.29&lang=en&user_id={0}".format(_user_id)
)

build_followers_request = lambda _user_id: SERVER_URL + (
    "users.getFollowers?v=5.29&lang=en&user_id={0}".format(_user_id)
)

pages = (
    requests.get(
        build_group_request({
            "offset": WINDOW_SIZE * i,
            "count": WINDOW_SIZE,
        })
    ).json()['response']['items']
    for i in xrange(int(float(COUNT) / WINDOW_SIZE + 1))
)


def get_user_ids():
    ids_dump_filename = "all_ids.pickle"
    if not os.path.exists(ids_dump_filename):
        user_ids = set()
        for i, page in enumerate(pages):
            logger.info("Page {0} from {1}".format(i, int(float(COUNT) / WINDOW_SIZE)))
            for _user_id in page:
                user_ids.add(_user_id)

        with open(ids_dump_filename, "w") as _dump:
            logger.info('dump to file, total %d' % len(user_ids))
            cPickle.dump(user_ids, _dump, cPickle.HIGHEST_PROTOCOL)
    else:
        with open(ids_dump_filename, "r") as _dump:
            user_ids = cPickle.load(_dump)
            logger.info('load from file, total %d' % len(user_ids))
    return user_ids


def get_graph():
    # строим граф
    graph_dump_filename = "graph.pickle"
    user_ids = get_user_ids()
    if not os.path.exists(graph_dump_filename):

        graph = nx.Graph(directed=False)

        counter = 0
        for user_id in user_ids:

            counter += 1
            graph.add_node(user_id)

            if counter % 10 == 0:
                logger.info(counter)

            try:
                res_friends = requests.get(build_friends_request(user_id), timeout=5).json()
            except requests.exceptions.ConnectionError:
                time.sleep(5)
                res_friends = requests.get(build_friends_request(user_id), timeout=5).json()

            try:
                res_followers = requests.get(build_followers_request(user_id), timeout=5).json()
            except requests.exceptions.ConnectionError:
                time.sleep(5)
                res_followers = requests.get(build_followers_request(user_id), timeout=5).json()

            friends_ids = set(res_friends['response']['items']) & user_ids
            followers_ids = set(res_followers['response']['items']) & user_ids

            _ids = friends_ids.union(followers_ids)

            for f_id in _ids:
                graph.add_node(f_id)
                graph.add_edge(user_id, f_id)

        with open(graph_dump_filename, "w") as dump:
            cPickle.dump(graph, dump, cPickle.HIGHEST_PROTOCOL)
    else:
        with open(graph_dump_filename, "r") as dump:
            graph = cPickle.load(dump)

    return graph

if __name__ == "__main__":

    G = get_graph()

    result = {
      "pagerank_ids": [],
      "harmonic_ids": []
    }

    logger.info('graph nodes %d' % G.number_of_nodes())

    logger.info('harmonic')
    harmonic = hc(G)
    sorted_h = sorted(harmonic.items(), key=operator.itemgetter(1), reverse=True)
    result['harmonic_ids'] = map(lambda x: str(x[0]), sorted_h[0:200])

    logger.info('pr')
    pr = pagerank(G, alpha=0.8507246376811566)
    sorted_pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)
    result['pagerank_ids'] = map(lambda x: str(x[0]), sorted_pr[0:200])

    with open('lab6centralities.json', 'w') as f:
        f.write(json.dumps(result))
        f.close()

    logger.info('finish')