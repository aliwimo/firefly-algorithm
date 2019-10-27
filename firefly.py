import random
import math
import time

MAX_GENERATION = 50
POPULATION_SIZE = 90
DIMENSION_SIZE = 30
ALPHA = 0.2
BETA0 = 0
GAMMA = 1.0
TOP_LIMIT = 100
DOWN_LIMIT = -100

Location_Array = []
Firefly_List = []
Firefly_List0 = []


class Firefly:
    def __init__(self, location):
        self.location = []
        for index in range(DIMENSION_SIZE):
            self.location.append(location[index])

    def brightness(self):
        brightness = 0
        for index in range(DIMENSION_SIZE):
            brightness += self.location[index] ** 2
        return brightness

    # def brightness(self):
    #     x = self.location[0]
    #     y = self.location[1]
    #     return ((x + (2 * y) - 7) ** 2) + (((2 * x) + y - 5) ** 2)

    def light_intensity(self, other):
        return self.brightness() * math.exp((-1) * GAMMA * self.distance(other))

    def attractiveness(self, other):
        return BETA0 * math.exp((-1) * GAMMA * self.distance(other))

    def distance(self, other):
        distance = 0
        if other != self:
            for index in range(DIMENSION_SIZE):
                distance += (self.location[index] - other.location[index]) ** 2
        return math.sqrt(distance)

    def update_location(self, other):
        for index in range(DIMENSION_SIZE):
            epsilon = random.random() - 0.5
            rand = ALPHA * epsilon
            self.location[index] += self.attractiveness(other) * (other.location[index] - self.location[index]) + rand
            if self.location[index] > TOP_LIMIT:
                self.location[index] = TOP_LIMIT
            if self.location[index] < DOWN_LIMIT:
                self.location[index] = DOWN_LIMIT


def generate_fireflies():
    for i in range(POPULATION_SIZE):
        del Location_Array[:]
        for j in range(DIMENSION_SIZE):
            Location_Array.append(random.randint(DOWN_LIMIT, TOP_LIMIT))
        Firefly_List.append(Firefly(Location_Array))
        Firefly_List0.append(Firefly(Location_Array))



def run():
    for i in range(POPULATION_SIZE):
        for j in range(POPULATION_SIZE):
            if Firefly_List[i].brightness() > Firefly_List[j].light_intensity(Firefly_List[i]):
                new_firefly = Firefly(Firefly_List[i].location)
                new_firefly.update_location(Firefly_List[j])
                if new_firefly.brightness() < Firefly_List[i].brightness():
                    Firefly_List[i] = new_firefly


def rank_fireflies():
    best_firefly = Firefly_List[0]
    for i in range(POPULATION_SIZE):
        if Firefly_List[i].brightness() < best_firefly.brightness():
            best_firefly = Firefly_List[i]
    print(best_firefly.brightness())


generate_fireflies()
start_time = time.time()
for gen in range(MAX_GENERATION):
    print("Starting Generation: {}".format(gen))
    run()
    rank_fireflies()
elapsed_time = time.time() - start_time
print("Generation Time: {}".format(elapsed_time))
