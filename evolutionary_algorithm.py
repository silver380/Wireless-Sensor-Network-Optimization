import util
import numpy as np
import random
from chromosome import Chromosome
import sys


class EvolutionaryAlgorithm:
    """
    A class representing an Evolutionary Algorithm for optimizing the placement of communication towers.

    :param n_iter: The number of iterations the algorithm will run.
    :type n_iter: int
    :param map_size: The size of the map on which the optimization is being performed.
    :type map_size: int
    :param mut_prob: The probability of a mutation occurring during the algorithm.
    :type mut_prob: float
    :param recomb_prob: The probability of a recombination occurring during the algorithm.
    :type recomb_prob: float
    :param blocks_population: A 2D list representing the population of each block on the map.
    :type blocks_population: list
    :param tower_construction_cost: The cost of constructing a new tower.
    :type tower_construction_cost: float
    :param tower_maintanance_cost: The cost of maintaining a tower.
    :type tower_maintanance_cost: float
    :param user_satisfaction_scores: A list of scores representing user satisfaction scores.
    :type user_satisfaction_scores: list
    :param user_satisfaction_levels: A list of levels representing user satisfaction levels.
    :type user_satisfaction_levels: list
    :param population_size: The size of the population of candidate solutions.
    :type population_size: int
    :param pop_sum: The total population of the map.
    :type pop_sum: int
    ;type prev_best_ans: float
    ;typr not_improved: float

    :ivar n_iter: The number of iterations the algorithm will run.
    :ivar map_size: The size of the map on which the optimization is being performed.
    :ivar mut_prob: The probability of a mutation occurring during the algorithm.
    :ivar recomb_prob: The probability of a recombination occurring during the algorithm.
    :ivar blocks_population: A 2D list representing the population of each block on the map.
    :ivar tower_construction_cost: The cost of constructing a new tower.
    :ivar tower_maintanance_cost: The cost of maintaining a tower.
    :ivar user_satisfaction_scores: A list of scores representing user satisfaction scores.
    :ivar user_satisfaction_levels: A list of levels representing user satisfaction levels.
    :ivar population: A list representing the current population of candidate solutions.
    :ivar population_size: The size of the population of candidate solutions.
    :ivar current_iter: The current iteration of the algorithm.
    :ivar pop_sum: The total population of the map.
    :ivar fitness_avg: The average fitness score of the current population.
    :ivar fitness_history: A list of fitness scores for each iteration of the algorithm.
    :ivar prev_best_ans: best found answer
    :ivar not_improved: number of iterations with no improvement in average fitness
    """
    def __init__(self, n_iter, mut_prob, map_size, blocks_population, recomb_prob, tower_construction_cost,
                 tower_maintanance_cost, user_satisfaction_scores, user_satisfaction_levels, population_size, pop_sum, prev_best_ans):
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
        self.pop_sum = pop_sum
        self.fitness_avg = 0
        self.fitness_history = []
        self.prev_best_ans = prev_best_ans
        self.not_improved = 0

    # Random initialization
    def init_population(self):
        """
        Randomly initializes the population of the evolutionary algorithm.

        :return: None
        :raises: None
        """
        for _ in range(self.population_size):
            young_pop = Chromosome(self.map_size, self.mut_prob, self.recomb_prob, self.blocks_population,
                                   self.user_satisfaction_scores, self.user_satisfaction_levels,
                                   self.tower_construction_cost, self.tower_maintanance_cost, self.pop_sum, True)
            self.population.append(young_pop)

    # Fitness Tournament selection
    def tournament_selection(self, tour_pop, k):
        """
        A function that selects the best parent from a subset of the population using the tournament selection method.

        :param tour_pop: A list of candidate chromosomes to compete for selection.
        :type tour_pop: list
        :param k: The number of chromosomes to select for the tournament.
        :type k: int
        :return: The best chromosome selected from the tournament.
        :rtype: Chromosome
        """
        parents = random.sample(tour_pop, k=k)
        parents = sorted(parents, key=lambda agent: agent.fitness, reverse=True)
        bestparent = parents[0]
        return bestparent

    def parent_selection(self):
        """
            Selects parents for the next generation using tournament selection.

            :return: A list of parent agents for recombination.
            :rtype: list
            """
        parents = []
        for _ in range(self.population_size):
            best_parent = self.tournament_selection(self.population,
                                                    util.calculate_k(len(self.population), self.current_iter))
            parents.append(best_parent)

        return parents

    def recombination(self, mating_pool):
        """
        Performs single-point crossover between pairs of parents selected from a given mating pool.

        :param mating_pool: A list of candidate parents.
        :type mating_pool: list

        :return: A list of offspring chromosomes resulting from the recombination process.
        :rtype: list

        """
        youngs = []
        for _ in range(self.population_size // 2):
            parents = random.choices(mating_pool, k=2)
            young1 = Chromosome(self.map_size, self.mut_prob, self.recomb_prob, self.blocks_population,
                                self.user_satisfaction_scores, self.user_satisfaction_levels,
                                self.tower_construction_cost, self.tower_maintanance_cost, self.pop_sum, False)

            young2 = Chromosome(self.map_size, self.mut_prob, self.recomb_prob, self.blocks_population,
                                self.user_satisfaction_scores, self.user_satisfaction_levels,
                                self.tower_construction_cost, self.tower_maintanance_cost, self.pop_sum, False)
            # TODO: conditions for number of towers
            prob = random.uniform(0, 1)
            if prob <= self.recomb_prob:
                crossover_point = random.randint(1, max(min(len(parents[0].towers), len(parents[1].towers)) - 1, 1))
                young1.towers = parents[0].towers[:crossover_point].copy() + parents[1].towers[crossover_point:].copy()
                young2.towers = parents[1].towers[:crossover_point].copy() + parents[0].towers[crossover_point:].copy()
            else:
                young1.towers = parents[0].towers.copy()
                young2.towers = parents[1].towers.copy()

            youngs.append(young1)
            youngs.append(young2)
        return youngs

    def all_mutation(self, youngs):
        """
        This function performs mutation on the given chromosomes.

        :param youngs: A list of Chromosome objects on which mutation will be performed.
        :type youngs: list
        :return: A list of Chromosome objects after mutation.
        :rtype: list

        """
        for young in youngs:
            young.mutation()

        return youngs


    def survival_selection(self, youngs):
        """
        Returns the new population after combining the current population with the youngs using the mu + lambda method.

        :param youngs: A list of new chromosomes generated from the current population by recombination and mutation.

        :return: A list of chromosomes representing the new population after survival selection.
        """
        mpl = self.population.copy() + youngs
        mpl = sorted(mpl, key=lambda agent: agent.fitness, reverse=True)
        mpl = mpl[:self.population_size].copy()
        return mpl

    # No improvement in last 20 generation
    def is_terminated(self, prev):
        """
        The method checks whether the algorithm should terminate based on the condition that there was no improvement in the fitness of the best chromosome in the last 20 generations.
        
        :return: A boolean value indicating whether the algorithm should terminate or not. True if the algorithm should terminate, False otherwise.

        """
        avg = self.fitness_avg / ((self.current_iter+1) * self.population_size)
        if avg > prev + 1e-10:
            self.not_improved = 0
        elif (avg > prev - 1e-10) and (avg < prev + 1e-10):
            self.not_improved +=1
        
        return self.not_improved < 20

    def calculate_fitness_avg(self):
        """
                Calculate the average fitness of the current population.

                :return: None
                """
        self.fitness_avg = 0
        for pop in self.population:
            self.fitness_avg += pop.fitness

    def run(self):
        """
            Runs the genetic algorithm for a specified number of iterations.

            :return: List of the average fitness of each generation.
            :rtype: list
            """
        self.init_population()
        prev_avg = 0

        for _ in range(self.n_iter):
            parents = self.parent_selection().copy()
            youngs = self.recombination(parents).copy()
            youngs = self.all_mutation(youngs).copy()
            self.population = self.survival_selection(youngs).copy()
            self.calculate_fitness_avg()
            self.current_iter += 1
            util.curr_iter += 1
            best_current = sorted(self.population, key=lambda agent: agent.fitness, reverse=True)[0]
            print(f"current iteration: {self.current_iter} / {self.n_iter}",
                  f", best fitness: {best_current.fitness}")
            print(f'towers: {len(best_current.towers)}, construction cost: {best_current.constrcution_cost / 1e7}')
            print(f'user satisfaction norm = {best_current.curr_user_satisfaction_score}, user satisfaction score: {best_current.sum_satisfaction} / {best_current.pop_sum * best_current.user_satisfaction_scores[-1]} overlap :{best_current.coverage}')
            print(f'overdose: {best_current.overdose}, fitness_avg: {self.fitness_avg / (self.population_size)}')
            print(
                "------------------------------------------------------------------------------------------------------")
            self.fitness_history.append(self.fitness_avg / (self.population_size))
            prev_avg = self.fitness_avg / (self.population_size)

        ans = sorted(self.population, key=lambda agent: agent.fitness, reverse=True)[0]

        # save the best yet found answer
        
        if(ans.fitness > self.prev_best_ans):
            original_stdout = sys.stdout
            with open('towers.txt', 'w') as f:
                sys.stdout = f
                for tower in ans.towers:
                    print(*tower)
                sys.stdout = original_stdout

            with open('adj.txt', 'w') as f:
                sys.stdout = f
                for adj in ans.adj_id:
                    print(*adj)
                sys.stdout = original_stdout

            with open('user_satisfaction_score.txt', 'w') as f:
                sys.stdout = f
                for sat_score in ans.block_user_satisfaction_score:
                    print(*sat_score)
                sys.stdout = original_stdout

            with open('user_satisfaction_level.txt', 'w') as f:
                sys.stdout = f
                for sat_level in ans.block_user_satisfaction_level:
                    print(*sat_level)
                sys.stdout = original_stdout

        return ans.fitness, ans.constrcution_cost, len(ans.towers), ans.sum_satisfaction, self.fitness_history
