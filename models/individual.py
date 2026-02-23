import random

from models import ga

class Individual: 
    def __init__(self, genome : str = None):
        self.length = 40
        if genome is None:
            self.genome = self.generate_genome()
        else:
            self.genome = genome

        self.stored_fitness = {}

    def get_length(self) -> int:
        return self.length

    def generate_genome(self) -> str:
        genome = ""
        self.stored_fitness = {}
        for _ in range(self.length):
            genome += random.choice(["0", "1"])
        return genome
    
    def fitness(self, fitness_strat) -> float:
        if fitness_strat in self.stored_fitness:
            return self.stored_fitness[fitness_strat]
        fitness_value = 0
        if fitness_strat == "counting_ones":
            fitness_value = self.genome.count("1")   
        else:
            subfunction_length = 4
            number_of_subfunctions = self.length // subfunction_length     
            d = 1.0 if fitness_strat == "trap_tight_deceptive" or fitness_strat == "trap_loose_deceptive" else 2.5
            tight = True if fitness_strat == "trap_tight_nondeceptive" or fitness_strat == "trap_tight_deceptive" else False

            for j in range(number_of_subfunctions): 
                indices = []
                if tight:
                    indices = [j*subfunction_length + i for i in range(subfunction_length)] # [1, 2, 3, 4], [5, 6, 7, 8], etc
                else: 
                    indices = [j + i*number_of_subfunctions for i in range(subfunction_length)] # [1, 11, 21, 31], [2, 12, 22, 32], etc

                subfunction_counting_ones = sum(self.genome[index] == '1' for index in indices)
                
                if subfunction_counting_ones == subfunction_length:
                    B = subfunction_length
                else:
                    B = subfunction_length - d - ((subfunction_length - d) / (subfunction_length - 1)) * subfunction_counting_ones
                
                fitness_value += B

        self.stored_fitness[fitness_strat] = fitness_value
        return fitness_value
            