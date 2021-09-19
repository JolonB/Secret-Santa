import numpy as np


def get_graph(people: dict):
    keys = list(people.keys())
    people = dict(people)  # create a copy of `people` and delete the original

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
            for excluded in blacklist:
                excluded_person = people.get(excluded)
                if excluded_person:
                    graph[person_index][excluded_person["index"]] = 0

    return graph, keys
