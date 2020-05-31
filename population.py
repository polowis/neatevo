from species import Species
import random, math

class Population:
    def __init__(self, config, population=500, mutation_rate=0.5):
        self.inputs = 0
        self.output = 0
        self.model = config
        self.agents = []
        self.population = population
        self.mutation_rate = mutation_rate
        self.generation = 0
        self.outdated_agents = [] # history agents

        for i in range(population):
            self.agents.append(Species(self.model))
        
    #----------------------------------------------------------------
    #
    # 
    # 
    #----------------------------------------------------------------
    def mutate(self):
        """mutate weight by adding random value"""
        for i in range(self.population):
            genes = self.agents[i].flatten()
            genes = self.__mutate(genes, self.mutation_rate)
            self.agents[i].set_genes(genes)

    #----------------------------------------------------------------
    #
    # 
    # 
    #----------------------------------------------------------------
    def crossover(self):
        """reproduce child from parent gene"""
        for i in range(self.population):
            self.outdated_agents = self.agents.copy()
            parentX = self.pick()
            parentY = self.pick()

            genes = self.__crossover(parentX.flatten(), parentY.flatten())

    #----------------------------------------------------------------
    #
    # 
    # 
    #----------------------------------------------------------------
    def perform_natural_selection(self):
        """do generation"""
        self.crossover()
        self.mutate()
        self.generation = self.generation + 1
        print("Generation: %d" % self.generation)

    #----------------------------------------------------------------
    #
    # 
    # 
    #----------------------------------------------------------------
    def think(self):
        """return the output of nn"""
        res = []
        for i in range(len(self.agents)):
            res.append(self.agents[i].think())
        return res

    #----------------------------------------------------------------
    #
    # 
    # 
    #----------------------------------------------------------------    
    def bestAgent(self):
        """return index of best agents from last generation"""
        index = 0
        _max = float('-inf')
        for i in range(len(self.outdated_agents)):
            if self.outdated_agents[i].fitness > _max:
                _max = self.outdated_agents[i].fitness
                index = i
        return index

    #----------------------------------------------------------------
    #
    # 
    # 
    #----------------------------------------------------------------
    def observe(self, array, index):
        """get inputs and feed into nn"""
        self.agents[index].set_input(array)

    #----------------------------------------------------------------
    #
    # 
    # 
    #----------------------------------------------------------------    
    def feed_forward(self):
        """feed forward every species in the network"""
        for i in range(len(self.agents)):
            self.agents[i].feed_forward()
    
    #----------------------------------------------------------------
    #
    # 
    # 
    #----------------------------------------------------------------

    def pick(self):
        """normalize agents fitness"""
        total = 0
        for i in range(len(self.outdated_agents)):
            total += math.pow(self.outdated_agents[i].score, 2)

        for i in range(len(self.outdated_agents)):
            self.outdated_agents[i].fitness = math.pow(self.outdated_agents[i].score, 2) / total
        
        index = 0
        r = random.random()

        while r > 0:
            r =  r - self.outdated_agents[index].fitness
            index = index + 1
        index -= 1

        return self.outdated_agents[index]
        
    #----------------------------------------------------------------
    #
    # 
    # 
    #----------------------------------------------------------------
    def set_fitness(self, fitness, index):
        """set fitness for an agent at given index"""
        self.agents[index].score = fitness

    def __crossover(self, geneX, geneY):
        """random crossover \n
        randomly takes genes from parents
        """
        genes = []
        for i in range(len(geneX)):
            if random.random() < 0.5:
                genes.append(geneX[i])
            else:
                genes.append(geneY[i])
        return genes
    

    def __mutate(self, genes, mutation_rate):
        """mutate weight by random value"""
        for i in range(len(genes)):
            if random.random() < mutation_rate:
                genes[i] = (random.random() * 2) - 1
        return genes

