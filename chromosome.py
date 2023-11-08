import random
import util
import math


class Chromosome:
    """ This class represents a Chromosome in the evolutionary algorithm for optimizing the placement of cellular towers for maximum user satisfaction.

    :param map_size: The size of the map.
    :type map_size: int
    :param mut_prob: The mutation probability.
    :type mut_prob: float
    :param recomb_prob: The recombination probability.
    :type recomb_prob: float
    :param blocks_population: A matrix of the population in each block of the map.
    :type blocks_population: List[List[int]]
    :param user_satisfaction_scores: A matrix of user satisfaction scores for each block of the map.
    :type user_satisfaction_scores: List[List[float]]
    :param user_satisfaction_levels: A list of user satisfaction levels.
    :type user_satisfaction_levels: List[float]
    :param tower_construction_cost: The cost of constructing a tower.
    :type tower_construction_cost: float
    :param tower_maintanance_cost: The cost of maintaining a tower.
    :type tower_maintanance_cost: float
    :param pop_sum: The total population on the map.
    :type pop_sum: float
    :param calc_fitness: A function that calculates the fitness of a chromosome.
    :type calc_fitness: Callable[[Chromosome], float]

    :ivar towers: A list of towers in the chromosome, represented as a tuple of x coordinate, y coordinate, radius, bandwidth, and population sum.
    :type towers: List[Tuple[int, int, float, float, int]]
    :ivar adj_id: A matrix where each element represents the id of the tower a neighborhood is connected to.
    :type adj_id: List[List[int]]
    :ivar mut_prob: The mutation probability.
    :type mut_prob: float
    :ivar recomb_prob: The recombination probability.
    :type recomb_prob: float
    :ivar map_size: The size of the map.
    :type map_size: int
    :ivar max_r: The maximum radius of a tower.
    :type max_r: float
    :ivar min_r: The minimum radius of a tower.
    :type min_r: float
    :ivar max_r_used: The max r we use for initialization.
    :type max_r_used: float
    :ivar blocks_population: A matrix of the population in each block of the map.
    :type blocks_population: List[List[int]]
    :ivar user_satisfaction_scores: A matrix of user satisfaction scores for each block of the map.
    :type user_satisfaction_scores: List[List[float]]
    :ivar user_satisfaction_levels: A list of user satisfaction levels.
    :type user_satisfaction_levels: List[float]
    :ivar tower_construction_cost: The cost of constructing a tower.
    :type tower_construction_cost: float
    :ivar tower_maintanance_cost: The cost of maintaining a tower.
    :type tower_maintanance_cost: float
    :ivar block_user_satisfaction_score: A matrix of the user satisfaction score for each block of the map based on the tower placement in the chromosome.
    :type block_user_satisfaction_score: List[List[float]]
    :ivar block_user_satisfaction_level: A matrix of the user satisfaction level for each block of the map based on the tower placement in the chromosome.
    :type block_user_satisfaction_level: List[List[int]]
    :ivar fitness: The fitness score of the chromosome.
    :type fitness: float
    :ivar pop_sum: The total population on the map.
    :type pop_sum: float
    :ivar constrcution_cost: The construction cost of the towers in the chromosome.
    :type constrcution_cost: float
    :ivar curr_user_satisfaction_score: The user satisfaction score based on the tower placement in the chromosome.
    :type curr_user_satisfaction_score: float
    :ivar user_satisfaction_penalty: The penalty for user dissatisfaction if the user satisfaction is zero.
    :type user_satisfaction_penalty: float
    :ivar epsilon: A small value used for comparing distance.
    :type epsilon: float
    :ivar calc_fitness: A function that calculates the fitness of a chromosome.
    :type calc_fitness: Callable[[Chromosome], float]
    :type sum_satisfaction: float
    """

    def __init__(self, map_size, mut_prob, recomb_prob, blocks_population, user_satisfaction_scores,
                 user_satisfaction_levels,
                 tower_construction_cost, tower_maintanance_cost, pop_sum, calc_fitness):
        # List of towers: (x, y, r, BW, population_sum)
        self.towers = []

        # Indicates each neighborhood is connected to which tower
        self.adj_id = [[-1 for i in range(map_size)] for j in range(map_size)]

        # Mutation probability
        self.mut_prob = mut_prob

        # Recombination probability
        self.recomb_prob = recomb_prob

        # The maximum bandwidth of the towers
        self.map_size = map_size
        self.max_r = (map_size ** 2 + map_size ** 2) ** 0.5
        self.min_r = (2 ** 0.5) / 2
        self.max_r_used = self.map_size / 5
        self.blocks_population = blocks_population
        self.user_satisfaction_scores = user_satisfaction_scores
        self.user_satisfaction_levels = user_satisfaction_levels
        self.tower_construction_cost = tower_construction_cost
        self.tower_maintanance_cost = tower_maintanance_cost
        self.block_user_satisfaction_score = [[0 for i in range(map_size)] for j in range(map_size)]
        self.block_user_satisfaction_level = [[0 for i in range(map_size)] for j in range(map_size)]
        self.fitness = 0
        self.pop_sum = pop_sum
        self.constrcution_cost = 0
        self.curr_user_satisfaction_score = 0
        self.user_satisfaction_penalty = 0
        self.epsilon = 1e-10
        self.calc_fitness = calc_fitness
        self.sum_satisfaction = 0
        self.init_chromosome()

    def init_chromosome(self):
        """
        Initialize a chromosome for the genetic algorithm by randomly selecting a number of towers and their positions on the map.
        The number of towers is determined by calculating the maximum and minimum sensor coverage area and choosing a random value in between them.
        Then, for each tower, a random x and y position is selected within the map_size.
        The tower radius is initially set to 0 and the tower tuple containing x, y, radius.

        If the calculate_fitness flag is set, the fitness of the chromosome is calculated using the calculate_fitness function.

        :param self: An instance of the Chromosome class.
        :type self: Chromosome

        :returns: None.
        :rtype: None
        """
        city_s = self.map_size ** 2
        max_sensor_coverage = (self.max_r_used ** 2) * math.pi
        min_sensor_coverage = (self.min_r ** 2) * math.pi
        num_tower = round(random.uniform((city_s / max_sensor_coverage), city_s / min_sensor_coverage))
        for _ in range(num_tower):
            x = random.uniform(0, self.map_size)
            y = random.uniform(0, self.map_size)
            r = 0
            tower = (x, y, r, 0, 0)
            self.towers.append(tower)

        if self.calc_fitness:
            self.calculate_fitness()

    def adj_tower(self, i, j):
        """
        A function to get the ID and distance of the nearest tower to a block by given coordinates.
        If there are multiple selections, the tower with the least population is returned.

        :param i: An integer representing the x coordinate of the block.
        :type i: int
        :param j: An integer representing the y coordinate of the block.
        :type j: int

        :return: A tuple containing the ID and the distance of the nearest tower to the given block.
        :rtype: tuple[int, float]
        """
        min_dist = 1000000
        min_dist_id = -1
        for tower_id, tower in enumerate(self.towers):
            dist = util.calculate_distance(tower, i + 0.5, j + 0.5)
            if (dist < min_dist - self.epsilon):
                min_dist_id = tower_id
                min_dist = dist
            elif (dist >= min_dist - self.epsilon and dist <= min_dist + self.epsilon ):
                if self.towers[tower_id][4] < self.towers[min_dist_id][4]:
                   min_dist_id = tower_id
                   min_dist = dist 
        return min_dist_id, min_dist

    def update_adj(self):
        """
        Update the adjacency between neighborhoods and towers.

        This method updates the adjacency between the neighborhoods and the towers, based on the distance between them.
        The algorithm calculates the minimum distance between each neighborhood and tower and associates the closest tower
        with that neighborhood. The method also updates the tower's range and adjusts its power based on the population it serves.

        :param self: An instance of the Chromosome class.
        :type self: Chromosome

        :returns: None.
        :rtype: None
        """
        #self.towers = sorted(self.towers, key=lambda x:x[0])
        # Set minimum range for all towers and set the population to zero
        for tower_id in range(len(self.towers)):
            self.towers[tower_id] = (self.towers[tower_id][0], self.towers[tower_id][1], 0, self.towers[tower_id][3], 0)

        # Associate each neighborhood with its closest tower
        for i in range(self.map_size):
            for j in range(self.map_size):
                candidate, min_dist = self.adj_tower(i, j)
                self.adj_id[i][j] = candidate
                self.towers[candidate] = (self.towers[candidate][0], self.towers[candidate][1]
                                          , max(self.towers[candidate][2], min_dist), self.towers[candidate][3],
                                          self.towers[candidate][4] + self.blocks_population[i][j])

        # Adjust the power of each tower based on the number of people it serves
        self.adjust_power()

    def mut_append(self):
        """
        Mutation operation that appends a new tower to the existing towers list with a probability of mutation probability.

        :param self: An instance of the Chromosome class.
        :type self: Chromosome

        :returns: None.
        :rtype: None
        """
        append_prob = random.uniform(0, 1)
        if append_prob <= self.mut_prob:
            x = random.uniform(0, self.map_size)
            y = random.uniform(0, self.map_size)
            r = 0
            tower = (x, y, r, 0, 0)
            self.towers.append(tower)

    def mut_relocation_tower(self):
        """
        Relocates towers randomly with a probability defined by mutation probability.

        The new position is calculated by adding a random value in the range [-1, 1] to the
        current x and y coordinates of the tower.

        :param self: An instance of the Chromosome class.
        :type self: Chromosome

        :returns: None.
        :rtype: None
        """
        for i in range(len(self.towers)):
            reloc_prob = random.uniform(0, 1)
            if reloc_prob <= self.mut_prob:
                add_x = random.uniform(-1, 1)
                add_y = random.uniform(-1, 1)
                new_x = self.towers[i][0] + add_x
                new_x = min(max(0, new_x), self.map_size)
                new_y = self.towers[i][1] + add_y
                new_y = min(max(0, new_y), self.map_size)
                self.towers[i] = (new_x, new_y, self.towers[i][2], self.towers[i][3], self.towers[i][4])

    def mut_pop(self):
        """Mutation operation that randomly removes a tower with a probability of mutation probability.

        :param self: An instance of the Chromosome class.
        :type self: Chromosome

        :returns: None.
        :rtype: None
            """
        pop_prob = random.uniform(0, 1)
        if pop_prob <= self.mut_prob and len(self.towers) > 1:
            pop_id = random.randint(0, len(self.towers) - 1)
            self.towers.pop(pop_id)

    def mutation(self):
        """Mutates the current population by performing the following operations:

           1. Mutates the location of some of the existing towers by adding a random offset to their x and y coordinates.
           2. Removes a tower from the population with a certain probability.
           3. Adds a new tower to the population with a certain probability.
           4. Recalculates the fitness of the population after the mutations have been applied.

           The probabilities of performing each of these operations are determined by the mutation probability attribute of
           the population object.

           :param self: An instance of the Chromosome class.
            :type self: Chromosome

            :returns: None.
            :rtype: None
           """
        self.mut_relocation_tower()
        self.mut_pop()
        self.mut_append()
        self.calculate_fitness()

    def adjust_power(self):
        """
            Adjusts the power of each tower based on the tower population and user satisfaction levels.

            :param self: An instance of the Chromosome class.
            :type self: Chromosome

            :returns: None.
            :rtype: None
            """
        for tower_id in range(len(self.towers)):
            tower_population = self.towers[tower_id][4]
            max_bw = util.calculate_max_BW(tower_population, self.user_satisfaction_levels[-1],
                                           self.towers[tower_id][2])
            mid_bw = util.calculate_max_BW(tower_population, self.user_satisfaction_levels[len(self.user_satisfaction_levels)//2],
                                            self.towers[tower_id][2])
            min_bw = util.calculate_max_BW(tower_population, self.user_satisfaction_levels[0], self.towers[tower_id][2])
            bw = min(max_bw,random.triangular(random.uniform(min_bw,10*mid_bw), max_bw*1.3, 2*max_bw)) if min_bw!= max_bw else max_bw

            new_tower = (
                self.towers[tower_id][0], self.towers[tower_id][1], self.towers[tower_id][2], bw,
                self.towers[tower_id][4])
            self.towers[tower_id] = new_tower

    def calculate_user_satisfaction_score(self, user_received_bandwidth):
        """
        Calculates the user satisfaction score based on the received bandwidth by the user.

        :param user_received_bandwidth: The bandwidth received by the user.
        :type user_received_bandwidth: float

        :return: The user satisfaction score corresponding to the received bandwidth.
        If the received bandwidth is below the lowest satisfaction level, then returns the user satisfaction penalty score. If the received bandwidth is above the highest satisfaction level, then returns the highest satisfaction score.
        :rtype: float
        """
        for i, user_satisfaction_level in enumerate(self.user_satisfaction_levels):
            if user_received_bandwidth < user_satisfaction_level:
                if i == 0:
                    return self.user_satisfaction_penalty
                return self.user_satisfaction_scores[i - 1]
        return self.user_satisfaction_scores[len(self.user_satisfaction_levels) - 1]

    def calculate_tower_blocks_population(self, tower_id):
        """
        Calculates the total population served by a given tower, which is the sum of the population
        of all the blocks within the tower's coverage range.

        :param tower_id: The ID of the tower to calculate the population served.
        :type tower_id: int
        :return: The total population served by the given tower.
        :rtype: int
        """
        tower_blocks_population = 0
        for r in range(len(self.adj_id)):
            for c in range(len(self.adj_id[r])):
                if self.adj_id[r][c] == tower_id:
                    tower_blocks_population += self.blocks_population[r][c]
        return tower_blocks_population

    def coverage_penalty(self):
        """
        Calculates the penalty for overlapping coverage area between towers.

        :return: The coverage penalty
         :rtype: float
        """
        penalty = 0
        for tower in self.towers:
            for tower1 in self.towers:
                if tower != tower1:
                    penalty += util.overlap_area(tower[0], tower[1], tower[2], tower1[0], tower1[1], tower1[2])

        penalty /= 2
        return penalty

    def calculate_fitness(self):
        """
        Calculates the fitness of the solution based on the current configuration of towers.

        :return: The fitness score of the solution
        :rtype: float

        Calculates the user satisfaction score, tower construction and maintenance cost, and tower coverage penalty.

        User satisfaction score is calculated for each block by the received bandwidth from the tower and the user's
        satisfaction level, which is determined by the user satisfaction levels set at initialization.

        Tower construction and maintenance cost is calculated based on the tower parameters and the costs of tower construction
        and maintenance.

        Tower coverage penalty is calculated based on the overlap area between towers.

        The fitness score is the multiplication of the user satisfaction score, tower construction and maintenance cost,
        coverage penalty, zero towers and user satisfaction overdose.
        """

        # Update the adjacency matrix of towers
        self.update_adj()

        # Initialize variables
        users_satisfaction_overdose = 0
        users_satisfaction = 0
        zero_towers = 0

        # Calculate user satisfaction score for each tower
        for i in range(len(self.adj_id)):
            for j in range(len(self.adj_id[i])):
                block_population = self.blocks_population[i][j]
                tower_id = self.adj_id[i][j]

                # Skip if there is no tower or the block is not connected to any tower
                if tower_id == -1 or tower_id >= len(self.towers):
                    continue

                # Calculate bandwidth and user satisfaction
                tower = self.towers[tower_id]
                tower_blocks_population = self.towers[tower_id][4]
                BW_prime = (tower[3] * block_population) / tower_blocks_population
                Bw = util.coverage(tower, i + 0.5, j + 0.5) * BW_prime

                #  Calculate user's satisfaction and overdose(when the bandwidth that the user is receiving is way too high)
                self.block_user_satisfaction_level[i][j] = Bw / block_population
                self.block_user_satisfaction_score[i][j] = self.calculate_user_satisfaction_score(Bw / block_population)
                users_satisfaction += (self.block_user_satisfaction_score[i][j] * block_population)
                users_satisfaction_overdose += max(0, self.block_user_satisfaction_level[i][j] -
                                                   self.user_satisfaction_levels[-1])

        # count zero towers which is the number of towers with no blocks
        for t in self.towers:
            if t[4] == 0:
                zero_towers += 1

        # Calculate towers cost
        towers_constrcution_cost = len(self.towers) * self.tower_construction_cost
        towers_maintanance_cost = 0
        for tower in self.towers:
            towers_maintanance_cost += (self.tower_maintanance_cost * tower[3])

        # Normalize 
        users_satisfaction_norm = (users_satisfaction - self.pop_sum * self.user_satisfaction_penalty) / (
                self.pop_sum * self.user_satisfaction_scores[-1]
                - self.pop_sum * self.user_satisfaction_penalty)
        max_BW = util.calculate_max_BW(self.pop_sum, self.user_satisfaction_levels[-1], self.max_r)
        towers_maintanance_cost_norm = 0
        if towers_maintanance_cost != 0:
            towers_maintanance_cost_norm = towers_maintanance_cost / (
                    max_BW * (self.map_size ** 2) * self.tower_maintanance_cost)

        towers_constrcution_cost_norm = towers_constrcution_cost / ((self.map_size ** 2) * self.tower_construction_cost)

        coverage_penalty = self.coverage_penalty() / (((len(self.towers) ** 2) / 4) * (self.max_r ** 2) * math.pi)
        users_satisfaction_overdose_norm = users_satisfaction_overdose / (self.pop_sum * max_BW)
        zero_towers_norm = zero_towers / (len(self.towers))
        # Maximization
        self.constrcution_cost = towers_maintanance_cost + towers_constrcution_cost
        self.curr_user_satisfaction_score = users_satisfaction_norm
        self.coverage = coverage_penalty
        self.overdose = users_satisfaction_overdose_norm
        self.sum_satisfaction = users_satisfaction
        negative = -1 if (
                (1 - (1e28) * users_satisfaction_overdose_norm) < 0 or 1 - (100) * coverage_penalty < 0) else 1
        # Calculating fitness value
        self.fitness = negative * (20 * (1 - towers_constrcution_cost_norm) * (1 - towers_maintanance_cost_norm)
                                   * (abs(1 - (100) * coverage_penalty)) * (1 - zero_towers_norm) * (
                                       abs(1 - (1e28) * users_satisfaction_overdose_norm)) * users_satisfaction_norm)
        
