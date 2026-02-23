import time
from ga_engine import GaEngine
from models.ga import Ga
from models.results import Results
from models.averageResults import Average_results
import matplotlib.pyplot as plt

# runs the specific experiment to plot, with population of 200, uniform crossover, and counting ones as fitness function.
def run_counting_ones(tracing, fitness_strat, crossover_strat) -> int:
    if tracing:
        population_size = 200
        genome_length = 40
        ga = Ga(population_size=population_size, max_population=population_size, fitness_strat="counting_ones", crossover_strat="UX")
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

        plt.plot(generations, success_counts, marker='o', label="Success Amount")
        plt.plot(generations, error_counts, marker='x', label="Error Amount")

        plt.xlabel("Generation")
        plt.ylabel("Count")
        plt.title("Selection Decisions per Generation (Population N=200, Uniform Crossover)")
        plt.legend()
        plt.grid(True)
        plt.show()
        
        schema_zero_amounts = [r[0].amount for r in ga_engine.schema_dictionary_history]
        schema_one_amounts = [r[1].amount for r in ga_engine.schema_dictionary_history]

        plt.plot(generations, schema_zero_amounts, marker='o', label="Schema 0*")
        plt.plot(generations, schema_one_amounts, marker='x', label="Schema 1*")
        plt.xlabel("Generation")
        plt.ylabel("Amount")
        plt.title("Schema amount per Generation (Population N=200, Uniform Crossover)")
        plt.legend()
        plt.grid(True)
        plt.show()

        schema_zero_fitnesses = [r[0].schema_fitness for r in ga_engine.schema_dictionary_history]
        schema_one_fitnesses = [r[1].schema_fitness for r in ga_engine.schema_dictionary_history]
        schema_zero_fitnesses_deviations = [r[0].schema_fitness_deviation for r in ga_engine.schema_dictionary_history]
        schema_one_fitnesses_deviations = [r[1].schema_fitness_deviation for r in ga_engine.schema_dictionary_history]

        plt.errorbar(generations, schema_zero_fitnesses, yerr=schema_zero_fitnesses_deviations, marker='o', label="Schema 0*")
        plt.errorbar(generations, schema_one_fitnesses, yerr=schema_one_fitnesses_deviations, marker='x', label="Schema 1*")
        plt.xlabel("Generation")
        plt.ylabel("Average Fitness")
        plt.title("Schema Average Fitness per Generation (Population N=200, Uniform Crossover)")
        plt.legend()
        plt.grid(True)
        plt.show()

        return None
    else:
        return run_find_min_population(fitness_strat=fitness_strat, crossover_strat=crossover_strat)

# Goal to find the min pop needed.
def run_find_min_population(
    population_size: int = 10,
    max_population: int = 1280,
    fitness_strat: str = "",
    crossover_strat: str = "",
) -> int | None:

    STEP_BASE = 5
    current = population_size
    last_bad = None
    first_good = None

    # Double search till we find a good population size, or reach the max_population limit.
    while current <= max_population:
        if is_population_good(current, fitness_strat, crossover_strat):
            first_good = current
            break
        else:
            last_bad = current
            current *= 2

    if first_good is None:
        print(f"Could not find suitable population up to {max_population}")
        return None

    if last_bad is None:
        print(f"Found minimal population size: {first_good}")
        return first_good

    # Go back and forth till we find an even better population size.
    refinement_steps = 0
    best_found = first_good

    step_size = (first_good - last_bad) // 2

    step_size = max(STEP_BASE, (step_size // STEP_BASE) * STEP_BASE)

    while refinement_steps < 10 and step_size >= STEP_BASE:

        candidate = best_found - step_size

        if candidate <= last_bad:
            break

        print(f"Refinement step {refinement_steps + 1}: trying {candidate}")

        if is_population_good(candidate, fitness_strat, crossover_strat):
            best_found = candidate
        else:
            last_bad = candidate

        # halve step size
        step_size //= 2
        step_size = (step_size // STEP_BASE) * STEP_BASE

        refinement_steps += 1

    print(f"\nFinal minimal population size: {best_found}")
    return best_found

# Runs a test to see if a population size is good, by running 10 runs of the genetic algorithm and checking if at least 9 of them reached the optimum fitness.
def is_population_good(pop_size: int, fitness_strat, crossover_strat) -> bool:
    success_count = 0

    for run in range(10):
        ga = Ga(
            population_size=pop_size,
            max_population=pop_size,
            fitness_strat=fitness_strat,
            crossover_strat=crossover_strat,
        )
        ga_engine = GaEngine(ga)
        ga_engine.execute_genetic_engine()

        reached = ga.reached_optimum()
        print(
            f"[Pop {pop_size}] Run {run+1}/10 → "
            f"Reached optimum: {reached}"
        )

        if reached:
            success_count += 1

    print(f"[Pop {pop_size}] Success rate: {success_count}/10\n")
    return success_count >= 9

# runs the optimal population size, based on the found population size of function run_find_min_population.
def run_optimal_population_size(population_size, amount_of_runs, fitness_strat, crossover_strat) -> tuple[list[Results], Average_results]:
    results = []
    for run in range(amount_of_runs):
        start_time = time.time()

        ga = Ga(population_size=population_size, max_population=population_size, fitness_strat=fitness_strat, crossover_strat=crossover_strat)            
        ga_engine = GaEngine(ga)
        ga_engine.execute_genetic_engine()

        end_time = time.time()
        results.append(create_result(ga_engine, cpu_time=end_time - start_time))
    return results, create_average_results(results)

# create result data of one run of the genetic algorithm.
def create_result(ga_engine: GaEngine, cpu_time: float) -> Results:
    return Results(
        population_size=ga_engine.ga.population_size,
        generations=ga_engine.current_generation,
        fitness_evaluations=ga_engine.ga.amount_of_fitness_evaluations,
        cpu_time=cpu_time
    )

# create average results of multiple runs of the genetic algorithm, with standard deviations.
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

# calculate standard deviation of a list of results, based on a key function (generations,fitness,cpu_time) 
# to extract the value to calculate the deviation on.
def calculate_standard_deviation_of_results(list_of_results: list[Results], mean_value: float, key_func) -> float:

    total_distance = 0

    for r in list_of_results:
        value = key_func(r)
        distance = (value - mean_value) ** 2
        total_distance += distance

    mean_distance = total_distance / len(list_of_results)
    return mean_distance ** 0.5


def run_crossover_test():
    population_size = 10
    genome_length = 20
    fitness_strat = "counting_ones"
    crossover_strat = "UX"

    ga = Ga(population_size=population_size, max_population=population_size, fitness_strat=fitness_strat, crossover_strat=crossover_strat)
    parent_a = ga.population.individuals[0]
    parent_b = ga.population.individuals[1]

    print(f"Parent A: {parent_a.genome}, Fitness: {parent_a.fitness(ga.fitness_strat)}")
    print(f"Parent B: {parent_b.genome}, Fitness: {parent_b.fitness(ga.fitness_strat)}")

    child_a, child_b = ga.produce_offspring(parent_a, parent_b)

    print(f"Child A: {child_a.genome}, Fitness: {child_a.fitness(ga.fitness_strat)}")
    print(f"Child B: {child_b.genome}, Fitness: {child_b.fitness(ga.fitness_strat)}")