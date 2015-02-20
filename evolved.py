from random import randint, random
from math import pi, ceil, log
from copy import copy

class Individual:
    
    def __init__( self, properties, fnc_fitness, fnc_constraint, bin_string=None ):

        self.properties     = properties
        self.names          = list(properties.keys())
        self.size           = list(properties.values())
        self.bin_string     = bin_string if bin_string else random_bin_string(sum(self.size))
        self.integers       = []
        self.fitness        = 0
        self.constraint     = 0
        self.fnc_fitness    = fnc_fitness
        self.fnc_constraint = fnc_constraint

    def evaluate(self):
        """
        Calculate new values and evaluate Individual with
        fitness function and determine constraint.
        """
        self.calculate_integers()

        self.fitness    = self.fnc_fitness(self.integers)
        self.constraint = self.fnc_constraint(self.integers)

        return {'Fitness': self.fitness, 'Constraint': self.constraint}

    def show(self):
        print(''.join(['Bin: ', self.bin_string,
                       ', ', str(zip(self.names, self.integers)),
                       ', Fitness: ', str(self.fitness),
                       ', Constraint: ', str(self.constraint)]))



    def calculate_integers(self):
        """
        Split bin_string according to size of properties
        and convert substrings to decimal numbers.
        """
        s0 = 0
        self.integers = []
        for s1 in self.size:
            self.integers.append(
                self.bin_to_int(self.bin_string[s0:s0+s1])
            )
            s0 += s1

        return self.integers

    def bin_to_int(self, bin_string):
        base = 1
        num = 0
        for i in bin_string[::-1]:
            num += base*int(i)
            base *= 2
        return num


def random_bin_string(length):
    bin_string = ''
    for _ in range(length):
        bin_string += str(randint(0,1))
    return bin_string

def get_rank_based_selection(population, size=None, greatest_fitness_first=True):

    # list, sorted by rank and filtered by constraint
    sorted_population = sorted( population,
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

def singel_point_recombine(str1, str2):
    point = randint(0,len(str1))
    return [str1[:point]+str2[point:], str1[point:]+str2[:point]]

def mutate(bin_string, p=0.1):
    """
    Function mutate inverts each bit of bin_string with
    probability p.
    """
    result = []
    for c in bin_string:
        if random() <= p:
            c = '0' if c == '1' else '1'
        result.append(c)

    return ''.join(result)

def next_generation(population):
    """
    creates next generation from a population
    i)   current population is evaluated
    ii)  individuals for reproduction are selected
    iii) selected individuals are mutated and copulated
    """

    # Evaluate individuals of population
    for ind in population:
        [fitness, constraint] = ind.evaluate()
    
    # Rank based selection of individuals fullfilling constraint
    selection = get_rank_based_selection( [ind for ind in population if ind.constraint],
                                          size=len(population),
                                          greatest_fitness_first = False )

    # Mutate
    for ind in selection:
        ind.bin_string = mutate(ind.bin_string)

    return selection

def main():

    SIZE_POPULATION = 30
    surface_cylinder = (lambda prop: pi*prop[0]**2/2 + pi*prop[0]*prop[1])
    volume_cylinder_constraint = (lambda prop: pi*prop[0]**2*prop[1]/4 >= 300)
    encoded_properties_cylinder = {
        'diameter': 5,
        'height': 5
    }

    # create initial population
    population = []
    for _ in range(SIZE_POPULATION):
        population.append(Individual( properties=encoded_properties_cylinder,
                                      fnc_fitness=surface_cylinder,
                                      fnc_constraint=volume_cylinder_constraint ))

    for _ in range(100):
        population = next_generation(population)

        print('\nMutated')
        for ind in population:
            ind.show()

if __name__ == '__main__':
    main()