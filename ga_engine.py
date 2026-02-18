from models.ga import Ga


class GaEngine:
    def __init__(self, ga : Ga):
        self.ga = ga
        self.max_epochs = 1200000
        self.current_epoch = 0
        self.fitness_history = []

    # Genetic algorithm. 
    def execute_genetic_engine(self):
        while not self.should_ga_stop():
            self.current_epoch += 1
            self.execute_epoch()
            self.fitness_history.append(self.ga.evaluate_total_fitness())

    def should_ga_stop(self) -> bool:
        return self.check_for_big_differences() or self.current_epoch >= self.max_epochs or self.ga.reached_optimum()

    def check_for_big_differences(self, threshold=100, check_last_n_epochs=20) -> bool:
        # check if the fitness had big differences in the last 10 epochs, if not, we can assume we are stagnating and stop the algorithm.
        if len(self.fitness_history) < check_last_n_epochs:
            return False
        recent_history = self.fitness_history[-check_last_n_epochs:]
        max_fitness = max(recent_history)
        min_fitness = min(recent_history)
        return max_fitness - min_fitness < threshold

    # one step of the algorithm
    def execute_epoch(self):
        print(f"Average fitness: {self.ga.evaluate_average_fitness()}")
        self.ga.family_competition()


# evaluate_individual(genome, fitness_fn)

# shuffle_population(pop)

# pair_families(pop)

# produce_offspring(parent_a, parent_b, crossover_fn)

# family_competition(parents, offspring)

# check_optimum(pop)

# check_stagnation(counter)