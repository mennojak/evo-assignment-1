from models.individual import Individual
import random

class Population:
    def __init__(self, N):
        self.individuals : list[Individual] = []
        for _ in range(N):
            self.individuals.append(Individual())
    
    def get_shuffled_individuals(self) -> list[Individual]:
        shuffled = self.individuals[:]
        random.shuffle(shuffled)
        return shuffled
    
    def add_new_individuals(self, new_individuals):
        self.individuals.extend(new_individuals)