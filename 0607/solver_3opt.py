#!/usr/bin/env python3

import sys
import math
import random
from common import print_tour, read_input

# Distance Memoization dictionary
distance_cache = {}

def distance(city1, city2):
    key = tuple(sorted((city1, city2)))
    if key not in distance_cache:
        distance_cache[key] = (city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2
    return distance_cache[key]

def total_distance(tour, cities):
    N = len(tour)
    return sum(distance(cities[tour[i]], cities[tour[(i + 1) % N]]) for i in range(N))

def solve(cities):
    N = len(cities)
    tour = list(range(N))
    random.shuffle(tour)
    tour = two_opt(tour, cities)
    return three_opt(tour, cities)

def two_opt(tour, cities):
    def reverse_segment_if_better(tour, i, j):
        """If reversing tour[i:j] would make the tour shorter, then do it."""
        # Given tour [...A-B...C-D...], consider reversing B...C to get [...A-C...B-D...]
        A, B, C, D = tour[i], tour[(i + 1) % N], tour[j], tour[(j + 1) % N]
        d0 = distance(cities[A], cities[B]) + distance(cities[C], cities[D])
        d1 = distance(cities[A], cities[C]) + distance(cities[B], cities[D])
        if d0 > d1:
            tour[i+1:j+1] = reversed(tour[i+1:j+1])
            return True
        return False

    N = len(tour)
    while True:
        improved = False
        for i in range(N):
            for j in range(i + 2, N):
                if j - i == 1:
                    continue
                if reverse_segment_if_better(tour, i, j):
                    improved = True
        if not improved:
            break
    return tour

def three_opt(tour, cities, num_attempts=100000):
    def reverse_segment_if_better(tour, i, j, k):
        """Reverses the tour segment between i and j, j and k, and i and k if it improves the tour."""
        a, b, c, d, e, f = tour[i], tour[i+1], tour[j], tour[j+1], tour[k], tour[(k+1) % len(tour)]
        d0 = distance(cities[a], cities[b]) + distance(cities[c], cities[d]) + distance(cities[e], cities[f])
        d1 = distance(cities[a], cities[c]) + distance(cities[b], cities[d]) + distance(cities[e], cities[f])
        d2 = distance(cities[a], cities[b]) + distance(cities[c], cities[e]) + distance(cities[d], cities[f])
        d3 = distance(cities[a], cities[d]) + distance(cities[e], cities[b]) + distance(cities[c], cities[f])
        d4 = distance(cities[a], cities[c]) + distance(cities[d], cities[e]) + distance(cities[b], cities[f])
        d5 = distance(cities[a], cities[d]) + distance(cities[e], cities[c]) + distance(cities[b], cities[f])
        
        if d0 > d1:
            tour[i+1:j+1] = reversed(tour[i+1:j+1])
            return True
        elif d0 > d2:
            tour[j+1:k+1] = reversed(tour[j+1:k+1])
            return True
        elif d0 > d3:
            tour[i+1:k+1] = reversed(tour[i+1:k+1])
            return True
        elif d0 > d4:
            tour[i+1:j+1], tour[j+1:k+1] = reversed(tour[i+1:j+1]), reversed(tour[j+1:k+1])
            return True
        elif d0 > d5:
            tour[i+1:k+1] = reversed(tour[i+1:k+1])
            return True
        return False

    N = len(tour)
    attempts = 0
    while attempts < num_attempts:
        improved = False
        i, j, k = sorted(random.sample(range(N), 3))
        if reverse_segment_if_better(tour, i, j, k):
            improved = True
            attempts = 0
        else:
            attempts += 1
    return tour

def main():
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = list(range(len(cities)))
    random.shuffle(tour)
    print(f'Initial total distance: {total_distance(tour, cities)}')
    tour = three_opt(tour, cities)
    print(f'Optimized total distance: {total_distance(tour, cities)}')
    print_tour(tour)

if __name__ == '__main__':
    main()
