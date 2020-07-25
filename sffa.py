import numpy as np
import benchmark

POP_SIZE    = 90
DIM_SIZE    = 30
MAX_GEN     = 50
ALPHA       = 0.2
BETA_MIN    = 1.0
GAMMA       = 1.0
BOUND       = 100

LB = -BOUND * np.ones(DIM_SIZE)
UB = BOUND * np.ones(DIM_SIZE)

OBJ_FUNC    = benchmark.sphere

# total number of function evaluations
eval_num = POP_SIZE * MAX_GEN

Best = []

# generate fireflies
def generate_fireflies():
    return np.random.uniform(0, 1, (POP_SIZE, DIM_SIZE)) * (UB - LB) + LB

# def objective_function(firefly):
#     return sum(x ** 2 for x in firefly)

def calculate_fitnesses(fireflies):
    return [OBJ_FUNC(i) for i in fireflies]
    
def find_limits(fireflies):
    for i in range(POP_SIZE):
        np.where(fireflies[i] > BOUND, BOUND, fireflies[i])
        np.where(fireflies[i] < -BOUND, -BOUND, fireflies[i])

def update_alpha(alpha):
    delta = 1 - (10 ** (-4) / 0.9) ** (1 / MAX_GEN)
    return (1 - delta) * alpha


fireflies = generate_fireflies()

for gen in range(MAX_GEN):
    
    ALPHA = update_alpha(ALPHA)

    fitnesses = calculate_fitnesses(fireflies)
    sorted_index = np.argsort(fitnesses)
    fitnesses.sort()

    # temp_fireflies = fireflies.copy()

    fireflies = fireflies[sorted_index, :]

    fireflies_old = fireflies.copy()
    fitnesses_old = fitnesses.copy()

    best_firefly = fireflies[0]
    best_fitness = fitnesses[0]

    scale = abs(UB - LB)
    for i in range(POP_SIZE):
        for j in range(POP_SIZE):
            
            distance = np.sqrt(np.sum((fireflies[i] - fireflies_old[j]) ** 2))
            if (fitnesses[i] > fitnesses_old[j]):
                beta0 = 1
                beta = (beta0 - BETA_MIN) * np.exp(-GAMMA * (distance ** 2)) + BETA_MIN
                tmpf = ALPHA * (np.random.rand(DIM_SIZE) - 0.5) * scale
                
                fireflies[i] = fireflies[i] * (1 - beta) + fireflies[j] * beta + tmpf

    find_limits(fireflies)
    # fireflies = find_bounds(fireflies)


    Best.append(best_fitness)
    print(f'Gen: {gen} - Best: {best_fitness}')
print(f'Gen: {gen} - Best: {best_fitness}')


print('end of run')

