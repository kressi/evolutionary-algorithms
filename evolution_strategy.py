"""
Evolution strategies usually are encoded in R^n, binary
encoding has shown to be inefficient.
"""

from random import randint, random, shuffle, gauss
from math import log, pi, exp, sqrt
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
        self.fitness    = None
        self.constraint = None
        
        # Strategy parameters
        self.age        = 0
        self.p_mutation = 0.01


    def __str__(self):
        return ''.join([
            "Gen: ",          self.genotype[:5], ".", self.genotype[5:],
            " H: ",           str(self.height),
            "\tD: ",          str(self.diameter),
            "\tSurface: ",    str(self.fitness),
            "\tVolume: ",     str(self.constraint),
            "\tAge: ",        str(self.age),
            "\tp_mutation: ", str(self.p_mutation)
        ])

    def decode(self):
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

        population[-1].decode()
        population[-1].evaluate()

    return population

def next_generation(population):

    next_generation = crossover(population)
    next_generation = select_phenotypes(next_generation)

    # Evaluate creatures
    for phenotype in next_generation:
        phenotype.decode()
        phenotype.evaluate()
        phenotype.age += 1

    return next_generation

def select_phenotypes(population, mu=7, kappa=15):
    """
    Rank based selection (Stochastic universal sampling)
    """

    # list, sorted by rank and filtered by constraint
    sorted_population = sorted( [creature for creature in population if creature.constraint and creature.age < kappa],
                                key=lambda ind: ind.fitness,
                                reverse=False )

    # List with boundaries of interval for rank probability
    probability_interval = get_probability_interval(len(sorted_population))

    selection = []
    for _ in range(mu):
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

def mutate(population):
    for phenotype in population:
        phenotype.p_mutation = mutate_strategy(phenotype.p_mutation)
        phenotype.genotype   = random_genotype_mutation( phenotype.genotype,
                                                         phenotype.p_mutation )
    return population

def mutate_strategy(sigma):
    """
    non-isotropic mutation
    sigma: mutation strength
    """
    # tau: learning rate
    tau = 1/(sqrt(2))

    return exp( tau*gauss(0,1) )*sigma

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

def crossover(population, nr_offsprings=49):

    offsprings = []
    while len(offsprings) < 49:

        # randomly select three distinct parents
        shuffle(population)
        p1 = population.pop()
        p2 = population.pop()
        p3 = population.pop()

        # Create new genotype
        offspring_genotype = three_parent_recombine(p1.genotype, p2.genotype, p3.genotype)

        # Create new phenotype from genotype
        offsprings.append(CylinderPhenotype(offspring_genotype))
        offsprings[-1].decode()
        offsprings[-1].evaluate()

        # Put parents back into population
        population.append(p1)
        population.append(p2)
        population.append(p3)

    # Mutate offsprings and append to population
    offsprings = mutate(offsprings)
    population += offsprings

    return population

def three_parent_recombine(gen1, gen2, gen3):
    p1 = randint(0,min(len(gen1),len(gen2)))
    p2 = randint(0,min(len(gen1),len(gen2)))
    return gen1[:min(p1,p2)]+gen2[min(p1,p2):max(p1,p2)]+gen3[max(p1,p2):]

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


def main():

    SIZE_POPULATION      = 7
    NUMBER_GENERATIONS   = 100

    # Mutation Strategy Parameter
    # Size of population
    #MU     = 7
    # Maximum age of a phenotype
    #KAPPA  = 15
    # Number of offsprings
    #LAMBDA = 49
    # Number of parents per offspring
    #RHO    = 3

    population = initialize_population(size=SIZE_POPULATION)
    champions  = []

    for _ in range(NUMBER_GENERATIONS):
        population = next_generation(population)
        champions.append(get_champion(population))

    create_summary(champions)


if __name__ == '__main__':
    main()
