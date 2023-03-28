import util
problem_config_file = 'problem_config.txt'
map_path = 'blocks_population.txt'

if __name__ == "__main__":
   problem_config = util.read_config(problem_config_file)
   city_map =  util.read_map(map_path)