from ga_engine import GaEngine
from models.ga import Ga


def run_counting_ones(tracing):
    if tracing:
        print("Running Tracing run (Counting Ones, N=200, UX)...")

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

