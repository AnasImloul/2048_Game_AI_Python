from random import choice, randint

def empty(grid):
    empty_slots = []
    for slot, value in enumerate(grid):
        if value == 0:
            empty_slots.append(slot)
    return empty_slots

def random_add(grid, value = 2):

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

            if grid[rows * row + col] == 0:
                blocked = False
                continue

            k = row
            merge = True

            while k > 0:

                current = grid[col + rows * k]
                previous = grid[col + rows * (k - 1)]

                if previous == 0:
                    grid[col + rows * (k - 1)], grid[col + rows * k] = grid[col + rows * k], grid[col + rows * (k - 1)]
                    blocked = False

                if merge and previous == current:
                    grid[col + rows * (k - 1)] += current

                    score += current << 1

                    grid[col + rows * k] = 0

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

            if grid[rows * row + col] == 0:
                blocked = False
                continue

            k = row
            merge = True

            while k + 1 < rows:

                current = grid[col + rows * k]
                previous = grid[col + rows * (k + 1)]

                if previous == 0:
                    grid[col + rows * (k + 1)], grid[col + rows * k] = grid[col + rows * k], grid[col + rows * (k + 1)]
                    blocked = False

                if merge and previous == current:
                    grid[col + rows * (k + 1)] += current

                    score += current << 1

                    grid[col + rows * k] = 0

                    merged += 1

                    blocked = False

                    merge = False

                k += 1

    return grid, score, blocked, merged

def right(grid, rows, columns):

    score = 0
    merged = 0

    blocked = True

    for row in range(columns):

        for col in range(rows - 1, -1, -1):

            if grid[rows * row + col] == 0:
                blocked = False
                continue

            k = col

            merge = True

            while k + 1 < columns:

                current = grid[k + rows * row]
                previous = grid[k + 1 + rows * row]

                if previous == 0:
                    grid[rows * row + k + 1], grid[rows * row + k] = grid[rows * row + k], grid[rows * row + k + 1]
                    blocked = False

                if merge and previous == current:
                    grid[k + 1 + rows * row] += current

                    score += current << 1
                    grid[rows * row + k] = 0

                    merged += 1
                    blocked = False

                    merge = False


                k += 1

    return grid, score, blocked, merged

def left(grid,rows, columns):

    score = 0

    merged = 0

    blocked = True

    for row in range(columns):

        for col in range(rows):

            if grid[rows * row + col] == 0:
                blocked = False
                continue

            k = col

            merge = True

            while k > 0:

                current = grid[k + rows * row]
                previous = grid[k - 1 + rows * row]

                if previous == 0:
                    grid[rows * row + k - 1], grid[rows * row + k] = grid[rows * row + k], grid[rows * row + k - 1]
                    blocked = False

                if merge and previous == current:
                    grid[k - 1 + rows * row] += current

                    score += current << 1

                    grid[rows * row + k] = 0

                    merged += 1

                    blocked = False

                    merge = False

                k -= 1

    return grid, score, blocked, merged

def __maxSearch__(grid, rows, columns, moves, depth=6):

    score = 0, 0, '0' * depth

    list = []
    if depth == 1:

        max_score = -1,-1,'0'

        for index,move in enumerate(moves):
            copy = grid.copy()
            copy, score, blocked, merged = move(copy, rows, columns)

            max_score = max(max_score, (merged, score, str(index)))

        return max_score

    possibles = []
    for index,move in enumerate(moves):

        copy = grid.copy()

        copy, score, blocked, merged = move(copy, rows, columns)

        if not blocked:
            possibles.append(move)

            copy = random_add(copy)

            way = __maxSearch__(copy, rows, columns, moves, depth-1)

            way = merged + way[0], score + way[1], str(index) + way[2]

            list.append(way)

    if list:
        return max(list, key=lambda x: x[:2])

    return 0, 0, str(randint(0, len(moves) - 1)) + "0" * (depth - 1)



if __name__ == '__main__':
    from time import perf_counter

    grid = [0,0,0,0,
            0,0,0,0,
            0,0,0,0,
            0,0,0,0]

    start = perf_counter()

    __maxSearch__(grid,4,4,[up,down,right,left], depth=8)

    print(perf_counter() - start)