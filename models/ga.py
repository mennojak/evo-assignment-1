from models.population import Population

class Ga():
    def __init__(self, population_size, generations):
        self.population_size = population_size
        self.generations = generations
        self.population =  Population(population_size)