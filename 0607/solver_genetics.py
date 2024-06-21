#!/usr/bin/env python3

import sys
import math
import random
from copy import deepcopy

from common import print_tour, read_input

# Distance Memoization dictionary
distance_cache = {}

def distance(city1, city2):
    key = tuple(sorted((city1, city2)))
    if key not in distance_cache:
        distance_cache[key] = math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
    return distance_cache[key]

def total_distance(tour, cities):
    N = len(tour)
    return sum(distance(cities[tour[i]], cities[tour[(i + 1) % N]] ) for i in range(N))

def mutate(tour, cities):
    return two_opt(deepcopy(tour), cities)

def crossover(tour1, tour2):
    N = len(tour1)
    i, j = sorted(random.sample(range(N), 2))
    
    child = [-1] * N
    child[i:j+1] = tour1[i:j+1]
    
    position = (j + 1) % N
    for city in tour2:
        if city not in child:
            child[position] = city
            position = (position + 1) % N

    return child

def two_opt(tour, cities):
    N = len(tour)
    while True:
        improved = False
        for i in range(N):
            for j in range(i + 2, N):
                if j - i == 1:
                    continue
                # Original distances
                d1 = distance(cities[tour[i]], cities[tour[(i + 1) % N]])
                d2 = distance(cities[tour[j]], cities[tour[(j + 1) % N]])
                # New distances after swap
                d3 = distance(cities[tour[i]], cities[tour[j]])
                d4 = distance(cities[tour[(i + 1) % N]], cities[tour[(j + 1) % N]])
                if d1 + d2 > d3 + d4:
                    tour[i+1:j+1] = reversed(tour[i+1:j+1])
                    improved = True
        if not improved:
            break
    return tour

def initialize_population(cities, population_size):
    return [random.sample(range(len(cities)), len(cities)) for _ in range(population_size)]

def tournament_selection(population, cities, k=5):
    selected = random.sample(population, k)
    selected = sorted(selected, key=lambda tour: total_distance(tour, cities))
    return selected[0]

def solve(cities):
    population_size = 10
    num_generations = 1000
    num_elites = 10
    mutation_rate = 1.0
    
    population = initialize_population(cities, population_size)
    
    for generation in range(num_generations):
        population = sorted(population, key=lambda tour: total_distance(tour, cities))
        new_population = deepcopy(population[:num_elites])
        
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, cities)
            parent2 = tournament_selection(population, cities)
            child = crossover(deepcopy(parent1), deepcopy(parent2))
            if random.random() < mutation_rate:
                child = mutate(child, cities)
            new_population.append(child)
        
        population = new_population
        
        # Print the total distance of the best tour in the current generation
        best_tour = min(population, key=lambda tour: total_distance(tour, cities))
        print(f'Generation {generation + 1}: Total Distance = {total_distance(best_tour, cities)}')
    
    best_tour = min(population, key=lambda tour: total_distance(tour, cities))
    return best_tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = solve(cities)
    print_tour(tour)
