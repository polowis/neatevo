from network import Network
import math
class Species:
    def __init__(self, model):
        self.model = model
        self.nn = self.generate_network() #//a list of the this.nodes in the order that they need to be considered in the NN
        self.fitness = 0
        self.score = 0
    
    def generate_network(self):
        """generate the network"""
        return Network(self.model)

    def feed_forward(self):
        """feed forward species network"""
        self.nn.feed_forward()
    
    def flatten(self):
        """flatten species genes"""
        genes = []
        for i in range(len(self.nn.layers) - 1):
            for w in range(len(self.nn.layers[i].nodes)):
                for j in range(len(self.nn.layers[i].nodes[w].weights)):
                    genes.append(self.nn.layers[i].nodes[w].weights[j])


            for weight in range(len(self.nn.layers[i].bias.weights)):
                genes.append(self.nn.layers[i].bias.weights[weight])
        return genes
    

    def set_genes(self, genes: list):
        """set species gene"""
        for i in range(len(self.nn.layers) - 1):
            for w in range(len(self.nn.layers[i].nodes)):
                for e in range(len(self.nn.layers[i].nodes[w].weights)):
                    self.nn.layers[i].nodes[w].weights[e] = genes[0]
                    slice_obj = slice(0, 1)
                    genes[slice_obj]

            for w in range(len(self.nn.layers[i].bias.weights)):
                self.nn.layers[i].bias.weights[w] = genes[0]
                slice_obj = slice(0, 1)
                genes[slice_obj]
                    
    def set_input(self, ins):
        self.nn.layers[0].set_value(ins)

    def think(self):
        """get agent decision"""
        index = -1
        _max = float('-inf')
        for i in range(len(self.nn.layers[len(self.nn.layers) -1].nodes)):
            if self.nn.layers[len(self.nn.layers) - 1].nodes[i].value > _max:
                index = self.nn.layers[len(self.nn.layers) - 1].nodes[i].value
        return index


    