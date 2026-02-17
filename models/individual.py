import random

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
    
    def fitness(self) -> int:
        return self.genome.count("1")
    
    # Counting ones

    # Trap functions (tightly linked)
        # Deceptive trap
        # Non-deceptive trap

    # Trap functions (not linked)
            