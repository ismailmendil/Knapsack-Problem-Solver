class BenchmarkReader:
    def __init__(self,file_path):
        with open(file_path,mode='r') as benchmark_file:
            self.lines = benchmark_file.read().split('\n')
            self.capacity = self.fetch_constraint(self.lines)
            #print(self.capacity)
            self.problem_values = self.fetch_data(self.lines)
            #print(self.problem_values)
            self.Solution = self.fetch_solution(self.lines)
            #print(self.Solution)
    def fetch_constraint(self,lines):
        for line in lines:
            part = line.split(' ')
            if part[0] == 'c:':
                return int(part[1])
            
    def fetch_data(self,lines):
        index_begin_data = lines.index("begin data ")
        problem_values = []
        for line in lines[index_begin_data+1:]:
            if line != "end data ":
                vector = line.split('\t')
                problem_values.append([int(vector[0]),int(vector[1])])
            else:
                return problem_values
    
    def fetch_solution(self,lines):
        solution_line = lines.index("sol: ")
        tab_solution = []
        Solution = {'index':[],'nb':[],'weight':[],'price':[]}
        for line in lines[solution_line+1:]:
            if (line != ""):
                tab_solution.append(line.split("\t"))
            else:
                break
        for elem in tab_solution:
            
            Solution['index'].append(int(elem[1]))
            Solution['nb'].append(int(elem[2]))
            Solution['weight'].append(int(elem[3]))
            Solution['price'].append(int(elem[4])) 
        return Solution
            
            


#b = BenchmarkReader("/home/ali/Desktop/TP_OPTM/assets/upk/1.ukp")