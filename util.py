import json
import numpy as np
import math
curr_iter = 0
def read_config(file_path):
    data = {}
    with open(file_path) as f:
        data = json.load(f)
    return data

def read_map(file_path):
    city_map = []
    with open(file_path) as f:
        for line in f:
            city_map.append(list(map(int,line.split(','))))
    pop_sum = 0
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
    max_BW = max_user_satisfaction_level * max_pop / coverage((0,0,0,0,0), 0, r)
    return max_BW

def calculate_min_BW(max_BW, map_size, min_user_satisfaction_level, blocks_population):
    min_BW = max_BW
    for i in range(map_size):
        for j in range(map_size):
            min_BW = min(min_BW, blocks_population[i][j] * min_user_satisfaction_level / coverage((i,j,0,0,0), i, j))
    return min_BW

def calculate_distance(tower,i,j):
        return ((tower[0]-i)**2 + (tower[1]-j)**2)**0.5

def calculate_std(max_r):
    std = max((2**0.5)/2, max_r * 1 / (curr_iter+1))
    return std

def overlap_area(x1, y1, r1, x2, y2, r2):
    # distance between the centers of the circles
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    # check if the circles are completely separate
    if d > r1 + r2:
        return 0
    
    # check if one circle is completely inside the other
    if d < abs(r1 - r2):
        return math.pi * min(r1, r2)**2
    
    # calculate the overlap area using the formula for the area of a segment of a circle
    if r1 == 0 or d == 0 or r2 == 0:
        return 0
    a1 = math.acos((r1**2 + d**2 - r2**2) / (2 * r1 * d))
    a2 = math.acos((r2**2 + d**2 - r1**2) / (2 * r2 * d))
    return r1**2 * a1 + r2**2 * a2 - d * r1 * math.sin(a1)

def calculate_k(population_size, iter):
    return round(2 + (population_size - 2) * iter / population_size)
    #return (population_size//2)
    #return 5
     