class Knapsack:
    capacity = 0
    weights = []
    prices = []
    index = []
    def __init__(self,capacity,weights_and_prices):
        self.capacity = capacity
        for elem in weights_and_prices:
            self.weights.append(elem[0])
            self.prices.append(elem[1])
        for i in range(len(self.weights)):
            self.index.append(i)
        
    def sort_by_utility(self):
        utility = []
        for i in range(len(self.weights)):
            utility.append((self.index[i],int(self.prices[i])/int(self.weights[i])))
        
        utility.sort(key=lambda pair:pair[1], reverse=True)
        
        self.weights = [self.weights[elem[0]] for elem in utility]
        self.prices = [self.prices[elem[0]] for elem in utility]
        self.index = [self.index[elem[0]] for elem in utility]
        
'''
weights_and_prices = [[32,2],[49,5],[33,4],[60,6]]
capacity = 130
kp = Knapsack(capacity,weights_and_prices)
kp.sort_by_utility()
'''