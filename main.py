import util
from evolutionary_algorithm import EvolutionaryAlgorithm as EA
import math

problem_config_file = 'problem_config.txt'
map_path = 'blocks_population.txt'
tower_construction_cost = 0
tower_maintanance_cost = []
user_satisfaction_levels = []
user_satisfaction_scores = []
map_size = 0
max_BW = 0
n_iter = 200
population_size = 50
mut_prob = 0.1
recomb_prob = 0.9
pop_avg = 0
pop_sum = 0

if __name__ == "__main__":
   problem_config = util.read_config(problem_config_file)
   tower_construction_cost = problem_config['tower_construction_cost']
   tower_maintanance_cost =problem_config['tower_maintanance_cost']
   user_satisfaction_levels = problem_config['user_satisfaction_levels']
   user_satisfaction_scores = problem_config['user_satisfaction_scores']
   map_size, blocks_population, pop_sum = util.read_map(map_path)
   
   for i in range(map_size):
      for j in range(map_size):
         pop_avg += blocks_population[i][j]
   pop_avg /= (map_size*map_size)
   #pop_avg = math.log(1+pop_avg)

   max_BW = util.calculate_max_BW(map_size, pop_sum,user_satisfaction_levels[-1])
   # print(max(map(max, blocks_population)), user_satisfaction_levels[-1])
   min_BW= util.calculate_min_BW(max_BW,map_size,user_satisfaction_levels[0],blocks_population)

   print(map_size, max_BW, min_BW,pop_sum)

   model = EA(n_iter, mut_prob, map_size, blocks_population, recomb_prob, tower_construction_cost,
                  tower_maintanance_cost, user_satisfaction_scores,user_satisfaction_levels, population_size, pop_avg, pop_sum)
   model.run()



