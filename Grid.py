from functions import digit, max_digits, up, down, right, left, random_add,  __maxSearch__



class Grid:

    def __init__(self, rows, columns):

        self.rows, self.columns = rows, columns

        self.grid = [0 for i in range(self.rows * self.columns)]

        self.grid = random_add(self.grid, 2)
        self.grid = random_add(self.grid, 2)

        self.score = 0

        self.moves = [up, down, right, left]

        self.merged = 0

        self.blocked = False


    def random_add(self, value = 2):
        random_add(self.grid, value)


    def up(self):
        self.grid, score, blocked, merged = up(self)

        self.score += score
        self.blocked = blocked
        self.merged += merged

    def down(self):
        self.grid, score, blocked, merged = up(self)

        self.score += score
        self.blocked = blocked
        self.merged += merged

    def left(self):
        self.grid, score, blocked, merged = up(self)

        self.score += score
        self.blocked = blocked
        self.merged += merged

    def right(self):
        self.grid, score, blocked, merged = up(self)

        self.score += score
        self.blocked = blocked
        self.merged += merged

    def next_move(self, depth = 6):

        best_move = int(__maxSearch__(self.grid, self.rows, self.columns, self.moves, depth)[2][0])

        return self.moves[best_move]

    def play(self, rounds, depth = 6,show = False):
        for round in range(rounds):
            if show:
                print(self)

            next = self.next_move(depth)
            self.grid, score, blocked, merged = next(self.grid, self.rows, self.columns)

            self.score += score
            self.blocked = blocked
            self.merged += merged

            if self.blocked:
                print(f"Reached a total score of {self.score} after playing {round} rounds.")
                break

            self.random_add()

    def __str__(self):
        s=""
        digits = max_digits(self.grid)
        for i,value in enumerate(self.grid):

            s += str(value) + (" "*(2 + digits - digit(value)) if ((i==0 and self.columns != 1) or (i+1)%self.columns) else "\n")

        return s + f"Score : {self.score}\n"

    def __getitem__(self, item):
        return self.grid[item]

    def __setitem__(self, key, item):
        self.grid[key] = item

    def copy(self):
        copy = Grid(self.rows, self.columns)

        copy.grid = self.grid.copy()
        copy.empty_slots = self.empty_slots.copy()

        copy.score = self.score

        copy.merged = self.merged

        copy.first_move = self.first_move

        return copy
