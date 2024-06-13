#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def total_distance(tour, cities):
    N = len(tour)
    return sum(distance(cities[tour[i]], cities[tour[(i + 1) % N]]) for i in range(N))

def mutate(tour):
    new_tour = tour.copy()
    i, j = sorted(random.sample(range(len(tour)), 2))
    new_tour[i:j+1] = reversed(new_tour[i:j+1])
    return new_tour

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

def initialize_population(cities, population_size):
    return [random.sample(range(len(cities)), len(cities)) for _ in range(population_size)]

def solve(cities):
    population_size = 100
    num_generations = 1000
    num_elites = 10
    mutation_rate = 0.1
    
    population = initialize_population(cities, population_size)
    
    for generation in range(num_generations):
        population = sorted(population, key=lambda tour: total_distance(tour, cities))
        new_population = population[:num_elites]
        
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:50], 2)
            child = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)
        
        population = new_population

    best_tour = min(population, key=lambda tour: total_distance(tour, cities))
    return best_tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = solve(cities)
    print_tour(tour)
