import random
import util
import math

class Chromosome:
    def __init__(self, map_size, mut_prob, recomb_prob, blocks_population, user_satisfaction_scores, user_satisfaction_levels, 
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
        self.max_r = (map_size**2 + map_size**2)**0.5
        self.min_r = (2**0.5)/2
        self.max_r_std = self.map_size / 5 
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
        self.init_chromosome()

    def init_chromosome(self):
        city_s = self.map_size ** 2
        max_sensor_coverage = (self.max_r_std ** 2) * math.pi
        min_sensor_coverage = (self.min_r ** 2) * math.pi
        num_tower = round(random.uniform((city_s/max_sensor_coverage),city_s/min_sensor_coverage))
        for _ in range(num_tower):
            x = random.uniform(0,self.map_size) 
            y = random.uniform(0,self.map_size)
            r = 0
            tower = (x, y, r, 0, 0)
            self.towers.append(tower)

        if self.calc_fitness:
            self.calculate_fitness()
    
    def adj_tower(self,i,j):
        min_dist = 1000000
        min_dist_id = -1
        for tower_id, tower in enumerate(self.towers):
            dist = util.calculate_distance(tower, i+0.5, j+0.5)
            if  (dist < min_dist - self.epsilon) :
                min_dist_id = tower_id
                min_dist = dist
        return min_dist_id, min_dist
            
    def update_adj(self):
        for tower_id in range(len(self.towers)):
            self.towers[tower_id] = (self.towers[tower_id][0],self.towers[tower_id][1],self.min_r,self.towers[tower_id][3],0)

        for i in range(self.map_size):
            for j in range(self.map_size):
                candidate,min_dist=  self.adj_tower(i,j)
                self.adj_id[i][j] = candidate
                self.towers[candidate] = (self.towers[candidate][0],self.towers[candidate][1]
                                          ,max(self.towers[candidate][2], min_dist),self.towers[candidate][3], self.towers[candidate][4] + self.blocks_population[i][j])


        self.adjust_power()

    def mut_append(self):
        append_prob = random.uniform(0,1)
        if append_prob <= self.mut_prob:
            x = random.uniform(0,self.map_size) 
            y = random.uniform(0,self.map_size)
            r = 0
            tower = (x, y, r, 0, 0)
            self.towers.append(tower)
            
    
    def mut_relocation_tower(self):
        for i in range(len(self.towers)):
            reloc_prob = random.uniform(0,1)
            if reloc_prob <= self.mut_prob:
                std = util.calculate_std(self.max_r)
                add_x = random.uniform(-1,1) 
                add_y = random.uniform(-1,1)
                new_x = self.towers[i][0] + add_x
                new_x = min(max(0,new_x),self.map_size)
                new_y = self.towers[i][1] + add_y
                new_y = min(max(0,new_y),self.map_size)
                self.towers[i] = (new_x,new_y,self.towers[i][2], self.towers[i][3], self.towers[i][4])


    def mut_pop(self):
        pop_prob = random.uniform(0,1)
        if pop_prob <= self.mut_prob and len(self.towers) > 1:
            pop_id = random.randint(0,len(self.towers)-1)
            self.towers.pop(pop_id)


    def mutation(self):
        self.mut_relocation_tower()
        self.mut_pop()
        self.mut_append()
        self.calculate_fitness()
    

    def adjust_power(self):
        for tower_id in range(len(self.towers)):
            tower_population = self.towers[tower_id][4]
            max_bw = util.calculate_max_BW(tower_population,self.user_satisfaction_levels[-1],self.towers[tower_id][2])
            min_bw = util.calculate_max_BW(tower_population,self.user_satisfaction_levels[0],self.towers[tower_id][2])
            bw = max(random.uniform(min_bw + random.uniform(0,10*min_bw),max_bw),max_bw)
            new_tower = (self.towers[tower_id][0],self.towers[tower_id][1],self.towers[tower_id][2], bw, self.towers[tower_id][4])
            self.towers[tower_id] = new_tower

    
    def calculate_user_satisfaction_score(self, user_received_bandwidth):    
        for i, user_satisfaction_level in enumerate(self.user_satisfaction_levels):
            if user_received_bandwidth < user_satisfaction_level:
                if i == 0:
                    return self.user_satisfaction_penalty
                return self.user_satisfaction_scores[i-1]
        return self.user_satisfaction_scores[len(self.user_satisfaction_levels)-1]
        
    def calculate_tower_blocks_population(self, tower_id):
        tower_blocks_population = 0
        for r in range(len(self.adj_id)):
                for c in range(len(self.adj_id[r])):
                    if self.adj_id[r][c] == tower_id:
                        tower_blocks_population += self.blocks_population[r][c]
        return tower_blocks_population
    
    def coverage_penalty(self):
        penalty = 0
        for tower in self.towers:
            for tower1 in self.towers:
                if tower != tower1:
                    penalty += util.overlap_area(tower[0],tower[1],tower[2], tower1[0],tower1[1],tower1[2])

        penalty /= 2
        return penalty

    def calculate_fitness(self):
        self.update_adj()
        users_satisfaction_overdose = 0
        users_satisfaction = 0
        zero_towers = 0
        for i in range(len(self.adj_id)):
            for j in range(len(self.adj_id[i])):
                block_population = self.blocks_population[i][j]
                tower_id = self.adj_id[i][j]
                if tower_id == -1 or tower_id >= len(self.towers):
                    continue
                tower = self.towers[tower_id]

                tower_blocks_population = self.towers[tower_id][4]
                BW_prime = (tower[3] * block_population) / tower_blocks_population
                Bw = util.coverage(tower, i + 0.5, j + 0.5) * BW_prime

                #  Calculate user's satisfaction
                self.block_user_satisfaction_level[i][j] =  Bw / block_population
                self.block_user_satisfaction_score[i][j] = self.calculate_user_satisfaction_score(Bw / block_population)
                users_satisfaction += (self.block_user_satisfaction_score[i][j] * block_population)
                users_satisfaction_overdose += max(0, self.block_user_satisfaction_level[i][j] - self.user_satisfaction_levels[-1])
    
        #count zero towers
        for t in self.towers:
            if t[4] == 0:
                zero_towers +=1
        # Calculate towers cost
        towers_constrcution_cost = len(self.towers) * self.tower_construction_cost
        towers_maintanance_cost  = 0
        for tower in self.towers:
            towers_maintanance_cost += (self.tower_maintanance_cost * tower[3])
        
        # Normalize 
        users_satisfaction_norm = (users_satisfaction - self.pop_sum*self.user_satisfaction_penalty) / ( self.pop_sum * self.user_satisfaction_scores[-1] 
                                                                            - self.pop_sum*self.user_satisfaction_penalty)
        max_BW = util.calculate_max_BW(self.pop_sum,self.user_satisfaction_levels[-1],self.max_r)
        towers_maintanance_cost_norm = 0
        if towers_maintanance_cost != 0:
            towers_maintanance_cost_norm = towers_maintanance_cost / (max_BW * (self.map_size ** 2) * self.tower_maintanance_cost)
        
        towers_constrcution_cost_norm = towers_constrcution_cost / ((self.map_size ** 2) * self.tower_construction_cost)

        coverage_penalty = self.coverage_penalty() / (((len(self.towers)**2)/4) * (self.max_r**2)*math.pi)
        users_satisfaction_overdose_norm = users_satisfaction_overdose / (self.pop_sum * max_BW) 
        zero_towers_norm = zero_towers / (len(self.towers))
        # Maximization
        self.constrcution_cost = towers_maintanance_cost + towers_constrcution_cost
        self.constrcution_cost_norm = (towers_maintanance_cost_norm + towers_maintanance_cost_norm)/2
        self.curr_user_satisfaction_score = users_satisfaction_norm
        self.coverage = coverage_penalty 
        self.overdose = users_satisfaction_overdose_norm
        negative = -1 if ((1-(1e28)*users_satisfaction_overdose_norm) < 0 or 1 - (100)*coverage_penalty <0) else 1 
        self.fitness = negative * (20 * (1 - towers_constrcution_cost_norm) * (1 - towers_maintanance_cost_norm) 
                        * (abs(1 - (100)*coverage_penalty)) * (1-zero_towers_norm) * (abs(1-(1e28)*users_satisfaction_overdose_norm)) * users_satisfaction_norm)