def is_circular(main_index: int, to_check: list):
    def to_string(l: list):
        return " ".join(str(x) for x in l)

    keep_indices = list(range(main_index + 1))
    main = to_check[main_index] * 2
    main_str = to_string(main)
    for i in range(main_index, len(to_check)):
        if (
            len(to_check[main_index]) != len(to_check[i])
            or to_string(to_check[i]) not in main_str
        ):
            keep_indices.append(i)

    return [to_check[i] for i in keep_indices]


def deep_is_circular(solutions):
    i = 0
    while i < len(solutions):
        solutions = is_circular(i, solutions)
        i += 1

    return solutions
