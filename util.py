import json
import numpy as np
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
    return len(city_map), city_map

def coverage(tower, x, y):
        sigma = np.array([[8, 0], [0, 8]])
        ty = np.array([tower[0],tower[1]])
        bx = np.array([x,y])
        return np.exp(-0.5 * (bx-ty) @ np.linalg.inv(sigma) @ (bx-ty).T)

def calculate_max_BW(map_size, max_pop, max_user_satisfaction_level):
    max_BW = map_size * map_size * max_user_satisfaction_level * max_pop / coverage((0,0,0), map_size-1, map_size-1)
    return max_BW
    
def calculate_k(population_size, iter):
    return round(2 + (population_size - 2) * iter / population_size)
    # return (population_size//2)
    #return 2
     