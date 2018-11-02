import math
class ukp_instance:
	weights = []
	prices = []
	# it contains the efficiencies and its indexes
	sorted_objects = []


	def __init__(self, objects, capacity):
		self.objects = objects
		self.capacity = capacity
		self.number_items = len(self.objects)
		i = 0
		for obj in objects:
			self.weights.append(obj[0])
			self.prices.append(obj[1])
			self.sorted_objects.append((
				i,
				obj[1] / obj[0]
			)) # efficiency is the ratio of the price to the weight
			i = i + 1
	def binarize_ukp_instance(self):
	  weights = self.weights
	  prices = self.prices
	  amounts = [int(self.capacity / w) for w in weights]
	  ws = []
	  ps = []
	  mapping = []
	  for obj in range(len(amounts)):
		  max_exponent = int(math.log(amounts[obj], 2)) + 1
		  for i in range(max_exponent):
			  ws.append(weights[obj] * pow(2, i))
			  ps.append(prices[obj] * pow(2, i))
		  mapping.append({'index': obj, 'size': max_exponent})
	  return {
		'mapping': mapping,
		'weights': ws,
		'prices': ps
	  }
	def debinarize_to_ukp_solution(self, mapping, active_bits):
		index_bit = 0
		index_mapping = 0
		totaling = 0
		decoding = []
		amount = 0
		bit = active_bits[index_bit]
		while index_mapping < len(mapping) and index_bit < len(active_bits):
			item = mapping[index_mapping]
			totaling += item['size']
			if bit < totaling:
				#print('index item' + str(item['index']))
				while bit < totaling and index_bit < len(active_bits):
					#amount += pow(2, item['size'] - (totaling - bit))
					amount += pow(2, bit - (totaling - item['size']))
					#print(amount)
					index_bit += 1
					if index_bit < len(active_bits):
						bit = active_bits[index_bit]
				decoding.append({'index': item['index'], 'quantity': amount})
				amount = 0
			index_mapping += 1
		return decoding
	def max_weight(self):
		return max(self.weights)
	def min_weight(self):
		return min(weights)

	def arg_min_weight(self):
		index_min = 0
		i = 0
		min = self.weights[0]
		for item in self.weights:
			i = i + 1
			if item < min:
				min = item
				index_min = i
		return index_min

	def max_prices(self):
		return max(prices)

	def min_prices():
		return min(prices)

	def sort_by_efficiency(self):
		self.sorted_objects.sort(key=lambda pair:pair[1], reverse=True)
