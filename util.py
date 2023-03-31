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
    pop_sum = 0
    for i in range(len(city_map)):
        for j in range(len(city_map)):
            pop_sum += city_map[j][i]
    return len(city_map), city_map, pop_sum

def coverage(tower , x, y):
        sigma = np.array([[8, 0], [0, 8]])
        ty = np.array([tower[0],tower[1]])
        bx = np.array([x,y])
        return np.exp(-0.5 * (bx-ty) @ np.linalg.inv(sigma) @ (bx-ty).T)


# def coverage(a, b, x, y):
#     sigma = np.array([[8, 0], [0, 8]])
#     ty = np.array([a, b])
#     bx = np.array([x, y])
#     return np.exp(-0.5 * (bx - ty) @ np.linalg.inv(sigma) @ (bx - ty).T)

def calculate_max_BW(map_size, max_pop, max_user_satisfaction_level):
    max_BW = max_user_satisfaction_level * max_pop / coverage((0,0,0), map_size/4, map_size/4)
    return max_BW

def calculate_min_BW(max_BW, map_size, min_user_satisfaction_level, blocks_population):
    min_BW = max_BW
    for i in range(map_size):
        for j in range(map_size):
            min_BW = min(min_BW, blocks_population[i][j] * min_user_satisfaction_level / coverage((i,j,0), i, j))
    return min_BW
     
def calculate_k(population_size, iter):
    return round(2 + (population_size - 2) * iter / population_size)
    #return (population_size//2)
    #return 5

if __name__ == "__main__":
    print(calculate_max_BW(10, 1000, 3))