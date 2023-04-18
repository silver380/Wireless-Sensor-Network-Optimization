import json
import numpy as np
import math

curr_iter = 0
n_iter = 200


def read_config(file_path):
    """
    Reads the configuration data from a JSON file.

    :param file_path: The file path of the JSON configuration file.
    :type file_path: str

    :return: A dictionary containing the configuration data.
    :rtype: dict
    """
    data = {}
    with open(file_path) as f:
        data = json.load(f)
    return data


def read_map(file_path):
    """
    Reads a city map from the given file path and calculates the population sum.

    :param file_path: A string representing the path to the file containing the city map.
    :type file_path: str

    :return: A tuple containing the size of the city map (length of each side), the city map as a 2D list, and the total population sum.
    :rtype: tuple[int, list[list[int]], int]

    """
    city_map = []
    with open(file_path) as f:
        for line in f:
            city_map.append(list(map(int, line.split(','))))
    pop_sum = 0
    for i in range(len(city_map)):
        for j in range(len(city_map)):
            pop_sum += city_map[j][i]
    return len(city_map), city_map, pop_sum


def coverage(tower, x, y):
    """
    Calculate the Gaussian coverage of a tower at a given point (x,y) on the map.

    :param tower: A tuple containing the x and y coordinates of the tower.
    :type tower: tuple[int, int]
    :param x: The x coordinate of the point on the map.
    :type x: int
    :param y: The y coordinate of the point on the map.
    :type y: int

    :rtype: float
    :return: The Gaussian coverage of the tower at the given point (x,y) on the map.

    """
    sigma = np.array([[8, 0], [0, 8]])
    ty = np.array([tower[0], tower[1]])
    bx = np.array([x, y])
    return np.exp(-0.5 * (bx - ty) @ np.linalg.inv(sigma) @ (bx - ty).T)


def calculate_max_BW(max_pop, max_user_satisfaction_level, r):
    """
    Calculate the maximum available bandwidth for a tower with maximum population, maximum user satisfaction level, and given radius.

    :param max_pop: The maximum population that a tower can cover.
    :type max_pop: int
    :param max_user_satisfaction_level: The maximum user satisfaction level that a tower can provide.
    :type max_user_satisfaction_level: float
    :param r: The radius of the tower's coverage area.
    :type r: float

    :return: The maximum bandwidth for the tower.
    :rtype: float

    """
    max_BW = max_user_satisfaction_level * max_pop / coverage((0, 0, 0, 0, 0), 0, r)
    return max_BW


def calculate_distance(tower, i, j):
    """
        Calculate the Euclidean distance between the given tower and the block with coordinates (i, j).

        :param tower: A tuple of (x, y, r, bandwidth, population) representing the tower.
        :type tower
        :param i: The x coordinate of the block.
        :type i: int
        :param j: The y coordinate of the block.
        :type j: int
        :return: The Euclidean distance between the tower and the block.
        :rtype: float
        """
    return ((tower[0] - i) ** 2 + (tower[1] - j) ** 2) ** 0.5


def overlap_area(x1, y1, r1, x2, y2, r2):
    """

    Calculate the overlap area between two circles.

    :param x1: The x-coordinate of the center of the first circle.
    :type x1: float
    :param y1: The y-coordinate of the center of the first circle.
    :type y1: float
    :param r1: The radius of the first circle.
    :type r1: float
    :param x2: The x-coordinate of the center of the second circle.
    :type x2: float
    :param y2: The y-coordinate of the center of the second circle.
    :type y2: float
    :param r2: The radius of the second circle.
    :type r2: float
    :return: The overlap area between the two circles.
    :rtype: float

    """
    # distance between the centers of the circles
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # check if the circles are completely separate
    if d > r1 + r2:
        return 0

    # check if one circle is completely inside the other
    if d < abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2

    # calculate the overlap area using the formula for the area of a segment of a circle
    if r1 == 0 or d == 0 or r2 == 0:
        return 0
    a1 = math.acos((r1 ** 2 + d ** 2 - r2 ** 2) / (2 * r1 * d))
    a2 = math.acos((r2 ** 2 + d ** 2 - r1 ** 2) / (2 * r2 * d))
    return r1 ** 2 * a1 + r2 ** 2 * a2 - d * r1 * math.sin(a1)


def calculate_k(population_size, iter):

    """
    Calculates the value of k (the number of solutions that will be selected for tournament selection) for recombination .

    :param population_size: The size of the population in the genetic algorithm.
    :type population_size: int
    :param iter: The current iteration number of the genetic algorithm.
    :type iter: int
    :return: The value of k.
    :rtype: int
    """

    return max(2, population_size * iter // n_iter)

    #return (population_size//5)
    
    #return 5
