from random import choice, randint
from math import log10


def insert(list, value, key=lambda x: x):
    i = len(list) - 1
    list[i] = value

    while i > 0:
        if key(list[i]) > key(list[i - 1]):
            list[i], list[i - 1] = list[i - 1], list[i]

        i -= 1

    return list


def digit(value):
    if value == 0:
        return 1

    if value < 0:
        return 1 + int(1 + log10(value))

    return int(1 + log10(value))


def max_digits(grid):
    digits = 1
    for value in grid:
        if value != 0:
            digits = max(digits, digit(value))
    return digits


def empty(grid):
    empty_slots = []
    for slot, value in enumerate(grid):
        if value == 0:
            empty_slots.append(slot)
    return empty_slots


def random_add(grid, value=2):
    empty_slots = empty(grid)

    if len(empty_slots) == 0:
        return grid

    pos = choice(empty_slots)

    grid[pos] = value

    return grid


def up(grid, rows, columns):
    merged = 0

    score = 0

    blocked = True

    for col in range(columns):
        for row in range(rows):
            if grid[columns * row + col] == 0:
                blocked = False
                continue

            k = row
            merge = True

            while k > 0:

                current = grid[col + columns * k]
                previous = grid[col + columns * (k - 1)]

                if previous == 0:
                    grid[col + columns * (k - 1)], grid[col + columns * k] = grid[col + columns * k], grid[col + columns * (k - 1)]
                    blocked = False

                if merge and previous == current:
                    grid[col + columns * (k - 1)] += current

                    score += current << 1

                    grid[col + columns * k] = 0

                    merged += 1

                    blocked = False

                    merge = False

                k -= 1

    return grid, score, blocked, merged


def down(grid, rows, columns):
    score = 0

    merged = 0

    blocked = True

    for col in range(columns):
        for row in range(rows - 1, -1, -1):

            if grid[columns * row + col] == 0:
                blocked = False
                continue

            k = row
            merge = True

            while k + 1 < rows:

                current = grid[col + columns * k]
                previous = grid[col + columns * (k + 1)]

                if previous == 0:
                    grid[col + columns * (k + 1)], grid[col + columns * k] = grid[col + columns * k], grid[col + columns * (k + 1)]
                    blocked = False

                if merge and previous == current:
                    grid[col + columns * (k + 1)] += current

                    score += current << 1

                    grid[col + columns * k] = 0

                    merged += 1

                    blocked = False

                    merge = False

                k += 1

    return grid, score, blocked, merged


def right(grid, rows, columns):
    score = 0
    merged = 0

    blocked = True

    for row in range(rows):

        for col in range(columns - 1, -1, -1):

            if grid[columns * row + col] == 0:
                blocked = False
                continue

            k = col

            merge = True

            while k + 1 < columns:

                current = grid[k + columns * row]

                previous = grid[k + 1 + columns * row]

                if previous == 0:
                    grid[columns * row + k + 1], grid[columns * row + k] = grid[columns * row + k], grid[columns * row + k + 1]
                    blocked = False

                if merge and previous == current:
                    grid[k + 1 + columns * row] += current

                    score += current << 1
                    grid[columns * row + k] = 0

                    merged += 1
                    blocked = False

                    merge = False

                k += 1

    return grid, score, blocked, merged


def left(grid, rows, columns):
    score = 0

    merged = 0

    blocked = True

    for row in range(rows):

        for col in range(columns):

            if grid[columns * row + col] == 0:
                blocked = False
                continue

            k = col

            merge = True

            while k > 0:

                current = grid[k + columns * row]
                previous = grid[k - 1 + columns * row]

                if previous == 0:
                    grid[columns * row + k - 1], grid[columns * row + k] = grid[columns * row + k], grid[columns * row + k - 1]
                    blocked = False

                if merge and previous == current:
                    grid[k - 1 + columns * row] += current

                    score += current << 1

                    grid[columns * row + k] = 0

                    merged += 1

                    blocked = False

                    merge = False

                k -= 1

    return grid, score, blocked, merged


# TODO at each depth remove the least scoring move
def __maxSearch__(grid, rows, columns, moves, depth=6):
    max_score = -1, -1, '0'
    if depth == 1:

        for index, move in enumerate(moves):
            copy = grid.copy()
            copy, score, blocked, merged = move(copy, rows, columns)

            max_score = max(max_score, (merged, score, str(index)))

        return max_score

    next_states = [(-1,-1,0,0,0)] * 4

    any_move_blocked = False

    for index, move in enumerate(moves):

        copy = grid.copy()

        copy, score, blocked, merged = move(copy, rows, columns)

        any_move_blocked = any_move_blocked | blocked

        next_states = insert(next_states, (merged, score, blocked, copy, index), lambda x: x[:2])

    if not any_move_blocked:
        next_states.pop()

    for state in next_states:
        merged, score, blocked, copy, index = state

        if not blocked:
            copy = random_add(copy)

            way = __maxSearch__(copy, rows, columns, moves, depth - 1)

            way = merged + way[0], score + way[1], str(index) + way[2]

            max_score = max(max_score, way)

    return max_score


if __name__ == '__main__':
    from time import perf_counter

    grid = [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]

    start = perf_counter()

    __maxSearch__(grid, 4, 4, [up, down, right, left], depth=8)

    print(perf_counter() - start)
