from models.ga import Ga


class GaEngine:
    def __init__(self, ga : Ga):
        self.ga = ga
        self.max_generations = 1200000
        self.current_generation = 0
        self.fitness_history = []

    # Genetic algorithm. 
    def execute_genetic_engine(self):
        while not self.should_ga_stop():
            self.current_generation += 1
            self.execute_generation()
            self.fitness_history.append(self.ga.evaluate_total_fitness())

    def should_ga_stop(self) -> bool:
        return self.check_for_big_differences() or self.current_generation >= self.max_generations or self.ga.reached_optimum()

    def check_for_big_differences(self, threshold=100, check_last_n_generations=20) -> bool:
        # check if the fitness had big differences in the last 20 generations, if not, we can assume we are stagnating and stop the algorithm.
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


# evaluate_individual(genome, fitness_fn)

# shuffle_population(pop)

# pair_families(pop)

# produce_offspring(parent_a, parent_b, crossover_fn)

# family_competition(parents, offspring)

# check_optimum(pop)

# check_stagnation(counter)