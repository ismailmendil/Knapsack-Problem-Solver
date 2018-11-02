import math




def binarize_ukp_instance(amounts, weights, prices):
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

def debinarize_to_ukp_solution(mapping, active_bits):
        active_bits.sort()
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
                print('index item' + str(item['index']))
                while bit < totaling and index_bit < len(active_bits):
                    #amount += pow(2, item['size'] - (totaling - bit))
                    amount += pow(2, bit - (totaling - item['size']))
                    #print(amount)
                    index_bit += 1
                    if index_bit < len(active_bits):
                        bit = active_bits[index_bit]
                decoding.append({'index': item['index'], 'amount': amount})
                amount = 0
            index_mapping += 1
        return decoding

weights = [5, 8, 9, 6, 3, 2]
prices = [5, 8, 9, 6, 3, 2]
amounts = [7, 8, 9, 6, 3, 1]

'''
weights = [1, 2, 3, 4, 5]
prices = [6, 7, 8, 9, 6]
amounts = [1, 4, 3, 10, 7]
'''
transformed = binarize_ukp_instance(amounts, weights, prices)
#print(transformed)

print(transformed['mapping'])
bits_index = [1, 3, 8, 10, 11, 12]
print(debinarize_to_ukp_solution(transformed['mapping'], bits_index))
