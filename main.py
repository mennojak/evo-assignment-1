from secrets import choice
import time
from experiments import run_counting_ones, run_find_min_population, run_optimal_population_size
from models.results import Results
from models.averageResults import Average_results
from pandas import DataFrame
import pandas as pd

def main():
    print("Select experiment:")
    print("1 - Counting Ones")
    print("2 - Deceptive Trap Function (tightly linked)")
    print("3 - Non-deceptive Trap Function (tightly linked)")
    print("4 - Deceptive Trap Function (loosely linked)")
    print("5 - Non-deceptive Trap Function (loosely linked)")
    print("6 - Tracing run (Counting Ones, N=200, UX)")

    choice = input("Enter 1-6: ")

    if choice != "6":
        print("\nSelect crossover strategy:")
        print("1 - Uniform Crossover (UX)")
        print("2 - Two-Point Crossover (2X)")
        operator_choice = input("Enter the number of the crossover strategy you want to use: ")

    start_time = time.time()

    population_size = None
    name: str = ""

    if choice == "1":
        print("Running Counting Ones experiment...")
        population_size = run_counting_ones(tracing=False, fitness_strat="counting_ones", crossover_strat="UX" if operator_choice == "1" else "2X")
        name = "Counting Ones - " + ("UX" if operator_choice == "1" else "2X")

    elif choice == "2":
        print("Running Deceptive Trap Function (tightly linked) experiment...")
        population_size = run_find_min_population(fitness_strat="trap_tight_deceptive", crossover_strat="UX" if operator_choice == "1" else "2X")
        name = f"Deceptive Trap Function (tightly linked) - {('UX' if operator_choice == '1' else '2X')}"

    elif choice == "3":
        print("Running Non-deceptive Trap Function (tightly linked) experiment...")
        population_size = run_find_min_population(fitness_strat="trap_tight_nondeceptive", crossover_strat="UX" if operator_choice == "1" else "2X")
        name = f"Non-deceptive Trap Function (tightly linked) - {('UX' if operator_choice == '1' else '2X')}    "

    elif choice == "4":
        print("Running Deceptive Trap Function (not linked) experiment...")
        population_size = run_find_min_population(fitness_strat="trap_loose_deceptive", crossover_strat="UX" if operator_choice == "1" else "2X")
        name = f"Deceptive Trap Function (not linked) - {('UX' if operator_choice == '1' else '2X')}"

    elif choice == "5":
        print("Running Non-deceptive Trap Function (not linked) experiment...")
        population_size = run_find_min_population(fitness_strat="trap_loose_nondeceptive", crossover_strat="UX" if operator_choice == "1" else "2X")
        name = f"Non-deceptive Trap Function (not linked) - {('UX' if operator_choice == '1' else '2X')}"

    elif choice == "6":
        print("Running Tracing run (Counting Ones, N=200, UX)...")
        run_counting_ones(tracing=True, fitness_strat="counting_ones", crossover_strat="UX")
        name = "Tracing run (Counting Ones, N=200, UX)"

    if population_size is not None:
        results, average_results = run_optimal_population_size(population_size=population_size, amount_of_runs=10)
        average_results.experiment_name = name
        average_results.has_reached_good_population = True
        show_results(results,average_results)
    else:
        print("global optimum was not reached in any of the runs, so no results to show.")

    end_time = time.time()
    print(f"Experiment completed in {end_time - start_time:.2f} seconds.")

# show results of executed experiment.
def show_results(results: list[Results], average_results: Average_results):

    runs_data = {
        "Run": list(range(1, len(results) + 1)),
        "Population size": [r.population_size for r in results],
        "Generations": [r.generations for r in results],
        "Fitness evaluations": [r.fitness_evaluations for r in results],
        "CPU Time (s)": [r.cpu_time for r in results],
        "Success": "-",
    }

    df_runs = DataFrame(runs_data)

    average_row = DataFrame({
        "Run": ["average"],
        "Population size": [average_results.population_size],
        "Generations": [
            f"{average_results.average_generations:.2f} "
            f"(σ = {average_results.deviations_generations:.2f})"
        ],
        "Fitness evaluations": [
            f"{average_results.average_fitness_evaluations:.2f} "
            f"(σ = {average_results.deviations_fitness_evaluations:.2f})"
        ],
        "CPU Time (s)": [
            f"{average_results.average_cpu_time:.4f} "
            f"(σ = {average_results.deviations_cpu_time:.4f})"
        ],
        "Success": [average_results.has_reached_good_population],
    })


    final_df = DataFrame(pd.concat([df_runs, average_row], ignore_index=True))

    print(f"\n===== {average_results.experiment_name} =====")
    print(final_df.to_string(index=False))


if __name__ == "__main__":    
    main()