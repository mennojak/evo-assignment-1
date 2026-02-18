from enum import Enum
from models.individual import Individual
from models.population import Population
from operators import crossover

class Ga():
    def __init__(self, population_size, max_population):
        self.population_size = population_size
        self.max_population = max_population
        self.population =  Population(population_size)
        self.crossover_strat : str = "UX"
        self.fitness_strat : str = "counting_ones"
        self.amount_of_fitness_evaluations = 0
        self.successAmount_competition = 0
        self.errorAmount_competition = 0

    def reached_optimum(self):
        if self.fitness_strat == "counting_ones":
            for individual in self.population.individuals:
                if individual.fitness() == individual.length:
                    return True
            return False
        elif self.fitness_strat == "trap_deceptive" or self.fitness_strat == "trap_non_deceptive":

            # TODO Implement other fitness strategies here
            pass
        return False
    
    def evaluate_total_fitness(self) -> int:
        total_fitness = 0
        for individual in self.population.individuals:
            total_fitness += individual.fitness()

        return total_fitness

    def evaluate_average_fitness(self) -> int:
        total_fitness = self.evaluate_total_fitness()
        return total_fitness // len(self.population.individuals)
        
    def family_competition(self):
        shuffled_individuals = self.population.get_shuffled_individuals()
        new_pop = Population(0)

        for i in range(0, len(shuffled_individuals), 2):
            parent_a : Individual = shuffled_individuals[i]
            parent_b : Individual = shuffled_individuals[i + 1]

            child_a, child_b = self.produce_offspring(parent_a, parent_b)

            # Tag individuals so we can prioritize children
            family = [
                (parent_a, "parent"),
                (parent_b, "parent"),
                (child_a, "child"),
                (child_b, "child"),
            ]

            # print("\n--- New Family ---")
            # for ind, role in family:
            #     print(f"{role.upper()} fitness: {ind.fitness()}")

            # Sort by:
            # 1. Higher fitness first
            # 2. If equal fitness → child before parent
            sorted_family = sorted(
                family,
                key=lambda x: (x[0].fitness(), 1 if x[1] == "child" else 0),
                reverse=True
            )
            self.amount_of_fitness_evaluations += 2

            self.evaluate_decisions(family)

            # print("\nSorted (best first, child wins ties):")
            # for ind, role in sorted_family:
            #     print(f"{role.upper()} fitness: {ind.fitness()}")

            winners = sorted_family[:2]

            # print("\nSelected for next generation:")
            # for ind, role in winners:
            #     print(f"{role.upper()} survives with fitness {ind.fitness()}")

            # Add only the individual objects
            new_pop.add_new_individuals([ind for ind, _ in winners])

        self.population = new_pop
        
    # Returns 2 chidren, which are the result of crossing their genes.    
    def produce_offspring(self, parent_a : Individual, parent_b : Individual) -> tuple[Individual, Individual]:
        return self.get_child(parent_a, parent_b), self.get_child(parent_b, parent_a)
    
    def get_child(self, parent_a : Individual, parent_b : Individual) -> Individual:
        return crossover(parent_a, parent_b, self.crossover_strat)
    
    def evaluate_decisions(self, family:  list[tuple[Individual, str]]):
        parent1 = family[0][0]
        parent2 = family[1][0]
        child1 = family[2][0]
        child2 = family[3][0]

        list_of_results = []

        for index in  range(len(parent1.genome)):
            if parent1.genome[index] != parent2.genome[index]:
                if child1.genome[index] == '0' and child2.genome[index] == '0':
                    self.successAmount_competition += 1
                elif child1.genome[index] == '1' and child2.genome[index] == '1':
                    self.errorAmount_competition += 1

        


        