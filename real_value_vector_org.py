import random
from fitness_function import Fitness_Function, sphere_function, MUTATION_EFFECT_SIZE
from functools import total_ordering

LENGTH = None
RANGE_MIN = None
RANGE_MAX = None

@total_ordering
class RealValueVectorOrg(object):
    """
    this is a class that represents organisms as a real value vector
    fitness is determined by calling the fitness fuction
    the length is determined at object creation
    """

    def __init__(self, genotype=None):
        if genotype is None:
            genotype = _create_random_genotype()
        assert LENGTH == len(genotype)
        self.genotype = genotype
        self.environment = None

    def fitness(self, environment=None):
        if environment is None:
            if self.environment is None:
                raise AssertionError("Can't call fitness unless you set an environment")
            environment = self.environment
        return environment(self.genotype)

    def get_mutant(self):
        return RealValueVectorOrg(_get_mutated_genotype(self.genotype, MUTATION_EFFECT_SIZE))

    def get_clone(self):
        return RealValueVectorOrg(self.genotype)

    def __lt__(self, other):
        if self.fitness(self.environment) > other.fitness(self.environment):
            return True
        return self.genotype < other.genotype

    def __eq__(self, other):
        return self.genotype == other.genotype

    def __str__(self):
        return "RealValueVectorOrg({})".format(self.genotype)

    def __repr__(self):
        return str(self)

def _get_mutated_genotype(genotype, effect_size):
    "Mutates one locus in organism at random"
    mut_location = random.randrange(len(genotype))
    delta = random.normalvariate(0, effect_size)
    mutant_value = genotype[mut_location] + delta

    mutant = genotype[:]
    mutant[mut_location] = _wrap_around(mutant_value, RANGE_MIN, RANGE_MAX)            
    return mutant

def _wrap_around(value, min_, max_):
    width = max_ - min_
    while value < min_ or value > max_:
        if value < min_:
            value += width
        else:
            value -= width
    return value

def _create_random_genotype():
    genotype = []
    for _ in range(LENGTH):
        genotype.append(random.uniform(RANGE_MIN, RANGE_MAX))
    return genotype
