import random
import math
import time

maxGeneration = 200
population = 10
dimensionSize = 3  # 2D
absorption = 1.0  # gamma absorption coefficient [0.1, 100]
randomness = 0.2  # alpha
attractiveness = 1  # beta at 0 distance
epsilon = 0.1  # between [-0.5, 0.5]
topLimit = 100
downLimit = -100

populationMap = []
distanceArray = []
lightIntensityR = []
attractivenessR = []


def generate_fireflies():
    for index in range(population):
        location = []
        for j in range(dimensionSize):
            location.append(random.randint(downLimit, topLimit))
        firefly_data = {
            "fireflyID": "firefly_{}".format(index),
            "location": location,
            "lightIntensity": 0
        }
        populationMap.append(firefly_data)


def objective_function():
    for index in range(population):
        my_sum = 0
        for j in range(dimensionSize):
            my_sum += math.pow(populationMap[index]["location"][j], 2)
        populationMap[index]["lightIntensity"] = my_sum


def calc_distance():
    for index in range(population):
        inner_array = []
        for j in range(population):
            distance = 0
            if index == j:
                distance = 0
            else:
                for k in range(dimensionSize):
                    distance += math.pow((populationMap[index]["location"][k] - populationMap[j]["location"][k]), 2)
                distance = math.sqrt(distance)
            inner_array.append(distance)
        distanceArray.append(inner_array)


def light_intensity_and_attractiveness():
    for index in range(population):
        light_intensity_inner_array = []
        attractiveness_r_inner_array = []
        for j in range(population):
            if index == j:
                light_intensity = 0
                attraction = 0
            else:
                light_intensity = populationMap[index]["lightIntensity"] * math.exp((-1 * absorption * math.pow(distanceArray[index][j], 2)))
                attraction = attractiveness / (1 + absorption * math.pow(distanceArray[index][j], 2))
            light_intensity_inner_array.append(light_intensity)
            attractiveness_r_inner_array.append(attraction)
        
        lightIntensityR.append(light_intensity_inner_array)
        attractivenessR.append(attractiveness_r_inner_array)


def move_towards(id1, id2):
    location1 = populationMap[id1]["location"]
    location2 = populationMap[id2]["location"]
    for index in range(dimensionSize):
        populationMap[id1]["location"][index] = location1[index] + (attractivenessR[id2][id1] * (location2[index] - location1[index])) + (randomness * epsilon)


def move_randomly(id1):
    for index in range(dimensionSize):
        populationMap[id1]["location"][index] = populationMap[id1]["location"][index] + (randomness * epsilon)


def run():
    for index in range(population):
        has_moved = False
        for j in range(population):
            if populationMap[index]["lightIntensity"] < lightIntensityR[index][j]:
                move_towards(index, j)
                has_moved = True
        if not has_moved:
            move_randomly(index)
        objective_function()
        calc_distance()
        light_intensity_and_attractiveness()


def display_map():
    print("<table style='border: 1px solid black'>")
    print("<tr style='border: 1px solid black'>")
    print("<th style='border: 1px solid black'>fireflyID</th>")
    print("<th style='border: 1px solid black'>location</th>")
    print("<th style='border: 1px solid black'>lightIntensity</th>")
    print("</tr>")
    for index in range(population):
        print("<tr style='border: 1px solid black'>")
        print("<th style='border: 1px solid black'>{}</th>".format(populationMap[index]["fireflyID"]))
        print("<th style='border: 1px solid black'>{}</th>".format(populationMap[index]["location"]))
        print("<th style='border: 1px solid black'>{}</th>".format(populationMap[index]["lightIntensity"]))
        print("</tr>")
    print("</table>")
    print("Population Table")


def display_distance_table():
    print("<table style='border: 1px solid black'>")
    print("<tr style='border: 1px solid black'>")
    print("<th style='border: 1px solid black'>fireflyID</th>")
    for index in range(population):
        print("<th style='border: 1px solid black'>{}</th>".format(index))
    print("</tr>")
    for index in range(population):
        print("<tr style='border: 1px solid black'>")
        print("<td style='border: 1px solid black'>{}</th>".format(index))
        for j in range(population):
            print("<td style='border: 1px solid black'>{}</th>".format(distanceArray[index][j]))
        print("</tr>")
    print("</table>")
    print("Distance Table")


def display_light_intensity_table():
    print("<table style='border: 1px solid black'>")
    print("<tr style='border: 1px solid black'>")
    print("<th style='border: 1px solid black'>fireflyID</th>")
    for index in range(population):
        print("<th style='border: 1px solid black'>{}</th>".format(index))
    print("</tr>")
    for index in range(population):
        print("<tr style='border: 1px solid black'>")
        print("<td style='border: 1px solid black'>{}</th>".format(index))
        for j in range(population):
            print("<td style='border: 1px solid black'>{}</th>".format(lightIntensityR[index][j]))
        print("</tr>")
    print("</table>")
    print("lightIntensityR Table")


def display_attractiveness_r_table():
    print("<table style='border: 1px solid black'>")
    print("<tr style='border: 1px solid black'>")
    print("<th style='border: 1px solid black'>fireflyID</th>")
    for index in range(population):
        print("<th style='border: 1px solid black'>{}</th>".format(index))
    print("</tr>")
    for index in range(population):
        print("<tr style='border: 1px solid black'>")
        print("<td style='border: 1px solid black'>{}</th>".format(index))
        for j in range(population):
            print("<td style='border: 1px solid black'>{}</th>".format(attractivenessR[index][j]))
        print("</tr>")
    print("</table>")
    print("attractivenessR Table")


generate_fireflies()
objective_function()
calc_distance()
light_intensity_and_attractiveness()
print("<h3>First Generation</h3>")
print("<h3>----------------</h3>")
display_map()
display_distance_table()
display_light_intensity_table()
display_attractiveness_r_table()

for i in range(maxGeneration):
    start_time = time.time()
    run()
    print("<h3>{}. Generation</h3>".format(i+2))
    print("<h3>----------------</h3>")
    display_map()
    elapsed_time = time.time() - start_time
    print("Elapsed Time: {}".format(elapsed_time))
