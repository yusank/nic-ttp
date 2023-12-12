import Fitness
import matplotlib.pyplot as plt


def main():
    total_fitness = Fitness.total_fitness
    for row in total_fitness:
        print("\t".join(map(str, row)))

    total_profit = [row[2] for row in total_fitness]
    total_time = [row[3] for row in total_fitness]

    plt.scatter(total_time, total_profit, alpha=0.5)
    plt.title("Total Profit vs Total Time")
    plt.xlabel("Total Time")
    plt.ylabel("Total Profit")
    plt.show()


main()

