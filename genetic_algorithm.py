import util
import numpy as np
import random
from  chromosome import Chromosome

class GeneticAlgorithm:
    def __init__(self, n_iter, mut_prob, map_size, max_BW, blocks_population, recomb_prob, tower_construction_cost,
                  tower_maintanance_cost, user_satisfaction_scores,user_satisfaction_levels, population_size):
        self.iterations_no = n_iter
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
        self.max_BW = max_BW
        self.current_iter = 0
    
    # Random initialization
    def init_population(self):
        for _ in range(self.population_size):
            young_pop = Chromosome(self.map_size, self.mut_prob, self.recomb_prob, self.max_BW, self.blocks_population, self.user_satisfaction_scores, self.user_satisfaction_levels, 
                self.tower_construction_cost, self.tower_maintanance_cost)
            self.population.append(young_pop)

    def tournament_selection(self,  k):
        parents = random.choices(self.population, k)
        parents = sorted(parents, key=lambda agent: agent.fitness, reverse=True)
        bestparent = parents[0]
        return bestparent

    def roulette_wheel_selection(self):
        # Computes the totallity of the population fitness
        population_fitness = sum([chromosome.fitness for chromosome in self.population])
        
        # Computes for each chromosome the probability 
        chromosome_probabilities = [chromosome.fitness/population_fitness for chromosome in self.population]
        
        # Selects one chromosome based on the computed probabilities
        return np.random.choice(self.population, p=chromosome_probabilities)
    
    # Fitness proportional-roulette wheel/ Tournament selection
    def parent_selection(self):
        parents = []
        for _ in range(self.population_size):
            parents.append(self.tournament_selection(util.calculate_k(self.population_size, self.current_iter)))
        return parents
    
    def recombination(self):
        youngs = []
        for _ in range(self.population_size/2):
            parents = random.choices(self.parent_selection(), 2)
            young1 = Chromosome(self.map_size, self.mut_prob, self.recomb_prob, self.max_BW, self.blocks_population, self.user_satisfaction_scores, self.user_satisfaction_levels, 
                self.tower_construction_cost, self.tower_maintanance_cost)
            young1.towers.clear()
            young2 = Chromosome(self.map_size, self.mut_prob, self.recomb_prob, self.max_BW, self.blocks_population, self.user_satisfaction_scores, self.user_satisfaction_levels, 
                self.tower_construction_cost, self.tower_maintanance_cost)
            young2.towers.clear()
            for i in range(self.map_size):
                for j in range(self.map_size):
                    pc = random.uniform(0, 1)
                    if pc <= self.recomb_prob:
                        if parents[0].towers[parents[0].adj_id[i][j]] not in young1.towers:
                            young1.towers.append(parents[0].towers[parents[0].adj_id[i][j]])
                        young1.adj_id[i][j] = young1.towers.index(parents[0].towers[parents[0].adj_id[i][j]])
        
                        if parents[1].towers[parents[1].adj_id[i][j]] not in young2.towers:
                            young2.towers.append(parents[1].towers[parents[1].adj_id[i][j]])
                        young2.adj_id[i][j] = young2.towers.index(parents[1].towers[parents[1].adj_id[i][j]])
                    else:
                        if parents[0].towers[parents[0].adj_id[i][j]] not in young2.towers:
                            young2.towers.append(parents[0].towers[parents[0].adj_id[i][j]])
                        young2.adj_id[i][j] = young2.towers.index(parents[0].towers[parents[0].adj_id[i][j]])
        
                        if parents[1].towers[parents[1].adj_id[i][j]] not in young1.towers:
                            young1.towers.append(parents[1].towers[parents[1].adj_id[i][j]])
                        young1.adj_id[i][j] = young1.towers.index(parents[1].towers[parents[1].adj_id[i][j]])
            
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
        mpl = self.population + youngs
        mpl = sorted(mpl, key=lambda agent: agent.fitness, reverse=True)
        mpl = mpl [:self.population_size].copy()
        return mpl
    
    # No improvement in last 20 generation
    def is_terminated(self):
        pass

    def run(self):
        for _ in range(self.n_iter):
            self.init_population()
            youngs = self.recombination()
            youngs = self.all_mutation(youngs)
            self.population = self.survival_selection(youngs).copy()
            self.current_iter += 1
            print(f"current iteration: {self.current_iter}",
                  f", best fitness: {sorted(self.population, key=lambda agent: agent.fitness, reverse=True)[0].fitness}")
            print("--------------------------------------------------------------------------------------------------------------")

    

