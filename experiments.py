from ga_engine import execute_ga_epoch
from models.ga import Ga


def run_counting_ones(tracing):
    if tracing:
        print("Running Tracing run (Counting Ones, N=200, UX)...")

    else:
        print("Running Counting Ones experiment...")

    return "TODO"

def run_find_min_population(fitness, population_size=10, generations=1280):

    ga = Ga(population_size=population_size, generations=generations)

    while ga:
        execute_ga_epoch(ga)

    return "TODO"

