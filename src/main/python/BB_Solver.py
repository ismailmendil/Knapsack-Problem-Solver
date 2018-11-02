class BB_Solver:

    def __init__(self,capacity,weights,values):
        self.capacity = capacity
        self.weights = weights
        self.values = values
        self.nb_items = len(self.weights)
        self.current_index = 0
        self.sum_weight = 0
        self.sum_profit = 0
    
    def BB_KP_Solver(self):
        while self.capacity >= self.sum_weight:
            self.sum_weight += self.weights[self.current_index]
            self.sum_profit += self.sum_profit[self.current_index]
            self.current_index += 1
