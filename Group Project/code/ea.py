"""
Description: This file is the implement of the Evolution Algorithm.
Author: Yushan Kuerban
Date: 25/10/2003
"""
# Python packages
import math
import random
import time


# Implement of ordered crossover
def ordered_crossover(parent1, parent2):
    # Choose two random positions
    start = random.randint(0, len(parent1) - 1)
    end = random.randint(start, len(parent1) - 1)

    # Create two empty children
    child1 = [-1] * len(parent1)
    child2 = [-1] * len(parent2)

    # Copy the selected segment from parent 1 to child 1
    for i in range(start, end + 1):
        child1[i] = parent1[i]

    # Copy the remaining elements from parent 2 to child 1
    j = 0
    for i in range(len(parent2)):
        if parent2[i] not in child1:
            while child1[j] != -1:
                j += 1
            child1[j] = parent2[i]

    # Copy the selected segment from parent 2 to child 2
    for i in range(start, end + 1):
        child2[i] = parent2[i]

    # Copy the remaining elements from parent 1 to child 2
    j = 0
    for i in range(len(parent1)):
        if parent1[i] not in child2:
            while child2[j] != -1:
                j += 1
            child2[j] = parent1[i]

    return child1, child2


# Implement inversion mutation
def inversion_mutation(C):
    n = len(C)
    # Randomly generate two positions
    i = random.randint(0, n - 1)
    j = random.randint(0, n - 1)
    while i == j:  # If i ==j then re-generate j, until i != j
        j = random.randint(0, n - 1)
    # swap i and j if i > j to make sure i smaller than j.
    if i > j:
        i, j = j, i
    # reverse from small position to bigger position part
    C[i : j + 1] = reversed(C[i : j + 1])
    return C


class EA:
    def __init__(
        self,
        pop_size,
        tour_size,
        D,
    ):
        self.fit = None
        self.population = None
        self.pop_size = pop_size
        self.tour_size = tour_size
        self.crossover_operator = None
        self.mutation_operator = None
        self.MAX_EVALS = 1000
        # D represents to the matrix of cities distances.
        self.D = D
        self.city_count = len(D)
        # Set random seed as microsecond of current time.
        random.seed(round(time.time() * 1000000))

    # Generate a random solution
    def generate_random_solution(self):
        C = list(range(1, self.city_count + 1))  # Create a list which start with 1.
        random.shuffle(C)  # Shuffle it.
        return C

    # Calculate cost of solution C.
    def calculate_cost(self, C):
        cost = 0  # Initialize cost with 0
        for i in range(self.city_count - 1):
            # Calculate the cost, mind the index has to minus 1
            cost += self.D[C[i] - 1][C[i + 1] - 1]
        # Add the last cost, back to the first city from last one.
        cost += self.D[C[self.city_count - 1] - 1][C[0] - 1]
        return cost

    # Implement of tournament selection
    def tournament_selection(self):
        best = None  # Initialize the best individual.
        best_fit = math.inf  # Initialize the best fitness with max infinite
        for i in range(self.tour_size):  # Randomly select k individuals
            idx = random.randint(0, len(self.population) - 1)  # Generate random index
            sol = self.population[idx]  # Get the solution of current population
            sol_fit = self.fit[idx]  # Get the fitness of current population
            if sol_fit < best_fit:  # If fitness lower than the best one(less distance)
                # Update it.
                best = sol
                best_fit = sol_fit
        return best

    # Implement the worst replacement.
    def worst_replacement(self, sol, sol_fit):
        # Find the worst individual index(highest fitness)
        worst_idx = self.fit.index(max(self.fit))
        # Replace it with latest solution and fitness
        self.population[worst_idx] = sol
        self.fit[worst_idx] = sol_fit

    def update_operators(self, cross, mut):
        self.crossover_operator = cross
        self.mutation_operator = mut

    def run(self):
        if self.mutation_operator is None:
            self.mutation_operator = inversion_mutation
        if self.crossover_operator is None:
            self.crossover_operator = ordered_crossover
        # Generate init population
        self.population = [
            self.generate_random_solution() for _ in range(self.pop_size)
        ]

        # Calculate fitness of init population
        self.fit = [self.calculate_cost(sol) for sol in self.population]

        # Record evaluate times
        evals = 0

        # Init the best solution and best fitness
        best_sol = None
        best_fit = math.inf
        data = []
        # Start population selection, crossover and mutation operations.
        while evals < self.MAX_EVALS:
            # Use tournament_selection select two parents.
            a = self.tournament_selection()
            b = self.tournament_selection()
            #print("!")
            # Use crossover to generate offspring
            c, d = self.crossover_operator(a, b)
            #print("?")
            # Use mutation generate new solutions.
            e = self.mutation_operator(c)
            f = self.mutation_operator(d)

            # Calculate new solution fitness.
            e_fit = self.calculate_cost(e)
            f_fit = self.calculate_cost(f)

            # Use worst_replacement to replace the worst individual with new offsprings.
            if e_fit < f_fit:
                self.worst_replacement(e, e_fit)
                if e_fit < best_fit:
                    best_sol = e
                    best_fit = e_fit
            else:
                self.worst_replacement(f, f_fit)
                if f_fit < best_fit:
                    best_sol = f
                    best_fit = f_fit

            # Update evaluate times.
            evals += 1
            data.append(best_fit)

        # Print best solution and best fitness.
        #print("Best solution:", best_sol)
        #print("Best fitness:", best_fit)
        #print(self.population)
        return self.population
