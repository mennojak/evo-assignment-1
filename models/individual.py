import random

from models import ga

class Individual: 
    def __init__(self, genome : str = None):
        self.length = 40
        if genome is None:
            self.genome = self.generate_genome()
        else:
            self.genome = genome

    def generate_genome(self) -> str:
        genome = ""
        for _ in range(self.length):
            genome += random.choice(["0", "1"])
        return genome
    
    def fitness(self, fitness_strat) -> float:
        fitness_value = 0
        if fitness_strat == "counting_ones":
            fitness_value = self.genome.count("1")   
        else:
            k = 4 # Subfunction length   
            number_of_subfunctions = self.length // k     
            d = 1.0 if fitness_strat == "trap_tight_deceptive" or fitness_strat == "trap_loose_deceptive" else 2.5
            tight = True if fitness_strat == "trap_tight_nondeceptive" or fitness_strat == "trap_tight_deceptive" else False

            for j in range(number_of_subfunctions): 
                indices = []
                if tight:
                    indices = [j*k + i for i in range(k)] # [1, 2, 3, 4], [5, 6, 7, 8], etc
                else: 
                    indices = [j + i*number_of_subfunctions for i in range(k)] # [1, 11, 21, 31], [2, 12, 22, 32], etc

                subfunction_counting_ones = sum(self.genome[index] == '1' for index in indices)
                
                if subfunction_counting_ones == k:
                    B = k
                else:
                    B = k - d - ((k - d) / (k - 1)) * subfunction_counting_ones
                
                fitness_value += B

        return fitness_value
            