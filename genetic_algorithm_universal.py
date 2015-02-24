"""
Chromosome Representation GA
https://en.wikipedia.org/wiki/Genetic_algorithm#Chromosome_representation

Genetic algorithms belong to the larger class of evolutionary
algorithms (EA), which generate solutions to optimization
problems using techniques inspired by natural evolution,
such as inheritance, mutation, selection, and crossover.
"""

from random import randint, random
from math import ceil, log, pi
from copy import copy

class CylinderPhenotype:
    """Individual (phenotype, creature)
    """

    def __init__(self, genotype, sizes=[5,5]):

        # Genotype (properties, chromosomes)
        self.genotype   = genotype
        self.sizes      = sizes
        self.diameter   = None
        self.height     = None
        self.fitness    = None
        self.constraint = None

    def __str__(self):
        return ''.join([
            "Gen: ", self.genotype[:self.sizes[0]], ".", self.genotype[self.sizes[0]:],
            " H: ", str(self.height),
            "\tD: ", str(self.diameter),
            "\tSurface: ", str(self.fitness),
            "\tVolume: ", str(self.constraint)
        ])

    def calculate_decimals(self):
        [self.diameter, self.height] = property_values_from_genotype(self.genotype, self.sizes)
        return [self.diameter, self.height]

    def evaluate(self):
        # surface
        self.fitness    = pi*self.diameter**2/2 + pi*self.diameter*self.height
        # volume
        self.constraint = pi*self.diameter**2*self.height/4 >= 300
        return [self.fitness, self.constraint]


"""Genetic algorithm methodologies
"""
def initialize_population(size, properties):

    sizes_properties = properties.values()
    length_genotype  = sum(sizes_properties)
    population = []
    for _ in range(size):
        population.append(CylinderPhenotype(random_genotype(length_genotype)))
        population[-1].calculate_decimals()
        population[-1].evaluate()

    return population

def next_generation(population):

    next_generation = select_phenotypes(population)
    next_generation = mutate(next_generation)
    next_generation = crossover(next_generation)

    # Evaluate creatures
    for phenotype in next_generation:
        phenotype.calculate_decimals()
        phenotype.evaluate()

    return next_generation

def select_phenotypes(population):
    return get_rank_based_selection(population, greatest_fitness_first=False)

def get_rank_based_selection(population, size=None, greatest_fitness_first=True):
    """Stochastic universal sampling
    """

    # list, sorted by rank and filtered by constraint
    sorted_population = sorted( [creature for creature in population if creature.constraint],
                                key=lambda ind: ind.fitness,
                                reverse=greatest_fitness_first )

    # List with boundaries of interval for rank probability
    probability_interval = get_probability_interval(len(sorted_population))

    selection = []
    for _ in range(size if size else len(population)):
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

def mutate(population, probability=0.1):

    mutants = (creature for creature in population if random() <= probability)
    for phenotype in mutants:
        phenotype.genotype = random_genotype_mutation(phenotype.genotype)

    return population

def random_genotype_mutation(genotype, probability=0.1):
    """
    Inverts each bit of genotype with
    probability p.
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


"""Encoding and Decoding
"""
def random_genotype(length=10):
    return ''.join([str(randint(0,1)) for _ in range(length)])

def length_binary_encoded_interval(min=0, max=10, step=1):
    return ceil(log((abs(max-min))/step, 2))

def binary_to_real(bin_string, min=0, step=1):
    base = 1
    num = 0
    for i in bin_string[::-1]:
        num += base*int(i)
        base *= 2
    return (num-min)*step

def property_values_from_genotype(genotype, sizes=[5,5]):
    """
    Split binary representation (genotype) according to size
    of each property, and compute decimal value.
    """
    property_values = []

    s0 = 0
    for s1 in sizes:
        property_values.append(
            binary_to_real(genotype[s0:s0+s1])
        )
        s0 += s1

    return property_values


def main():

    SIZE_POPULATION = 30
    NUMBER_GENERATIONS = 5
    PROPERTIES = {
        'Height': length_binary_encoded_interval(max=31),
        'Diameter': length_binary_encoded_interval(max=31)
    }

    population = initialize_population(size=SIZE_POPULATION, properties=PROPERTIES)

    for _ in range(NUMBER_GENERATIONS):
        population = next_generation(population)

    # show population
    for phenotype in population:
        phenotype.calculate_decimals()
        phenotype.evaluate()
        print(phenotype)

if __name__ == '__main__':
    main()
