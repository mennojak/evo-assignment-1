from models.individual import Individual
from models.population import Population
from operators import crossover

class Ga():
    def __init__(self, population_size, max_population, fitness_strat, crossover_strat):
        self.population_size = population_size
        self.max_population = max_population
        self.population =  Population(population_size)
        self.crossover_strat = crossover_strat
        self.fitness_strat = fitness_strat
        self.amount_of_fitness_evaluations = 0
        self.successAmount_competition = 0
        self.errorAmount_competition = 0

    # check if one of the individuals in the population has reached the optimum fitness.
    def reached_optimum(self):
        for individual in self.population.individuals:
            if individual.fitness(self.fitness_strat) == individual.length:
                return True
        return False

    # evaluate the total fitness of the population, by summing the fitness of all individuals.
    def evaluate_total_fitness(self) -> int:
        total_fitness = 0
        for individual in self.population.individuals:
            total_fitness += individual.fitness(self.fitness_strat)
        return total_fitness

    # evaluate the average fitness of the population, by dividing the total fitness by the number of individuals.
    def evaluate_average_fitness(self) -> int:
        total_fitness = self.evaluate_total_fitness()
        return total_fitness // len(self.population.individuals)
        
    # do selection based on family competition.
    def family_competition(self):
        shuffled_individuals = self.population.get_shuffled_individuals()
        new_pop = Population(0)
        fitness_strategy = self.fitness_strat

        for i in range(0, len(shuffled_individuals), 2):
            parent_a : Individual = shuffled_individuals[i]
            parent_b : Individual = shuffled_individuals[i + 1]

            child_a, child_b = self.produce_offspring(parent_a, parent_b)

            family = [
                (parent_a, "parent"),
                (parent_b, "parent"),
                (child_a, "child"),
                (child_b, "child"),
            ]

            # Sort by:
            # 1. Higher fitness first
            # 2. If equal fitness → child before parent
            sorted_family = sorted(
                family,
                key=lambda x: (x[0].fitness(fitness_strategy), 1 if x[1] == "child" else 0),
                reverse=True
            )
            self.amount_of_fitness_evaluations += 2

            self.evaluate_decisions(sorted_family)

            winners = sorted_family[:2]

            new_pop.add_new_individuals([ind for ind, _ in winners])

        self.population = new_pop
        
    # Returns 2 chidren, which are the result of crossing their genes with parents.    
    def produce_offspring(self, parent_a : Individual, parent_b : Individual) -> tuple[Individual, Individual]:
        return self.get_child(parent_a, parent_b), self.get_child(parent_b, parent_a)
    
    # return the child of the two parents, based on the selected crossover strategy.
    def get_child(self, parent_a : Individual, parent_b : Individual) -> Individual:
        return crossover(parent_a, parent_b, self.crossover_strat)
    
    # check amount of successes and errors made in the family competition.
    def evaluate_decisions(self, sorted_family:  list[tuple[Individual, str]]):
        winner1 = sorted_family[0][0]
        winner2 = sorted_family[1][0]
        parents = [ind for ind, role in sorted_family if role == "parent"]
        parent1 = parents[0]
        parent2 = parents[1]

        for index in  range(len(parent1.genome)):
            if parent1.genome[index] != parent2.genome[index]:
                if winner1.genome[index] == '0' and winner2.genome[index] == '0':
                    self.errorAmount_competition += 1
                elif winner1.genome[index] == '1' and winner2.genome[index] == '1':
                    self.successAmount_competition += 1

        


        