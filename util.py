import json
import numpy as np
import math

CURRENT_ITERATION = 0

def read_config(file_path):
    data = {}
    with open(file_path) as f:
        data = json.load(f)
    return data

def read_map(file_path):
    pop_sum = 0
    city_map = []

    with open(file_path) as f:
        for line in f:
            city_map.append(list(map(int,line.split(','))))
    
    for i in range(len(city_map)):
        for j in range(len(city_map)):
            pop_sum += city_map[j][i]

    return len(city_map), city_map, pop_sum

def coverage(tower, x, y):
        sigma = np.array([[8, 0], [0, 8]])
        ty = np.array([tower[0],tower[1]])
        bx = np.array([x,y])
        return np.exp(-0.5 * (bx-ty) @ np.linalg.inv(sigma) @ (bx-ty).T)

def calculate_max_BW(max_pop, max_user_satisfaction_level, r):
    return max_user_satisfaction_level * max_pop / coverage((0,0,0,0,0), 0, r)
  
def calculate_min_BW(map_size, min_user_satisfaction_level, blocks_population):
    min_BW = 0

    for i in range(map_size):
        for j in range(map_size):
            min_BW +=  blocks_population[i][j] * min_user_satisfaction_level / coverage((i + 0.5,j + 0.5,0,0,0), i + 0.5, j + 0.5)
    
    return min_BW / (map_size**2)

def calculate_distance(tower, i, j):
    return math.dist([tower[0], tower[1]], [i, j])

def calculate_std(max_r):
    return max((2 ** 0.5)/2, max_r * 1 / (CURRENT_ITERATION + 1))

def overlap_area(x1, y1, r1, x2, y2, r2):
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    if d > r1 + r2:
        return 0
    if d < abs(r1 - r2):
        return math.pi * min(r1, r2)**2
    if r1 == 0 or d == 0 or r2 == 0:
        return 0
    a1 = math.acos((r1**2 + d**2 - r2**2) / (2 * r1 * d))
    a2 = math.acos((r2**2 + d**2 - r1**2) / (2 * r2 * d))
    return r1**2 * a1 + r2**2 * a2 - d * r1 * math.sin(a1)

def calculate_k(population_size, iter):
    return population_size // 10
     