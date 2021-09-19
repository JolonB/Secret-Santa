import sys
from typing import Iterable

import numpy as np


def get_graph(people: dict):
    keys = list(people.keys())
    people = dict(people)  # create a copy of `people` so we don't modify the original

    for index, key in enumerate(keys):
        people[key].update({"index": index})

    graph_size = len(people)
    graph = np.ones((graph_size, graph_size))

    for key in keys:
        person_index = people[key]["index"]
        graph[person_index][person_index] = 0

        # Set the graph to zero if the person is in the exclude list
        blacklist = people[key].get("exclude")

        if blacklist:
            # If the blacklist is just a string, convert it to a singleton list
            if isinstance(blacklist, str):
                blacklist = [blacklist]
            # Convert the blacklist to list if it is any type of iterable
            if isinstance(blacklist, Iterable):
                blacklist = list(blacklist)
            else:
                print(
                    "WARNING: The excluded item {} is invalid".format(blacklist),
                    file=sys.stderr,
                )

            for excluded in blacklist:
                excluded_person = people.get(excluded)
                if excluded_person:
                    graph[person_index][excluded_person["index"]] = 0

    return graph, keys
