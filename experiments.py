import time
from ga_engine import GaEngine
from models.ga import Ga
from models.results import Results
from models.averageResults import Average_results
import matplotlib.pyplot as plt

def run_counting_ones(tracing):
    if tracing:
        print("Running Tracing run (Counting Ones, N=200, UX)...")
        population_size = 200
        genome_length = 40
        ga = Ga(population_size=population_size, max_population=population_size)
        ga_engine = GaEngine(ga)

        ga_engine.execute_genetic_engine()

        generations = list(range(len(ga_engine.fitness_history)))
        avg_fitnesses = [f  / (genome_length * population_size) for f in ga_engine.fitness_history]

        plt.plot(generations, avg_fitnesses, marker='o')
        plt.xlabel("Generation")
        plt.ylabel("Average fitness")
        plt.title("Counting Ones Convergence (Population N=200, Uniform Crossover)")
        plt.grid(True)
        plt.show()

        success_counts = [r[0] for r in ga_engine.history_of_succesrate_competitions]
        error_counts = [r[1] for r in ga_engine.history_of_succesrate_competitions]

        plt.plot(generations, success_counts, marker='o', label="Error Amount")
        plt.plot(generations, error_counts, marker='x', label="Correct Amount")

        plt.xlabel("Generation")
        plt.ylabel("Count")
        plt.title("Selection Decisions per Generation")
        plt.legend()
        plt.grid(True)
        plt.show()


        


    else:
        print("Running Counting Ones experiment...")

    return "TODO"

# Goal to find the min pop needed.
def run_find_min_population(fitness, population_size=10, max_population=1280):
    has_reached_good_population = False
    current_population = population_size

    # Do it 10 times, if the fitness in at least 9 of those 10 was good, then return population used. 
    while not has_reached_good_population and current_population <= max_population:
        amount_good_fitness = 0
        for step in range(10):
            ga = Ga(population_size=current_population, max_population=max_population)
            ga_engine = GaEngine(ga)
            ga_engine.execute_genetic_engine()
            print(f"{step} ---- Just did a GA: {current_population}, reached optimum: {ga.reached_optimum()}. Average Fitness: {ga.evaluate_average_fitness()}")
            if ga.reached_optimum():
                amount_good_fitness += 1
        if amount_good_fitness >= 9:
            # TODO if it's too good, then go back between the previous population and this one, to find the exact one. 
            has_reached_good_population = True
        else:
            current_population *= 2

    if has_reached_good_population:
        print(f"Found good fitness with population size {current_population}")
    else:
        print(f"Could not find good fitness with population size up to {max_population}")

    return current_population if has_reached_good_population else None

def run_optimal_population_size(population_size, amount_of_runs) -> tuple[list[Results], Average_results]:
    Results = []
    for run in range(amount_of_runs):
        start_time = time.time()

        ga = Ga(population_size=population_size, max_population=population_size)            
        ga_engine = GaEngine(ga)
        ga_engine.execute_genetic_engine()

        end_time = time.time()
        Results.append(create_result(ga_engine, cpu_time=end_time - start_time))
    return Results, create_average_results(Results)

def create_result(ga_engine: GaEngine, cpu_time: float) -> Results:
    return Results(
        population_size=ga_engine.ga.population_size,
        generations=ga_engine.current_generation,
        fitness_evaluations=ga_engine.ga.amount_of_fitness_evaluations,
        cpu_time=cpu_time
    )

def create_average_results(list_of_results: list[Results]) -> Average_results:

    average_generations = sum(r.generations for r in list_of_results) / len(list_of_results)
    average_fitness_evaluations = sum(r.fitness_evaluations for r in list_of_results) / len(list_of_results)
    average_cpu_time = sum(r.cpu_time for r in list_of_results) / len(list_of_results)

    deviation_generations = calculate_standard_deviation_of_results(list_of_results, average_generations, lambda r: r.generations)
    deviation_fitness_evaluations = calculate_standard_deviation_of_results(list_of_results, average_fitness_evaluations, lambda r: r.fitness_evaluations)
    deviation_cpu_time = calculate_standard_deviation_of_results(list_of_results, average_cpu_time, lambda r: r.cpu_time)

    return Average_results(
        population_size=list_of_results[0].population_size if list_of_results else 0,
        average_generations=average_generations,
        average_fitness_evaluations=average_fitness_evaluations,
        average_cpu_time=average_cpu_time,
        deviations_generations=deviation_generations,
        deviations_fitness_evaluations=deviation_fitness_evaluations,
        deviations_cpu_time=deviation_cpu_time
    )

def calculate_standard_deviation_of_results(list_of_results: list[Results], mean_value: float, key_func) -> float:

    total_distance = 0

    for r in list_of_results:
        value = key_func(r)
        distance = (value - mean_value) ** 2
        total_distance += distance

    mean_distance = total_distance / len(list_of_results)
    return mean_distance ** 0.5
