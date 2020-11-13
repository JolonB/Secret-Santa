import numpy as np
from circular_list import deep_is_circular


def hamiltonian(graph: np.array, circular_dup=True) -> list:
    solutions = []
    for i in range(len(graph)):
        new_solutions = ham(graph, [i])
        if new_solutions:
            solutions.extend(new_solutions)

    if not circular_dup:
        solutions = deep_is_circular(solutions)

    return solutions


def ham(graph: np.array, current: list) -> list:
    # return the list if all values have been added, and there is a connection between the first and last values
    if len(current) == len(graph) and graph[current[-1]][current[0]]:
        return [current]

    solutions = []

    # get the previous node
    last = current[-1]
    # graph[i] is a list of possible neighbours of the last added element
    for neigh in range(len(graph)):
        # skip if value already in `current` or if `last` and `neigh` are not connected
        if not graph[last][neigh] or neigh in current:
            continue
        # add new solutions to list of current solutions
        new_solutions = ham(graph, current + [neigh])
        if new_solutions:
            solutions.extend(new_solutions)
    return solutions


if __name__ == "__main__":
    g = np.array([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]])
    print(f"Sample graph is:\n{g}", end="\n\n")
    print(f"Full results:\n{hamiltonian(g)}", end="\n\n")
    print(
        f"Results with circular duplicates removed:\n{hamiltonian(g, False)}",
        end="\n\n",
    )
