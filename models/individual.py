import random

class Individual: 
    def __init__(self):
        self.length = 40
        self.genome = self.generate_genome()

    def generate_genome(self):
        genome = ""
        for _ in range(self.length):
            genome += random.choice(["0", "1"])
        return genome
        