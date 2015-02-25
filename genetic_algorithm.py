"""
Determine cylinder with minimal surface and
volume of at least 300 units.
===========================================

Lecture: Comuptatianal Intelligence - ZHAW
Lecturer: Dr. Carsten Franke
Topic: Einkriterielle Evoulutionaere Algorithmen

Author: Michael Kressibucher


Requirements:
-------------
Height of Cylinder h:   0 <= h <= 31
Diameter of Cylinder d: 0 <= d <= 31

Volume v:  pi*d^2*h/4 >= 300
Surface s: pi*d^2/2 + pi*d*h

-> By a genetic algorithm, diameter and height
   have to be determined, such that the surface
   of the cylinder is minimal.


Genotype:
Encoded properties h and d build genotype
length of genotype: ceil( log2(31) ) + ceil( log2(31) ) = 5 + 5

Champions:
Best creature of each population, over several
populaitons.

Compare fitness of populations for mutation probabilities
0.005, 0.01, 0.02, 0.1, 0.2.
-> mutation rate of 0.01 seeems to be most reliable for
   those 100 generations we train.

"""

from random import randint, random
from math import log, pi, floor
from copy import copy

class CylinderPhenotype:
    """Individual (phenotype, creature)
    """

    def __init__(self, genotype):

        # Genotype (properties, chromosomes)
        self.genotype   = genotype
        self.diameter   = None
        self.height     = None
        self.fitness    = None
        self.constraint = None

    def __str__(self):
        return ''.join([
            "Gen: ", self.genotype[:5], ".", self.genotype[5:],
            " H: ", str(self.height),
            "\tD: ", str(self.diameter),
            "\tSurface: ", str(self.fitness),
            "\tVolume: ", str(self.constraint)
        ])

    def calculate_decimals(self):
        self.diameter = binary_to_real(self.genotype[:5])
        self.height   = binary_to_real(self.genotype[5:])
        return [self.diameter, self.height]

    def evaluate(self):
        # surface
        self.fitness    = pi*self.diameter**2/2 + pi*self.diameter*self.height
        # volume greater than 300
        self.constraint = pi*self.diameter**2*self.height/4 >= 300
        return [self.fitness, self.constraint]


"""Genetic algorithm methodologies
"""
def initialize_population(size):

    population = []
    for _ in range(size):
        population.append(CylinderPhenotype(
            # Random Genotype of length 10
            ''.join([str(randint(0,1)) for _ in range(10)])
        ))

        population[-1].calculate_decimals()
        population[-1].evaluate()

    return population

def next_generation(population, mutation_probability=0.01):

    next_generation = select_phenotypes(population)
    next_generation = mutate(next_generation, mutation_probability)
    next_generation = crossover(next_generation)

    # Evaluate creatures
    for phenotype in next_generation:
        phenotype.calculate_decimals()
        phenotype.evaluate()

    return next_generation

def select_phenotypes(population):
    """
    Rank based selection (Stochastic universal sampling)
    """

    # list, sorted by rank and filtered by constraint
    sorted_population = sorted( [creature for creature in population if creature.constraint],
                                key=lambda ind: ind.fitness,
                                reverse=False )

    # List with boundaries of interval for rank probability
    probability_interval = get_probability_interval(len(sorted_population))

    selection = []
    for _ in range(len(population)):
        rand = random()
        for i, sub_interval in enumerate(probability_interval):
            if rand <= sub_interval:
                break
        # selected individuals are copied into selection
        # otherwise several items in selection would point
        # to the same individual.
        selection.append(copy(sorted_population[i]))

    return selection

def get_probability_interval(max_rank):
    """
    Create list with probability of ranks, interval
    of rank 1 is first in list
    """ 
    sum_ranks = max_rank*(max_rank+1)/2
    interval = [float(max_rank)/sum_ranks]
    for rank in range(max_rank-1,0,-1):
        interval.append( interval[-1] + float(rank)/sum_ranks )

    return interval

def mutate(population, probability):
    for phenotype in population:
        phenotype.genotype = random_genotype_mutation(phenotype.genotype, probability)
    return population

def random_genotype_mutation(genotype, probability):
    """
    Inverts each bit of genotype with probability p.
    """
    mutation = []
    for bit in genotype:
        if random() <= probability:
            bit = '0' if bit == '1' else '1'
        mutation.append(bit)

    return ''.join(mutation)

def crossover(population):
    """
    Split population in two groups, and mate individuals
    from the first group with individuals from the
    second group, giving two offsprings. They mate only
    with probability p. Offsprings will replace their
    parents.
    """
    return population

def singel_point_recombine(gen1, gen2):
    point = randint(0,min(len(gen1),len(gen2)))
    return [gen1[:point]+gen2[point:], gen1[point:]+gen2[:point]]

def get_champion(population):

    fitness  = None
    champion = None
    for phenotype in population:
        if phenotype.constraint and (not fitness or phenotype.fitness < fitness):
            fitness  = phenotype.fitness
            champion = phenotype

    return copy(champion)


"""Encoding and Decoding
"""
def binary_to_real(bin_string, min=0, step=1):
    base = 1
    num = 0
    for i in bin_string[::-1]:
        num += base*int(i)
        base *= 2
    return num


"""Plot
"""
def create_summary(population):
    """
    Plot fitness of the best individual of each generation
    """
    plot(range(len(population)),[phenotype.fitness for phenotype in population])
    superchamp = get_champion(population)
    print(''.join([
        'Superchamp Diameter: ', str(superchamp.diameter),
        ' Height: ', str(superchamp.height),
        ' Surface: ', str(superchamp.fitness)
    ]))    

def plot(x=[], y=[], size_x=100, size_y=50):
    """
    x, y list of values on x- and y-axis.
    plot those values within canvas size.
    """
    # for simplicity, x and y must contain the same number
    # of elements and must be positive.
    if len(x) != len(y) or min(x) < 0 or min(y) < 0:
        print('len(x) != len(y) or some elements are negative')

    # Scale points such that they fit on canvas
    scale_x = float(size_x-1)/max(x) if x and max(x) != 0 else size_x
    scale_y = float(size_y-1)/max(y) if y and max(y) != 0 else size_y
    x_scaled = [int(i * scale_x) for i in x]
    y_scaled = [int(i * scale_y) for i in y]

    # Create empty canvas
    canvas = [[' ' for _ in range(size_x)] for _ in range(size_y)]

    # Add scaled points to canvas
    for ix, iy in zip(x_scaled, y_scaled):
        canvas[size_y-iy+1][ix] = '*'

    # Print rows of canvas
    for row in [''.join(row) for row in canvas]:
        print(row)

    # Print scale
    print(''.join([ 'Max x: ', str(max(x)), ' Max y: ', str(max(y)), '\n' ]))


def main():

    SIZE_POPULATION      = 30
    NUMBER_GENERATIONS   = 100
    MUTATION_PROBABILITY = 0.01

    population = initialize_population(size=SIZE_POPULATION)
    champions  = []

    for _ in range(NUMBER_GENERATIONS):
        population = next_generation(population, mutation_probability=MUTATION_PROBABILITY)
        champions.append(get_champion(population))

    create_summary(champions)


if __name__ == '__main__':
    main()