import random
import Import


def binary_ordered_crossover(parent1, parent2):
    """
    Perform ordered crossover on binary representations.
    """
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size

    # Copy a slice from the first parent
    child[start : end + 1] = parent1[start : end + 1]

    # Fill the remaining positions with genes from the second parent
    for i in range(size):
        if child[i] is None:
            child[i] = parent2[i]
    return child


def invert_binary_matrix_range(matrix: list[list], start: int, end: int):
    """
    Inverts a specified range of rows in a 2D binary matrix.

    :param matrix: 2D list of binary values (0s and 1s).
    :param start: Starting index of the range to invert (inclusive).
    :param end: Ending index of the range to invert (inclusive).
    :return: The matrix with the specified range inverted.
    """
    # Ensure the range is within the bounds of the matrix
    start = max(0, start)
    end = min(end, len(matrix) - 1)

    # Invert each element in the specified range
    for i in range(start, end + 1):
        matrix[i] = [1 - bit for bit in matrix[i]]

    return matrix


def binary_inversion_mutation(individual: list[list]):
    """
    Perform inversion mutation on a binary individual.
    Randomly flips a selected range of genes.
    [[1,1,0,0,1],[1,0,0,1,0]]
    """
    start, end = sorted(random.sample(range(len(individual)), 2))
    invert_binary_matrix_range(individual, start, end)
    return individual


class KNP:
    def __init__(
        self, item_matrix, max_weight, pop_size, tour_size, generations
    ) -> None:
        if len(item_matrix) == 0:
            raise ValueError("matrix in not valid")

        self.item_matrix = item_matrix
        self.city_count = len(item_matrix)
        self.each_city_item_count = len(item_matrix[0])
        self.max_weight = max_weight
        self.pop_size = pop_size
        self.tour_size = tour_size
        self.generations = generations

    def initialize_population(self) -> None:
        """
        Initialize the population with random solutions.
        Each solution is a binary list representing whether to pick an item from a city or not.
        [[[0, 1], [1, 0], [0, 1]],
        [[1, 0], [1, 1], [0, 0]],
        [[1, 1], [0, 0], [0, 1]],
        [[1, 0], [0, 0], [1, 1]],
        [[1, 1], [1, 0], [1, 0]]]
        """
        self.population = [
            [
                [random.randint(0, 1) for _ in range(self.each_city_item_count)]
                for _ in range(self.city_count)
            ]
            for _ in range(self.pop_size)
        ]

    def set_population(self, population) -> None:
        self.population = population

    def tournament_selection(self, fitness) -> int:
        """
        Selects a single individual using tournament selection.
        """
        selected = random.sample(list(zip(self.population, fitness)), self.tour_size)
        return max(selected, key=lambda x: x[1])[0]

    def fitness_function(self, individual: list[tuple]):
        """
        Calculate the fitness of an individual. Higher fitness is better.
        Fitness is the total profit of the items chosen, considering the weight constraint.
        """
        total_weight = 0
        total_profit = 0
        for city_index, items in enumerate(individual):
            for item_index, take_item in enumerate(items):
                if take_item:
                    """
                    Take items from current city, which have higher profit with lighter weight.
                    """
                    # print(self.item_matrix[city_index])
                    item_weight, item_profit = self.item_matrix[city_index][item_index][
                        2:
                    ]
                    if total_weight + item_weight <= self.max_weight:
                        total_weight += item_weight
                        total_profit += item_profit
                    else:
                        # Update individual if the item cannot be taken due to weight limit
                        individual[city_index][item_index] = 0
                # print(total_weight)
        return total_profit, total_weight

    def genetic_algorithm(self):
        """
        Modified Genetic Algorithm for the knapsack problem with cities.
        """
        self.initialize_population()
        best_solution = None
        best_fitness = 0
        best_weight = 0

        for generation in range(self.generations):
            # print(generation)
            new_population = []
            fitness_values = [self.fitness_function(ind)[0] for ind in self.population]

            for _ in range(self.pop_size):
                # Selection
                parent1 = self.tournament_selection(fitness_values)
                parent2 = self.tournament_selection(fitness_values)

                # Crossover
                child = binary_ordered_crossover(parent1, parent2)

                # Mutation
                child = binary_inversion_mutation(child)

                new_population.append(child)

            self.set_population(new_population)

            # Check for new best solution
            for ind in self.population:
                fitness, weight = self.fitness_function(ind)
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_weight = weight
                    # best_solution = ind

        #  pprint.pprint(self.population)

        return new_population, best_fitness, best_weight


ITEM_MATRIX = Import.items_array

ITEM_MATRIX = [
    [(t[0], t[3], t[2], t[1]) for t in inner_list] for inner_list in ITEM_MATRIX
]

"""
[
    [(1, 1, 30, 20), (1, 2, 40, 20), (1, 3, 10, 30)],
    [(2, 1, 40, 30), (2, 2, 40, 20), (2, 3, 30, 20)],
    [(3, 1, 30, 40), (3, 2, 60, 20), (3, 3, 40, 10)],
    [(4, 1, 50, 50), (4, 2, 90, 20), (4, 3, 50, 30)],
    [(5, 1, 50, 70), (5, 2, 40, 80), (5, 3, 30, 90)],
]
"""

MAX_WEIGHT = Import.capacity
knp = KNP(
    item_matrix=ITEM_MATRIX,
    max_weight=MAX_WEIGHT,
    pop_size=20,
    tour_size=10,
    generations=1000,
)
best_solution, best_fitness, best_weight = knp.genetic_algorithm()

# Add 0 for first city to solution, which has no items.
best_solution = [[[0] * len(ITEM_MATRIX[0])] + sublist for sublist in best_solution]

"""
#print(len(best_solution[0]))
print(
    f"Best Solution: {best_solution}, Total Profit: {best_fitness}, Total Weight: {best_weight}"
)
num_elements = len(best_solution[0])
print("Number of elements in best_solution:", num_elements)
"""
