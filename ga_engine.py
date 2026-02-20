from models.SchemaResult import SchemaResult
from models.ga import Ga

class GaEngine:
    def __init__(self, ga : Ga):
        self.ga = ga
        self.max_generations = 1200
        self.current_generation = 0
        self.fitness_history = []
        self.schema_dictionary_history = []
        self.history_of_succesrate_competitions = []

    # genetic algorithm. 
    def execute_genetic_engine(self):
        while not self.should_ga_stop():

            self.evaluate_schema_first_value()

            self.current_generation += 1
            self.execute_generation()

            self.fitness_history.append(
                self.ga.evaluate_total_fitness()
            )

            self.history_of_succesrate_competitions.append(
                (self.ga.successAmount_competition, self.ga.errorAmount_competition)
            )

            self.ga.successAmount_competition = 0
            self.ga.errorAmount_competition = 0

    # check if the algorithm should stop, based on reaching the optimum, reaching the maximum number of generations 
    # or stagnating (not having big differences in fitness in the last 20 generations).
    def should_ga_stop(self) -> bool:
        return self.check_for_big_differences() or self.current_generation >= self.max_generations or self.ga.reached_optimum()

    # check if the fitness had big differences in the last 20 generations, if not, we can assume we are stagnating and stop the algorithm.
    def check_for_big_differences(self, threshold=100, check_last_n_generations=20) -> bool:
        if len(self.fitness_history) < check_last_n_generations:
            return False
        recent_history = self.fitness_history[-check_last_n_generations:]
        max_fitness = max(recent_history)
        min_fitness = min(recent_history)
        return max_fitness - min_fitness < threshold

    # one step of the algorithm
    def execute_generation(self):
        print(f"Average fitness: {self.ga.evaluate_average_fitness()}")
        self.ga.family_competition()

    # evaluate the schema of the first value of the genome, to see how it evolves over time.
    def evaluate_schema_first_value(self):
        schema_one = "1" + "*" * (self.ga.population.individuals[0].length - 1)
        schema_zero = "0" + "*" * (self.ga.population.individuals[0].length - 1)

        schema_result_one = SchemaResult(self.current_generation, schema_one)
        schema_result_zero  = SchemaResult(self.current_generation, schema_zero)
        schema_total_fitness_one = 0
        schema_total_fitness_zero = 0

        population_zero = []
        population_one = []

        for individual in self.ga.population.individuals:
            if individual.genome[0] == schema_one[0]:
                schema_result_one.amount = schema_result_one.amount + 1
                schema_total_fitness_one += individual.fitness(self.ga.fitness_strat)
                population_one.append(individual)
            elif individual.genome[0] == schema_zero[0]:
                schema_result_zero.amount = schema_result_zero.amount + 1
                schema_total_fitness_zero += individual.fitness(self.ga.fitness_strat)
                population_zero.append(individual)

        schema_result_one.schema_fitness = schema_total_fitness_one / schema_result_one.amount if schema_result_one.amount > 0 else 0
        schema_result_zero.schema_fitness = schema_total_fitness_zero / schema_result_zero.amount if schema_result_zero.amount > 0 else 0

        schema_result_one.schema_fitness_deviation = self.calculate_standard_deviation_of_SchemaResults(schema_result_one, population_one)
        schema_result_zero.schema_fitness_deviation = self.calculate_standard_deviation_of_SchemaResults(schema_result_zero, population_zero)

        self.schema_dictionary_history.append((schema_result_zero,schema_result_one))

        print(f"Schema {schema_result_one.schema} has amount {schema_result_one.amount}, average fitness {schema_result_one.schema_fitness:.2f} and deviation {schema_result_one.schema_fitness_deviation:.2f}")

    # calculate the standard deviation of a schema result, based on the fitness of the individuals that match the schema.
    def calculate_standard_deviation_of_SchemaResults(self, schema_result: SchemaResult, schema_population: list) -> float:

        total_distance = 0

        for individual in schema_population:
            value = individual.fitness(self.ga.fitness_strat)
            distance = (value - schema_result.schema_fitness) ** 2
            total_distance += distance

        mean_distance = total_distance / len(schema_population) if len(schema_population) > 0 else 0
        return mean_distance ** 0.5
