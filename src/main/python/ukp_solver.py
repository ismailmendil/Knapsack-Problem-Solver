from timeit import default_timer as timer
import math
import random
from ukp_solving_method import ukp_solving_method
from ukp_instance import ukp_instance

class ukp_solver:
	sorting_time = 0
	resolving_time = 0
	sorting_time = 0
	total_time = 0
	how_much_taken = []
	solution = []


	def __init__(self, ukp_instance, solving_method):
		self.sorting_time = 0
		self.resolving_time = 0
		self.sorting_time = 0
		self.total_time = 0
		self.how_much_taken = []
		self.solution = []
		self.ukp_instance = ukp_instance
		self.solving_method = solving_method
		self.how_much_taken = [0] * len(self.ukp_instance.sorted_objects)

	def solve(self):

		if self.solving_method == ukp_solving_method.DENSITY_ORDERED_UGREEDY:
			start = timer() # start the sorting of objects according to the decreasing of efficiencies
			self.ukp_instance.sort_by_efficiency()
			end = timer()
			self.sorting_time = end - start


			start = timer() # start the solving procedure
			self.density_ordered_ugreedy()
			end = timer()
			self.resolving_time = end - start
			self.total_time = self.sorting_time + self.resolving_time
		'''
	print('this sorting time: ' + str(self.sorting_time))
	print('this resolving time: ' + str(self.resolving_time))
	print('this total time: ' + str(self.total_time))
		'''
		if self.solving_method == ukp_solving_method.WEIGHT_ORDERED_UGREEDY:
			start = timer() # start the solving procedure
			self.weight_ordered_ugreedy()
			end = timer()
			self.sorting_time = 0
			self.resolving_time = end - start
			self.total_time = self.sorting_time + self.resolving_time

		if self.solving_method == ukp_solving_method.GENETIC_ALGORHITMS_NAIVE:
			start = timer()
			self.solve_ga_naive()
			end = timer()
			self.sorting_time = 0
			self.resolving_time = end - start
			self.total_time = self.sorting_time + self.resolving_time


	def get_total_value(self):

		total_price = 0
		'''
		for i in range(len(self.how_much_taken)):
			if (total_weight + self.how_much_taken[i] * self.ukp_instance.weights[i] < self.ukp_instance.capacity):
				total_price = total_price + self.how_much_taken[i] * self.ukp_instance.prices[i]
				total_weight = total_weight + self.how_much_taken[i] * self.ukp_instance.weights[i]
		return total_price
		'''
		'''
		for i in range(len(self.how_much_taken)):
				total_price += self.how_much_taken[i] * self.ukp_instance.prices[i]
		'''
		for elm in self.solution:
			total_price += elm['quantity'] * self.ukp_instance.prices[elm['index']]
		return total_price

	def get_total_weight(self):

		total_weight = 0

		for elm in self.solution:
			total_weight += elm['quantity'] * self.ukp_instance.weights[elm['index']]
		return total_weight

	def density_ordered_ugreedy(self):
		remaining_capacity = self.ukp_instance.capacity
		for i in range(len(self.ukp_instance.weights)):
			if (remaining_capacity >= self.ukp_instance.weights[i]):
				index = self.ukp_instance.sorted_objects[i][0]
				quantity = int(remaining_capacity / self.ukp_instance.weights[index])
				# self.how_much_taken[self.ukp_instance.sorted_objects[i][0]] = int(remaining_capacity / self.ukp_instance.weights[self.ukp_instance.sorted_objects[i][0]])
				if quantity != 0:
					self.solution.append({'index': index, 'quantity': quantity})
					remaining_capacity = remaining_capacity - quantity * self.ukp_instance.weights[index]

	def weight_ordered_ugreedy(self):

		index_min_weight = self.ukp_instance.arg_min_weight()
		#print(int(self.ukp_instance.capacity / self.ukp_instance.weights[index_min_weight]))
		#self.how_much_taken[index_min_weight] = int(self.ukp_instance.capacity / self.ukp_instance.weights[index_min_weight])
		self.solution.append({'index': index_min_weight, 'quantity': int(self.ukp_instance.capacity / self.ukp_instance.weights[index_min_weight])})


	def mut1(self):
		pass

	def solve_ga_naive(self):
		translated = self.ukp_instance.binarize_ukp_instance()
		items = []
		for i in range(len(translated['weights'])):
			items.append({'index': i, 'price': translated['prices'][i], 'weight': translated['weights'][i]})
		solution_binarized = self.ga_schema(items, self.ukp_instance.capacity)
		solution_binarized.sort()
		self.solution = self.ukp_instance.debinarize_to_ukp_solution(translated['mapping'], solution_binarized)

	# items  is an array of json objects that have 3 properties: 'index', 'weight', 'price'
	def ga_schema(self, items, capacity):
		ITER_NUM = 10
		ITEM_INITIAL_NUM = int(len(items) / 1000)
		GENERATION_INITIAL_SIZE = 6
		GENERATION_SIZE = 4
		SELECTION_PROBABILITY = 0.7
		CROSS_PROBABILITY = 0.7
		MUTATION_PROBABILITY = 0.1
		REPLACEMENT_PROBABILITY = 0.7

		population = []
		children = []
		# compute the fitness for each chromosome
		for i in range(len(items)):
			items[i]['efficiency'] = items[i]['price'] / items[i]['weight']

		# Initiliaze the population: We build 'GENERATION_INITIAL_SIZE' random solutions each has 'ITEM_INITIAL_NUM' items
		# Since it is 0-1 knapsack problem, taking the item means that the flag is set at 1, conversely if it is not taken, the flag is 0
		'''
				population = [ {'total_price': 0,
								'total_weight': 0,
								'Solution': [items[random.randint(0, len(items))] for i itotal_price += item['price']n random.sample(range(len(items)), ITEM_INITIAL_NUM)]} \
		'''
		for i in range(GENERATION_INITIAL_SIZE):
			total_weight = 0
			total_price = 0
			chromosome = []
			for item in random.sample(items, ITEM_INITIAL_NUM):
				total_price += item['price']
				total_weight += item['weight']
				chromosome.append(item)
			population.append({
				'total_price': total_price,
				'total_weight': total_weight,
				'chromosome': chromosome
			})


		# Iterate over time
		for t in range(ITER_NUM):
			# Select probabilisticly the good sub_population

			#population.sort(key = lambda pair: self.fitness(pair), reverse=True)
			#population = population[0:GENERATION_SIZE]

			population = self.select_population(population, GENERATION_SIZE, SELECTION_PROBABILITY)
			# Cross probabilisticly between chromosomes
			cross_product = self.split_into_couples(population)
			'''
			for i in range(int(GENERATION_SIZE / 2)):
				couple = random.sample(population, 2)
				cross_product.append(couple)
				# Eliminate the couple just seleleted for the next crossing
				population = [x for x in population if x not in couple]
			population = []
			'''
			for cp in cross_product:
				population.append(cp[0])
				population.append(cp[1])
				if random.random() > CROSS_PROBABILITY:
					population.append(self.crossover_midpoint(cp[0], cp[1]))


			# Mutate the chromosomes with the right probability

				mutated_population = []
				for elm in population:
					if random.random() > MUTATION_PROBABILITY:
						chromosome = self.mutate(elm, capacity, items)
					mutated_population.append(elm)
				# Replace by newer population with the right probability
				mutated_population.sort(key = lambda pair: self.fitness(pair), reverse=True)

				population = mutated_population[::]

		taken_items = self.best_solution(population)['chromosome']

		return [x['index'] for x in taken_items]
	def split_into_couples(self, population):
		positions = random.sample(range(len(population)), len(population))
		i = 0
		couples = []
		while i < len(population):
			couples.append([population[positions[i]], population[positions[i + 1]]])
			i += 2
		return couples

	def fitness(self, chromosome):

		return chromosome['total_price']

	def select_population(self, population_input, CHROMOSOME_NUM, SELECTION_PROBABILITY):
		#print(len(population_input))
		#print(population_input)
		population = random.sample(population_input, 4)
		#population = population_input[0: CHROMOSOME_NUM]
		return population

	def best_solution(self, population):
		better = []
		its_value = 0
		for elm in population:
			if elm['total_price'] > its_value:
				better = elm
				its_value = elm['total_price']
		return better

	def crossover_midpoint(self, parent11, parent22,):
		parent1 = parent11['chromosome']
		parent2 = parent22['chromosome']
		child1 = parent1[0: int(len(parent1) / 2)] + parent2[int(len(parent2) / 2):]
		child2 = parent1[0: int(len(parent2) / 2)] + parent2[int(len(parent1) / 2):]
		child = child1 + child2
		# remove doubling in child
		child_unique = []
		for c in child:
			if c not in child_unique:
				child_unique.append(c)

		total_price = 0
		total_weight = 0
		for c in child:
			total_price += c['price']
			total_weight += c['weight']
		return {
			'total_weight': total_weight,
			'total_price': total_price,
			'chromosome': child
		}

	def mutate(self, chromosome, capacity, all_genes):

		while chromosome['total_weight'] > capacity:
			index = self.min_property(chromosome['chromosome'], 'efficiency')
			chromosome['total_weight'] -= chromosome['chromosome'][index]['weight']
			chromosome['total_price'] -= chromosome['chromosome'][index]['price']
			del chromosome['chromosome'][index]
		all_genes_copy = all_genes[::]
		continues = True

		while continues:
			i = self.min_property(all_genes_copy, 'weight')
			if continues:
				print([x['index'] for x in chromosome['chromosome']])
				continues = False
			if all_genes_copy[i]['index'] in [x['index'] for x in chromosome['chromosome']]:
				del all_genes_copy[i]
			else:
				if chromosome['total_weight'] + all_genes_copy[i]['weight'] > capacity:
					break
					chromosome['chromosome'].append(all_genes_copy[i])
					chromosome['total_price'] += all_genes_copy[i]['price']
					chromosome['total_weight'] += all_genes_copy[i]['weight']
					del all_genes_copy[i]
			continues = False


		return chromosome

	def min_property(self, array, property):
		min = math.inf
		index_min = 0
		index = 0
		for elm in array:
			if elm[property] < min:
				min = elm[property]
				index_min = index
			index += 1


		return index_min

	def value_ordered_ugreedy(self):
		pass

	def ugreedy_solver(self):
		pass
