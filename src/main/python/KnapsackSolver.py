class KnapsackSolver:
    def __init__(self, knapsack):
        self.knapsack = knapsack
        self.lower_bound = -1
        self.n = len(knapsack.weights)
        self.taken = [0]*self.n

    def BB_solver1(self, j, p, w):  # the MTU1 recursive algorithm
        improved = False
        if w > self.knapsack.capacity:
            return improved
        if p > self.lower_bound:
            self.lower_bound = p
            improved = True
        else:
            improved = False
        if j >= self.n or (self.knapsack.capacity - w) < min(self.knapsack.weights[j:]) or self.eval(p, w, j) < (
            self.lower_bound + 1):
            return improved
        remaining_n = (self.knapsack.capacity - w) // self.knapsack.weights[j]
        for a in range(remaining_n, -1, -1):
            if self.BB_solver1(j + 1, p + a * self.knapsack.prices[j], w + a * self.knapsack.weights[j]):
                self.taken[j] = a
                improved = True
        return improved

    def eval(self, p, w, j):
        return p + int(((self.knapsack.capacity - w) / self.knapsack.weights[j]) * self.knapsack.prices[j])

    def BB_solver2(self):  # the MTU1 iteratif algorithm
        noeud0 = [0, 0, self.knapsack.capacity, 0]
        stack = []
        sol = [0]*self.n
        bound = 0
        stack.append(noeud0)
        while stack:
             noeud = stack.pop()
             print (" le noeud ", noeud )
             if noeud[0] != 0:
                 sol[noeud[0]-1] = noeud[1]

             if noeud[0] +1 <= self.n :
                 if noeud[0] != 0:
                    bound = noeud[3] +int((noeud[2] / self.knapsack.weights[noeud[0]] ) * self.knapsack.prices[noeud[0]])
                    print("bound ", bound)
             else:

                 if noeud[3] > self.lower_bound:
                     print("voici sol", sol)
                     self.taken = list(sol)
                     self.lower_bound = max( self.lower_bound, noeud[3])


             if ( noeud[0]+1 <= self.n ) and (bound > self.lower_bound ) :
                 print("je suis")
                 item = noeud[2] // self.knapsack.weights[noeud[0]]
                 a=0
                 while a<= item :
                     noe=[noeud[0]+1, a, noeud[2]-a*self.knapsack.weights[noeud[0]], noeud[3]+a*self.knapsack.prices[noeud[0]]]
                     stack.append(noe)
                     a +=1
             else:
                  if (bound < self.lower_bound):
                      sol[noeud[0]] = 0

    def BB_solver3(self):  # the MTU1 iteratif algorithm with best first
        noeud0 = [0, 0, self.knapsack.capacity, 0,0]
        stack = []
        sol = [0] * self.n
        stack.append(noeud0)
        while stack:
            noeud = stack.pop()
            print("noeud pop ",noeud)
            if noeud[0] != 0:
                sol[noeud[0] - 1] = noeud[1]
            if noeud[4] > self.lower_bound and noeud[0] +1 > self.n :
                    print("voici sol", sol)
                    self.taken = list(sol)
                    self.lower_bound = max(self.lower_bound, noeud[3])
                    print("lower bound",self.lower_bound)

            if (noeud[0] + 1 <= self.n) and (noeud[4] > self.lower_bound):
                item = noeud[2] // self.knapsack.weights[noeud[0]]
                a = 0
                children = []
                while a <= item:

                    noe = [noeud[0] + 1, a, noeud[2] - a * self.knapsack.weights[noeud[0]],
                           noeud[3] + a * self.knapsack.prices[noeud[0]],0]
                    if noe[0] + 1 <= self.n:
                            noe[4] = noe[3] + int((noe[2] / self.knapsack.weights[noe[0]]) * self.knapsack.prices[noe[0]])
                            print("bound noeud :", noe[0]," ",noe[4])
                    else :
                        noe[4]=noe[3]
                        print("bound noeud terminé:", noe[3])
                    children.append(noe)
                    a += 1
                children.sort(key= lambda ne : ne[4], reverse=True)
                while children :
                     stack.append(children.pop())

                print("stack",stack)
            else:
                if (noeud[4] < self.lower_bound):
                    sol[noeud[0]] = 0

    def density_ordered_ugreedy(self):
        remaining_capacity = self.knapsack.capacity
        for i in range(0, len(self.knapsack.weights)):
            self.taken[i] = int(remaining_capacity / self.knapsack.weights[i])
            remaining_capacity = remaining_capacity - self.taken[i] * self.knapsack.weights[i]
