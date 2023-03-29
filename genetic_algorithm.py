import util
import numpy as np

class GeneticAlgorithm:
    def __init__(self, n_iter, mut_prob, recomb_prob, tower_construction_cost,
                  tower_maintanance_cost, user_satisfaction_scores,user_satisfaction_levels, population_size, offsprings):
        self.iterations_no = n_iter
        self.mut_prob = mut_prob
        self.recomb_prob = recomb_prob
        self.tower_construction_cost = tower_construction_cost
        self.tower_maintanance_cost = tower_maintanance_cost
        self.user_satisfaction_scores = user_satisfaction_scores
        self.user_satisfaction_levels = user_satisfaction_levels
        self.population_size = population_size
        self.offsprings = offsprings
        self.init_population()
    
    # Random initialization
    def init_population(self):
        # self.population = 
        pass

    # Fitness proportional-roulette wheel 
    def parent_selection(self):
        pass

    def roulette_wheel_selection(self):
        # Computes the totallity of the population fitness
        population_fitness = sum([chromosome.fitness for chromosome in self.population])
        
        # Computes for each chromosome the probability 
        chromosome_probabilities = [chromosome.fitness/population_fitness for chromosome in self.population]
        
        # Selects one chromosome based on the computed probabilities
        return np.random.choice(self.population, p=chromosome_probabilities)
    
    # میو + لاندا
    def survival_selection(self):
        pass

    # No improvement in last 20 generation
    def is_terminated(self):
        pass

    

