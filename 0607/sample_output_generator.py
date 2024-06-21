#!/usr/bin/env python3

from common import format_tour, read_input

import solver_greedy
import solver_random
import solver_genetics
import solver_3opt

CHALLENGES = 8


def generate_sample_output():
    for i in range(6, CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        # for solver, name in ((solver_random, 'random'), (solver_greedy, 'greedy'), (solver_genetics, 'genetics')):
        for solver, name in ((solver_3opt, '3opt'), (solver_greedy, 'greedy')):
            tour = solver.solve(cities)
            with open(f'sample/{name}_{i}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')
                print(f'{name}_{i}.csv')


if __name__ == '__main__':
    generate_sample_output()
