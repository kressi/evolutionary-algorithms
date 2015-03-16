from random import randint, random, shuffle
from math import log, pi
from copy import copy
from terminalplot import plot

class CylinderPhenotype:
    """Individual (phenotype, creature)
    """

    def __init__(self, genotype):

        # Genotype (properties, chromosomes)
        self.genotype   = genotype
        self.diameter   = None
        self.height     = None
        self.surface    = None
        self.volume     = None

    def __str__(self):
        return ''.join([
            "Gen: ", self.genotype[:5], ".", self.genotype[5:],
            " H: ", str(self.height),
            "\tD: ", str(self.diameter),
            "\tSurface: ", str(self.surface),
            "\tVolume: ", str(self.volume)
        ])

    def calculate_decimals(self):
        self.diameter = binary_to_real(self.genotype[:5])
        self.height   = binary_to_real(self.genotype[5:])
        return [self.diameter, self.height]

    def evaluate(self):
        # surface
        self.surface    = pi*self.diameter**2/2 + pi*self.diameter*self.height
        # volume greater than 300
        self.volume = pi*self.diameter**2*self.height/4
        return [self.surface, self.volume]


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

    shuffle(population)

    volume_gen  = population[:int(len(population)/2)]
    surface_gen = population[int(len(population)/2):]

    volume_gen  = select_phenotypes(volume_gen, 'volume')
    surface_gen = select_phenotypes(surface_gen, 'surface')
    volume_gen  = mutate(volume_gen, mutation_probability)
    surface_gen = mutate(surface_gen, mutation_probability)
    volume_gen  = crossover(volume_gen)
    surface_gen = crossover(surface_gen)

    next_generation = volume_gen + surface_gen

    # Evaluate creatures
    for phenotype in next_generation:
        phenotype.calculate_decimals()
        phenotype.evaluate()

    return next_generation

def select_phenotypes(population, type):
    """
    Rank based selection (Stochastic universal sampling)
    """

    # list, sorted by rank and filtered by constraint
    if type == 'volume':
        sorted_population = sorted( population,
                                    key=lambda ind: ind.volume,
                                    reverse=True )
    else:
        sorted_population = sorted( population,
                                    key=lambda ind: ind.surface,
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

def crossover(population, breeder_size=10):
    """
    Chose n creatures and mate those, two parents
    giving birth to two offsprings. Offsprings will
    replace their parents.
    """
    offsprings = []
    shuffle(population)
    for _ in range(int(breeder_size/2)):
        # Genotype of mother and father will be
        # replaced with genotype of offsprings
        mother = population.pop()
        father = population.pop()
        offspring_genotypes = singel_point_recombine(mother.genotype, father.genotype)
        mother.genotype = offspring_genotypes[0]
        father.genotype = offspring_genotypes[1]
        offsprings.append(mother)
        offsprings.append(father)

    population += offsprings

    return population

def singel_point_recombine(gen1, gen2):
    point = randint(0,min(len(gen1),len(gen2)))
    return [gen1[:point]+gen2[point:], gen1[point:]+gen2[:point]]


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
    plot([phenotype.volume for phenotype in population],[phenotype.surface for phenotype in population])  


def main():

    SIZE_POPULATION      = 30
    NUMBER_GENERATIONS   = 100
    MUTATION_PROBABILITY = 0.01

    population = initialize_population(size=SIZE_POPULATION)

    for _ in range(NUMBER_GENERATIONS):
        population = next_generation(population, mutation_probability=MUTATION_PROBABILITY)

    create_summary(population)


if __name__ == '__main__':
    main()