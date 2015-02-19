from random import randint, random
from math import pi, ceil, log

class Individual:
    
    def __init__(self, bin_string=None, size=[5,5]):

        self.size = size
        if not bin_string:
            self.bin_string = self.random_bin_string(sum(self.size))
        else:
            self.bin_string = bin_string

        self.d          = 0
        self.h          = 0
        self.fitness    = 0
        self.constraint = 0

    def show(self):
        print(''.join(['Bin: ', self.bin_string,
                       ', h:', str(self.h),
                       ', d:', str(self.d), 
                       ', Fitness: ', str(self.fitness),
                       ', Constraint: ', str(self.constraint)]))

    def random_bin_string(self, length):
        bin_string = ''
        for _ in range(length):
            bin_string += str(randint(0,1))
        return bin_string

    def bin_to_int(self, bin_string):
        base = 1
        num = 0
        for i in bin_string:
            num += base*int(i)
            base *= 2
        return num

    def evaluate(self, fitness=(lambda d, h: pi*d**2/2 + pi*d*h),
                       constraint=(lambda d, h: pi*d**2*h/4 >= 300) ):
        """
        Evaluate Individual with provided fitness function and
        determine constraint.
        """

        self.d = self.bin_to_int(self.bin_string[:self.size[0]:-1])
        self.h = self.bin_to_int(self.bin_string[self.size[0]::-1])

        self.fitness    = fitness(self.d, self.h)
        self.constraint = constraint(self.d, self.h)

        return {'Fitness': self.fitness, 'Constraint': self.constraint}


def get_rank_based_selection(population):

    # sorted and filtered list
    auxiliary_population = sorted( [ind for ind in population if ind.constraint],
                                   key=lambda ind: ind.fitness,
                                   reverse=True )

    # List with boundaries of interval for rank probability
    probability_interval = get_probability_interval(len(auxiliary_population))

    selection = []
    for _ in range(len(population)):
        rand = random()
        for i, sub_interval in enumerate(probability_interval):
            if rand <= sub_interval:
                break
        selection.append(auxiliary_population[i])

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

def mutate(string, p=0.1):

    result = []
    for c in string:
        if random() <= p:
            c = '0' if c == '1' else '1'
        result.append(c)

    return ''.join(result)


def main():
    """
    """

    SIZE_POPULATION = 30

    # create initial population
    population = []
    for _ in range(SIZE_POPULATION):
        population.append(Individual())

    # Evaluate individuals of population
    for ind in population:
        [fitness, constraint] = ind.evaluate()

    # Rank based selection
    selection = get_rank_based_selection(population)


    print('\nSelection')
    for ind in selection:
        ind.show()

    # Mutate
    for ind in selection:
        ind.bin_string = mutate(ind.bin_string)

    print('\nMutated')
    for ind in selection:
        ind.show()


if __name__ == '__main__':
    main()