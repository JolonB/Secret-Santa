import pdb
import config
import random
import emailsvc
import hamiltonian
import config_parser
import numpy as np
from itertools import permutations
from circular_list import deep_is_circular


def allocate(graph: np.array, step: int = 2) -> list:
    # Fix invalid step sizes
    if step < 2:
        step = 2
    step = int(step)
    # Slice up the graph into subgraphs
    # find every possible permutation of the graph indices
    indices = list(permutations([i for i in range(len(graph))]))
    # groups indices for slicing the graph
    slices = []
    for i in indices:
        sl = slice_index_generator(i, step)
        if sl:
            slices.extend(sl)
    # add full set to sub_graphs
    slices.append((indices[0],))
    sub_graphs = slice_array(graph, slices)

    # Get all Hamiltonian cycles
    cycles = {}
    for index, sub_graph in sub_graphs.items():
        # no need to check the index, as there can only be one of each in sub_graphs
        cycles.update({index: hamiltonian.hamiltonian(sub_graph, False)})

    del sub_graphs  # free up some memory

    # Remove circular duplicates. Use a set to allow for faster access (because sets are hashed)
    valid_keys = set(deep_is_circular(list(cycles.keys())))

    # Shift the cycles (which all start from 0) to use the actual numbers (i.e. map them to the correct nodes in the graph)
    shifted_cycles = {}
    for index, cycle in cycles.items():
        # skip empty cycles
        if not cycle or index not in valid_keys:
            continue
        shifted_cycles.update({index: []})
        for c in cycle:
            new_c = [index[i] for i in c]
            shifted_cycles[index].append(new_c)

    del cycles  # free up some memory
    # print(shifted_cycles)
    # TODO fix something here that causes full cycle results (as in, the entire graph) being counted correctly
    # Get all combinations of hamiltonian cycles (while removing slices of the graph that don't contain cycles)
    full_cycles = []
    for slice_ in slices:
        for tup in slice_:
            # if no cycle exists for a specific graph index tuple (subgraph indices), don't add to new_slices
            if not shifted_cycles.get(tup):
                break
        else:
            full_cycles.extend(group(shifted_cycles, slice_))

    # print(f"full {full_cycles}")

    return random.choice(full_cycles)


def group(cycles: dict, nodes: list, index: int = 0):
    # If last set of values, simply return the last values in the list
    # cycles = {(0,1): [[0,1]], (2,3,4,5): [[2,3,4,5], [2,3,5,4], [2,4,3,5],...], ...}
    # nodes = ((0, 1, 2, 3, 4, 5),), ((0, 1), (2, 3), (4, 5))

    if index == len(nodes) - 1:
        return [
            [n] for n in cycles[nodes[index]]
        ]  # list(list(list)) : [[0,1]], [[[0,1,2,3,4,5]], [[0,1,2,3,4,5]]]
    # Otherwise, recursively build up the output]
    output = []
    for n in cycles[
        nodes[index]
    ]:  # list(list) : [[0, 1, 2], [0, 2, 1], ...] -> n : list : [0, 1, 2]
        groups = group(
            cycles, nodes, index + 1
        )  # list(list(list)) : [[[0, 1], [2, 3], [4, 5]], [[0, 1], [2, 3, 4, 5]]]
        [
            output.append([n] + g) for g in groups
        ]  # g : list(list) : [[0, 1], [2, 3], [4, 5]]
    return (
        output  # list(list(list)) : [[[0, 1], [2, 3], [4, 5]], [[0, 1], [2, 3, 4, 5]]]
    )


def slice_index_generator(indices: tuple, step: int) -> list:
    # indices == [(0,1,2,3),(0,1,3,2),(0,2,1,3),...,(3,2,1,0)], but we are only using one of them (i.e. (0,2,3,1))
    # want to split into every possible sublist with a length of `step` or greater. So we should get [((0,2),(3,1))]. We will not get (0,2,3,1).
    # if we had 5 values (0,1,2,3,4), then we should get [((0,1),(2,3,4)),((0,1,2),(3,4))]
    result = []
    for i in range(step, len(indices) + 1 - step):
        start = indices[:i]  # type == tuple
        end = indices[i:]  # type == tuple
        for sl_ind in slice_index_generator(end, step):  # sl_ind: type == tuple(tuple)
            result.append((start, *sl_ind))
        result.append((start, end))
    return result  # list(tuple(tuple))


def slice_array(graph: np.array, slices: list) -> list:
    mem = {}  # memoisation
    for slice_set in slices:
        for slice_ in slice_set:
            # only calculate new value if it hasn't already been calculated
            if slice_ not in mem:
                mem.update({slice_: graph[np.ix_(slice_, slice_)]})

    return mem


def map_gifts(allocations: list) -> list:
    mapping = [-1] * sum(
        [len(group) for group in allocations]
    )  # index gives gift to value
    for group in allocations:
        for i in range(len(group) - 1):
            mapping[group[i]] = group[i + 1]
        mapping[group[-1]] = group[0]  # edge case
    return mapping


def map_to_people(mapping: list, people: list, people_index: list):
    d = {}
    for index, recip_index in enumerate(mapping):
        person_name = people_index[index]
        d.update(
            {
                person_name: {
                    "email": people[person_name]["email"],
                    "recipient": people_index[recip_index],
                }
            }
        )
    return d


if __name__ == "__main__":
    people = config.people

    graph, people_index = config_parser.get_graph(people)

    allocation = allocate(graph, config.min_grouping)  # TODO add this to config

    # print(allocation)

    mapping = map_gifts(allocation)

    # print(mapping)

    person_mapping = map_to_people(mapping, people, people_index)

    print(person_mapping)

    emailsvc.email_people(person_mapping)
