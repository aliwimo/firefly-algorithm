import random
import math
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

MAX_GENERATION = 50
POPULATION_SIZE = 90
DIMENSION_SIZE = 30
ALPHA = 0.2
BETA0 = 1.0
GAMMA = 1.0
BOUND = 100
UB = BOUND
LB = -BOUND

Location_Array = [0] * DIMENSION_SIZE
Firefly_List = [0] * POPULATION_SIZE
Fitnesses = [0] * POPULATION_SIZE
Disntances = [0] * POPULATION_SIZE
Best = []

class Firefly:
    def __init__(self, location):
        self.location = location.copy()
        self.fitness = self.update_fitness()

    def update_fitness(self): #f3 (Sphere)
        return sum(i ** 2 for i in self.location)

    def light_intensity(self, distance):
        return self.fitness * math.exp(-GAMMA * (distance ** 1))

    def attractiveness(self, distance):
        return BETA0 * math.exp(-GAMMA * (distance ** 2))

    def update_location(self, other, distance):
        for index in range(DIMENSION_SIZE):
            epsilon = random.random() - 0.5
            alpha = ALPHA - (random.uniform(-ALPHA, ALPHA))
            rand = alpha * epsilon
            self.location[index] += self.attractiveness(distance) * (other.location[index] - self.location[index]) + rand
            # if self.location[index] > UB:
            #     self.location[index] = UB
            # if self.location[index] < LB:
            #     self.location[index] = LB

    def move_randomly(self):
        for index in range(DIMENSION_SIZE):
            epsilon = random.random() - 0.5
            alpha = ALPHA - (random.uniform(0, ALPHA))
            rand = alpha * epsilon
            self.location[index] += rand

    def check_bounds(self):
        for index in range(DIMENSION_SIZE):
            if self.location[index] > UB:
                self.location[index] = UB
            if self.location[index] < LB:
                self.location[index] = LB


def generate_fireflies():
    for i in range(POPULATION_SIZE):
        for j in range(DIMENSION_SIZE):
            Location_Array[j] = random.uniform(LB, UB)
        Firefly_List[i] = Firefly(Location_Array)
        Fitnesses[i] = Firefly_List[i].fitness


def calc_all_distances():
    for i in range(POPULATION_SIZE):
        Disntances[i] = update_distance(Firefly_List[i])


def update_distance(Firefly):
    inner_array = [0] * POPULATION_SIZE
    for i in range(POPULATION_SIZE):
        distance = 0
        for j in range(DIMENSION_SIZE):
            distance += (Firefly.location[j] - Firefly_List[i].location[j]) ** 2
        inner_array[i] = math.sqrt(distance)
    return inner_array

def run():
    for i in range(POPULATION_SIZE):
        moved = False
        for j in range(POPULATION_SIZE):
            distance = Disntances[i][j]
            if Firefly_List[i].light_intensity(distance) < Firefly_List[j].light_intensity(distance):
                new_firefly = Firefly(Firefly_List[i].location)
                new_firefly.update_location(Firefly_List[j], distance)
                new_firefly.fitness = new_firefly.update_fitness()
                moved = True
                if new_firefly.fitness < Firefly_List[i].fitness:
                    Firefly_List[i] = new_firefly
                    Fitnesses[i] = new_firefly.fitness
        if not moved:
            new_firefly = Firefly(Firefly_List[i].location)
            new_firefly.move_randomly()
            new_firefly.fitness = new_firefly.update_fitness()
            if new_firefly.fitness < Firefly_List[i].fitness:
                Firefly_List[i] = new_firefly
                Fitnesses[i] = new_firefly.fitness
        Firefly_List[i].check_bounds()
        new_firefly.fitness = Firefly_List[i].update_fitness()
        Disntances[i] = update_distance(Firefly_List[i])


def rank_fireflies(): #Global Minimum
    best_firefly = min(Fitnesses)
    print(best_firefly)
    Best.append(best_firefly)


# def rank_fireflies(): #Global Maximum
#     best_firefly = max(Fitnesses)
#     print(best_firefly)
#     Best.append(best_firefly)


def show_plot():
    plt.style.use('seaborn-whitegrid')
    ax = plt.axes()
    ax.plot(range(MAX_GENERATION), Best)
    ax.set_title('Optimal Solutions')
    ax.set_ylabel('Values')
    ax.set_xlabel('Generation')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.show()
    

generate_fireflies()
calc_all_distances()
# print(Fitnesses)
for gen in range(MAX_GENERATION):
    start_time = time.time()
    print("Starting Generation: {}".format(gen))
    run()
    elapsed_time = time.time() - start_time
    rank_fireflies()
    print("Generation Time: {}".format(elapsed_time))
show_plot()
# print(Fitnesses)