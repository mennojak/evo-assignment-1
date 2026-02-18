class Results:
    population_size: int
    generations: int
    fitness_evaluations: int
    cpu_time: float

    def __init__(self, population_size: int, generations: int, fitness_evaluations: int, cpu_time: float):
        self.population_size = population_size
        self.generations = generations
        self.fitness_evaluations = fitness_evaluations
        self.cpu_time = cpu_time