def remove_circular_duplicates(main_index: int, to_check: list):
    """Remove circular duplicates from a list of solutions.

    For example, given the input:

    `[[1,2,3], [2,3,1], [3,2,1]]`

    the resulting list will be:

    `[[1,2,3], [3,2,1]]`

    because the second solution is a circular duplicate of the first so it is removed.

    Parameters:
        main_index (int): The index of the solution to start checking for
        duplicates. Any solutions that are circular duplicates of solutions
        before this index will not be removed.
        to_check (list): The list of solutions to check for duplicates.

    Returns:
        list: The list of solutions with duplicates removed.
    """

    def to_string(l: list):
        # Convert a list to a string, with elements separated by spaces
        return " ".join(str(x) for x in l)

    # We always want to keep the solutions before and including main_index, so
    # we store those indices now
    keep_indices = list(range(main_index + 1))
    # Duplicate the list stored at `main_index`, i.e. `[1,2] -> [1,2,1,2]`
    main = to_check[main_index] * 2
    # Convert the doubled list to a string, i.e. `"[1,2,1,2]"`
    main_str = to_string(main)

    # Iterate over all solutions after main_index
    for i in range(main_index, len(to_check)):
        # Check that the solution has the same number of points as the main solution
        # and then check that `main_str` does not contain the current solution as a substring
        if (
            len(to_check[main_index]) != len(to_check[i])
            or to_string(to_check[i]) not in main_str
        ):
            keep_indices.append(i)

    # Convert the list of indices to a list of solutions
    return [to_check[i] for i in keep_indices]


def deep_remove_circular_duplicates(solutions):
    i = 0
    # We recheck the length because it is constantly changing
    while i < len(solutions):
        solutions = remove_circular_duplicates(i, solutions)
        # Increment to the next index so we don't check the same solution again
        i += 1

    return solutions
