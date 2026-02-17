from models.individual import Individual


class Population:
    def __init__(self, N):
        self.individuals = []
        for _ in range(N):
            self.individuals.append(Individual())
    
    
    