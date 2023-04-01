import util
import numpy as np
import random
from  chromosome import Chromosome
import sys

class GeneticAlgorithm:
    def __init__(self, n_iter, mut_prob, map_size, blocks_population, recomb_prob, tower_construction_cost,
                  tower_maintanance_cost, user_satisfaction_scores,user_satisfaction_levels, population_size, pop_avg, pop_sum):
        self.n_iter = n_iter
        self.map_size = map_size
        self.mut_prob = mut_prob
        self.recomb_prob = recomb_prob
        self.blocks_population = blocks_population
        self.tower_construction_cost = tower_construction_cost
        self.tower_maintanance_cost = tower_maintanance_cost
        self.user_satisfaction_scores = user_satisfaction_scores
        self.user_satisfaction_levels = user_satisfaction_levels
        self.population = []
        self.population_size = population_size
        self.current_iter = 0
        self.pop_avg = pop_avg
        self.pop_sum = pop_sum
    
    # Random initialization
    def init_population(self):
        for _ in range(self.population_size):
            young_pop = Chromosome(self.map_size, self.mut_prob, self.recomb_prob, self.blocks_population, self.user_satisfaction_scores, self.user_satisfaction_levels, 
                self.tower_construction_cost, self.tower_maintanance_cost, self.pop_avg, self.pop_sum)
            self.population.append(young_pop)

    def roulette_wheel_selection(self):
        # Computes the totallity of the population fitness
        population_fitness = sum([chromosome.fitness for chromosome in self.population])
        
        # Computes for each chromosome the probability 
        chromosome_probabilities = [chromosome.fitness/population_fitness for chromosome in self.population]
        
        # Selects one chromosome based on the computed probabilities
        return np.random.choice(self.population, p=chromosome_probabilities)
    
    # Fitness proportional-roulette wheel/ Tournament selection
    def tournament_selection(self, tour_pop, k):
        parents = random.choices(tour_pop, k=k)
        parents = sorted(parents, key=lambda agent: agent.fitness, reverse=True)
        bestparent = parents[0]
        return bestparent
    
    def parent_selection(self):
        parents = []
        candidate_parents = self.population.copy()
        for _ in range(self.population_size):
            best_parent = self.tournament_selection(candidate_parents,util.calculate_k(len(candidate_parents), self.current_iter))
            parents.append(best_parent)
            # if (len(candidate_parents) > 2):
            #     candidate_parents.remove(best_parent)
        return parents
    
    def recombination(self):
        youngs = []
        for _ in range(self.population_size//2):
            parents = random.choices(self.parent_selection(), k=2)
            young1 = Chromosome(self.map_size, self.mut_prob, self.recomb_prob, self.blocks_population, self.user_satisfaction_scores, self.user_satisfaction_levels, 
                self.tower_construction_cost, self.tower_maintanance_cost, self.pop_avg, self.pop_sum)
            
            young2 = Chromosome(self.map_size, self.mut_prob, self.recomb_prob, self.blocks_population, self.user_satisfaction_scores, self.user_satisfaction_levels, 
                self.tower_construction_cost, self.tower_maintanance_cost, self.pop_avg, self.pop_sum)
            crossover_point = random.randint(1, min(len(parents[0].towers), len(parents[1].towers)) - 1)
            young1.towers = parents[0].towers[:crossover_point].copy() + parents[1].towers[crossover_point:].copy()
            young2.towers = parents[1].towers[:crossover_point].copy() + parents[0].towers[crossover_point:].copy()
            young1.calculate_fitness()
            young2.calculate_fitness()
            youngs.append(young1)
            youngs.append(young2)
        return youngs
    
    def all_mutation(self, youngs):
        for young in youngs:
            young.mutation()

        return youngs

    # mu + lambda
    def survival_selection(self, youngs):
        #TODO :k
        k = 1
        mpl = sorted(self.population.copy(), key=lambda agent: agent.fitness, reverse=True)[:self.population_size//k].copy() + youngs
        mpl = sorted(mpl, key=lambda agent: agent.fitness, reverse=True)
        mpl = mpl [:self.population_size].copy()
        return mpl
    
    # No improvement in last 20 generation
    def is_terminated(self):
        pass

    def run(self):
        self.init_population()
        for _ in range(self.n_iter):
            youngs = self.recombination().copy()
            youngs = self.all_mutation(youngs).copy()
            self.population = self.survival_selection(youngs).copy()
            self.current_iter += 1
            util.curr_iter += 1
            best_current = sorted(self.population, key=lambda agent: agent.fitness, reverse=True)[0]
            print(f"current iteration: {self.current_iter} / {self.n_iter}",
                  f", best fitness: {best_current.fitness}")
            print(f'towers: {len(best_current.towers)}, construction cost = {best_current.constrcuted_cost}, user satisfaction = {best_current.user_satisfied}')
            print("--------------------------------------------------------------------------------------------")
            
        ans =  sorted(self.population, key=lambda agent: agent.fitness, reverse=True)[0]
        
        original_stdout = sys.stdout
        with open('towers.txt', 'w') as f:
            sys.stdout = f
            for tower in ans.towers:
                print(tower)
            sys.stdout = original_stdout
        
        with open('adj.txt', 'w') as f:
            sys.stdout = f
            for adj in ans.adj_id:
                print(adj)
            sys.stdout = original_stdout
        
        with open('user_satisfaction_score.txt', 'w') as f:
            sys.stdout = f
            for sat_score in ans.block_user_satisfaction_score:
                print(sat_score)
            sys.stdout = original_stdout
        
        with open('user_satisfaction_level.txt', 'w') as f:
            sys.stdout = f
            for sat_level in ans.block_user_satisfaction_level:
                print(sat_level)
            sys.stdout = original_stdout

    

