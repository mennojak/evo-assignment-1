def main():
    print("Select experiment:")
    print("1 - Counting Ones")
    print("2 - Deceptive Trap Function (tightly linked)")
    print("3 - Non-deceptive Trap Function (tightly linked)")
    print("4 - Deceptive Trap Function (not linked)")
    print("5 - Non-deceptive Trap Function (not linked)")
    print("6 - Tracing run (Counting Ones, N=200, UX)")

    choice = input("Enter 1-6: ")

    if choice == "1":
        print("Running Counting Ones experiment...")
        other_function(fitness="counting_ones", crossover="ux")

    elif choice == "2":
        print("Running Deceptive Trap Function (tightly linked) experiment...")
        run_find_min_population(fitness="trap_tight_deceptive", crossover="ux")

    elif choice == "3":
        print("Running Non-deceptive Trap Function (tightly linked) experiment...")
        run_find_min_population(fitness="trap_tight_nondeceptive", crossover="ux")

    elif choice == "4":
        print("Running Deceptive Trap Function (not linked) experiment...")
        run_find_min_population(fitness="trap_loose_deceptive", crossover="ux")

    elif choice == "5":
        print("Running Non-deceptive Trap Function (not linked) experiment...")
        run_find_min_population(fitness="trap_loose_nondeceptive", crossover="ux")

    elif choice == "6":
        print("Running Tracing run (Counting Ones, N=200, UX)...")
        other_function(fitness="counting_ones", crossover="ux", n=200)

if __name__ == "__main__":    main()