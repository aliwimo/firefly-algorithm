import numpy as np

# ========================================================
# Sphere Function
# Dimensions: d, xi = [-5.12, 5.12], for all i = 1, .., d.
# Global minimum 0 at (0, ..., 0)
# ========================================================
def sphere(X):
    return sum(x ** 2 for x in X)

# ========================================================
# Bohchevsky Function
# Dimensions: 2, xi = [-100, 100], for all i = 1, .., d.
# Global minimum 0 at (0, ..., 0)
# ========================================================
def Bohchevsky(X):
    x1 = X[0]
    x2 = X[1]
    eq = (x1 ** 2) + 2 * (x2 ** 2) - 0.3 * np.cos((3 * np.pi * x1) + (4 * np.pi * x2)) + 0.3
    return eq

# ========================================================
# Booth Function
# Dimensions: 2, xi = [-10, 10], for all i = 1, .., d.
# Global minimum 0 at (1, 3)
# ========================================================
def Booth(X):
    x1 = X[0]
    x2 = X[1]
    eq = ((x1 + 2 * x2 - 7) ** 2) + ((2 * x1 + x2 - 5) ** 2)
    return eq

# ========================================================
# Drop-Wave Function
# Dimensions: 2, xi = [-5.12, 5.12], for all i = 1, 2.
# Global minimum -1 at (0, 0)
# ========================================================
def drop_wave(X):
    up = 1 + np.cos(12 * np.sqrt((X[0] ** 2) + (X[1] ** 2)))
    down = 0.5 * ((X[0] ** 2) + (X[1] ** 2)) + 2
    return -up / down


# ========================================================
# Eggholder Function
# Dimensions: 2, xi = [-512, 512], for all i = 1, 2.
# Global minimum -959.6407 at (512, 404.2319)
# ========================================================
def eggholder(X):
    x1 = X[0]
    x2 = X[1]
    eq1 = -(x2 + 47) * np.sin(np.sqrt(abs(x2 + (x1 / 2) + 47)))
    eq2 = x1 * np.sin(np.sqrt(abs(x1 - (x2 + 47))))
    return eq1 - eq2




def dont_know(X):
    abs_list = list(map(abs, X))
    inner_sum = np.sum(abs_list)
    inner_prod = np.prod(abs_list)
    return inner_sum + inner_prod