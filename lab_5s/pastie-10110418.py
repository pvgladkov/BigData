#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cPickle
import json
import Queue
import time

import networkx as nx

import requests

MY_GROUP_ID = 29937606
MY_USER_ID = 182879134

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

build_friends_request = lambda user_id: SERVER_URL + (
    "friends.get?v=5.29&lang=en&user_id={0}".format(user_id)
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


IDS_DUMP_FILENAME = "all_ids.pickle"

if not os.path.exists(IDS_DUMP_FILENAME):
    USER_IDS = set()
    for i, page in enumerate(pages):
        print(
            "Page {0} from {1}".format(i, int(float(COUNT) / WINDOW_SIZE))
        )
        for user_id in page:
            USER_IDS.add(user_id)

    with open(IDS_DUMP_FILENAME, "wb") as dump:
        cPickle.dump(USER_IDS, dump, cPickle.HIGHEST_PROTOCOL)
else:
    with open(IDS_DUMP_FILENAME, "rb") as dump:
        USER_IDS = cPickle.load(dump)

GRAPH_DUMP_FILENAME = "graph.pickle"

if not os.path.exists(GRAPH_DUMP_FILENAME):
    graph = nx.Graph()

    q = Queue.Queue()
    q.put(MY_USER_ID)

    visited = set()

    counter = 0
    while not q.empty():
        current_id = q.get()
        if current_id in visited:
            continue
        counter += 1
        visited.add(current_id)

        friends_ids = set(requests.get(
            build_friends_request(current_id)
        ).json()['response']['items']) & USER_IDS - visited
        print(
            "Found friend N{0}: {1} ({2} friends)".format(
                counter,
                current_id,
                len(friends_ids)
            )
        )

        for f_id in friends_ids:
            graph.add_node(f_id)
            graph.add_edge(current_id, f_id)
            q.put(f_id)
        if counter % 1000 == 0:
            time.sleep(1)

    with open(GRAPH_DUMP_FILENAME, "wb") as dump:
        cPickle.dump(graph, dump, cPickle.HIGHEST_PROTOCOL)
else:
    with open(GRAPH_DUMP_FILENAME, "rb") as dump:
        graph = cPickle.load(dump)

res = {
    "max": nx.eccentricity(graph, MY_USER_ID),
    "mean": 0
}

count = graph.number_of_nodes() - 1
sum_paths = 0
for n in graph.nodes_iter():
    if n == MY_USER_ID:
        continue
    sum_paths += nx.shortest_path_length(
        graph,
        source=MY_USER_ID,
        target=n
    )

res["mean"] = round(float(sum_paths) / count, 10)
print(json.dumps(res))
