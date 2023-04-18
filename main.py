import util
import numpy as np
import time
from evolutionary_algorithm import EvolutionaryAlgorithm as EA

problem_config_file = 'problem_config.txt'
map_path = 'blocks_population.txt'
tower_construction_cost = 0
tower_maintanance_cost = []
user_satisfaction_levels = []
user_satisfaction_scores = []
map_size = 0
max_BW = 0
n_iter = util.n_iter # max number of iterations, change it in util.py
population_size = 50
mut_prob = 0.1
recomb_prob = 0.9
pop_avg = 0
pop_sum = 0
histories = []
best_ans = 0
best_ans_price = 0
best_ans_satisfaction = 0
best_towers = 0

if __name__ == "__main__":
   #reading map and config
   problem_config = util.read_config(problem_config_file)
   tower_construction_cost = problem_config['tower_construction_cost']
   tower_maintanance_cost =problem_config['tower_maintanance_cost']
   user_satisfaction_levels = problem_config['user_satisfaction_levels']
   user_satisfaction_scores = problem_config['user_satisfaction_scores']
   map_size, blocks_population, pop_sum = util.read_map(map_path)
   
   
   max_BW = util.calculate_max_BW(map_size, pop_sum,user_satisfaction_levels[-1])
   start_time = time.time()
   print(f"map size= {map_size}, max needed BW= {max_BW}, population sum = {pop_sum}, recomb_prob= {recomb_prob}, mut_prob= {mut_prob}")
   ea = EA(n_iter, mut_prob, map_size, blocks_population, recomb_prob, tower_construction_cost,
                  tower_maintanance_cost, user_satisfaction_scores,user_satisfaction_levels, population_size, pop_sum, best_ans)
   
   ans, ans_price, ans_towers, ans_satisfaction, history_i = ea.run()
   histories.append(history_i)
   if ans > best_ans:
      best_ans = ans
      best_ans_price = ans_price
      best_towers = ans_towers
      best_ans_satisfaction = ans_satisfaction

   end_time = time.time()
   runtime = end_time - start_time
   print("Runtime: {:.2f} seconds".format(runtime))
   print(f"best found answer has {best_ans} fitness, {best_towers} towers, {best_ans_price} price and {best_ans_satisfaction} user satisfaction")
   histories = np.array(histories)   
   np.savetxt("histories.csv", histories,
               delimiter = ",")
