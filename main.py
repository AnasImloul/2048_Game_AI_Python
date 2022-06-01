from Grid import Grid
from time import perf_counter_ns

grid = Grid(3,3)


for i in range(2):
    grid.random_add()


start = perf_counter_ns()

grid.play(rounds=10000, depth=8, show=True)

print((perf_counter_ns() - start)/1_000_000)