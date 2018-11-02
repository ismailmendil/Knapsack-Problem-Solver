from Knapsack import Knapsack
from KnapsackSolver import KnapsackSolver
from Benchmark_reader import BenchmarkReader
import sys
from timeit import default_timer as timer
from ukp_solving_method import ukp_solving_method
from ukp_instance import ukp_instance
from ukp_solver import ukp_solver
import csv
sys.setrecursionlimit(10000)

# constant declarations

BENCHMARK_FILE_PREFIX = 'exnsd'
BENCHMARK_FILE_POSTFIX = '.ukp'
BENCHMARK_DIR = '../../../assets/upk/'
BENCHMARK_FILES = [10, 16, 18, 20, 26]
STATS_PATH = '../stats/density_ordered_ugreedy_stats.csv'

stats = {
	'method_name': 'density oredered ugreedy algorithm',
	'bnckm_results': []
}
# variable declarations
# dictionay containing the name of the benchmark_file and the results of the solving process
def display_stats(stats):
	i = 1
	print('Beginning of the stats')
	print('Stats of the method:' + stats['method_name'])
	for stat in stats['bnckm_results']:
		print('Name of the instance: ' + stat['instance']['instance_name'])
		print('----------------------------------------------')
		print('Instance caracteristics: ')
		print('		number of item: ' + str(stat['instance']['number_items']))
		print('		size of the Knapsack: ' + str(stat['instance']['size_knapsack']))
		print('----------------------------------------------')
		print('Solving performance:')
		print('		Total time: ' + str(int(stat['performance']['total_time'] * 100000) / 100) + ' millisecs')
		print('		Sorting time: ' + str(int(stat['performance']['sorting_time'] * 10000) / 100)  + ' %')
		print('		Solving time: ' + str(int(stat['performance']['solving_time'] * 10000) / 100) + ' %')
		print('		Found value: ' + str(int(stat['performance']['found_value'] * 100)) + ' %')
		print('		Used capacity: ' + str(int(stat['performance']['used_capacity'] * 100)) + ' %')
		print(stat['performance']['solution'])
		print('---------------------------------------------------------------------------------------------------')
		print()
		print()

# It will iterate over all benckmarks and gather all stats in benckmarking_result


benckmarking_result = []

for iter in range(len(BENCHMARK_FILES)):
	br = BenchmarkReader(BENCHMARK_DIR + BENCHMARK_FILE_PREFIX + str(BENCHMARK_FILES[iter]) + BENCHMARK_FILE_POSTFIX)
	kp = ukp_instance(br.problem_values, br.capacity)

	solver = ukp_solver(kp, ukp_solving_method.GENETIC_ALGORHITMS_NAIVE)
	solver.solve()

	exact_prices = br.Solution['price']
	exact_quantity = br.Solution['nb']
	optimum = 0
	for i in range(len(br.Solution['nb'])):
		optimum = optimum + exact_prices[i] * exact_quantity[i]
	bnckm = {
		'sorting_time': solver.sorting_time / solver.total_time,
		'solving_time': solver.resolving_time / solver.total_time,
		'total_time': solver.total_time,
		'found_value': solver.get_total_value() / optimum,
		'used_capacity': solver.get_total_weight() / kp.capacity,
		'optimum': optimum,
		'solution': solver.solution
	}
	benckmarking_result.append(bnckm)
	stats['bnckm_results'].append({
		'instance': {
			'instance_name': BENCHMARK_FILE_PREFIX + str(BENCHMARK_FILES[iter]) + BENCHMARK_FILE_POSTFIX,
			'number_items': str(kp.number_items),
			'size_knapsack': str(kp.capacity)
		},
		'performance': bnckm
	})


'''
br = BenchmarkReader(BENCHMARK_DIR + BENCHMARK_FILE_PREFIX + '10' + BENCHMARK_FILE_POSTFIX)
kp = ukp_instance(br.problem_values, br.capacity)


solver = ukp_solver(kp, ukp_solving_method.DENSITY_ORDERED_UGREEDY)
solver.solve()


exact_prices = br.Solution['price']
exact_quantity = br.Solution['nb']
optimum = 0
for i in range(len(br.Solution['nb'])):
	optimum = optimum + exact_prices[i] * exact_quantity[i]

bnck_rslt = {
	'sorting_time': solver.sorting_time / solver.total_time,
	'solving_time': solver.resolving_time / solver.total_time,
	'total_time': solver.total_time,
	'found_value': solver.get_total_value() / optimum,
	'optimum': optimum
}

exact_prices = br.Solution['price']
exact_quantity = br.Solution['nb']
optimum = 0

print(br.Solution)
print(solver.solution)
print(bnck_rslt)
'''
# Ali's code for showing the real optimum and the one we calculated
'''
print("Total time: ", solver.total_time)
print("Sorting time fraction: ", solver.sorting_time / solver.total_time)
print("Solving time fraction: ", solver.resolving_time / solver.total_time)


print("The optimum value of this instance: ", optimum)
print("total value fraction given by the heuristic: ", (solver.get_total_value() / optimum))

print("total value given by the heuristic: ", solver.get_total_value())

print('index nb weight price')
cap = 0
final_taken = []
for i in range(len(solver.how_much_taken)):
    if solver.how_much_taken[i] > 0:
        if cap + solver.how_much_taken[i]*kp.weights[i] <= kp.capacity:
            cap += solver.how_much_taken[i]*kp.weights[i]
            final_taken.append(i)
            print(kp.sorted_objects[i][0],solver.how_much_taken[i], kp.weights[kp.sorted_objects[i][0]],kp.prices[kp.sorted_objects[i][0]])
print('found: ',cap,'for max capacity: ',kp.capacity)
print("Solution: ",br.Solution)
'''
# Displaying the stats on the terminal
display_stats(stats)
'''
# Wrting the stats in a file
with open(STATS_PATH, 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for item in benckmarking_result:
		writer.writerow([item['optimum']] + [item['found_value']] + [item['total_time']] +  [item['sorting_time']] + [item['solving_time']])
'''
