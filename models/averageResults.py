class Average_results:
    experiment_name: str
    population_size: int
    average_generations: float
    average_fitness_evaluations: float
    average_cpu_time: float
    deviations_generations: float
    deviations_fitness_evaluations: float
    deviations_cpu_time: float
    has_reached_good_population: bool = False

    def __init__(self, population_size: int, average_generations: float, average_fitness_evaluations: float, average_cpu_time: float, deviations_generations: float, deviations_fitness_evaluations: float, deviations_cpu_time: float):
        self.population_size = population_size
        self.average_generations = average_generations
        self.average_fitness_evaluations = average_fitness_evaluations
        self.average_cpu_time = average_cpu_time
        self.deviations_generations = deviations_generations
        self.deviations_fitness_evaluations = deviations_fitness_evaluations
        self.deviations_cpu_time = deviations_cpu_time

