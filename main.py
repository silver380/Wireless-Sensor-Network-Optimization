import util
problem_config_file = 'problem_config.txt'
map_path = 'blocks_population.txt'
tower_construction_cost = -1
tower_maintanance_cost = []
user_satisfaction_levels = []
user_satisfaction_scores = []
map_size = 0
max_BW = 0
if __name__ == "__main__":
   problem_config = util.read_config(problem_config_file)
   tower_construction_cost = problem_config['tower_construction_cost']
   tower_maintanance_cost =problem_config['tower_maintanance_cost']
   user_satisfaction_levels = problem_config['user_satisfaction_levels']
   user_satisfaction_scores = problem_config['user_satisfaction_scores']
   map_size, blocks_population = util.read_map(map_path)
   max_BW = util.calculate_max_BW(map_size, max(map(max, blocks_population)),user_satisfaction_levels[-1])


