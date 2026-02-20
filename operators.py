import random

from models.individual import Individual

# crossover operators for the genetic algorithm.
def uniform_crossover(parent_a : Individual, parent_b : Individual) -> Individual:
    genome_a = parent_a.genome
    genome_b = parent_b.genome

    if len(genome_a) != len(genome_b):
        raise ValueError("Parents must have genomes of equal length")

    child_genome = ""

    for i in range(len(genome_a)):
        if random.random() < 0.5:
            child_genome += genome_a[i]
        else:
            child_genome += genome_b[i]

    return Individual(child_genome)

# two-point crossover operator for the genetic algorithm.
def two_point_crossover(parent_a, parent_b):
    genome_a = parent_a.genome
    genome_b = parent_b.genome

    if len(genome_a) != len(genome_b):
        raise ValueError("Parents must have genomes of equal length")

    length = len(genome_a)

    # Choose two distinct crossover points
    p1 = random.randint(0, length - 2)
    p2 = random.randint(p1 + 1, length - 1)

    child_genome = (
        genome_a[:p1] +
        genome_b[p1:p2] +
        genome_a[p2:]
    )

    return Individual(child_genome)

# crossover strategy selector, based on the selected type of crossover.
def crossover(parent_a : Individual, parent_b : Individual, strategy) -> Individual:
    if strategy == "UX":
        return uniform_crossover(parent_a, parent_b)
    elif strategy == "2X":
        return two_point_crossover(parent_a, parent_b)
    else:
        raise ValueError(f"Unknown crossover strategy {strategy}")