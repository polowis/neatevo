from node import Node
from activation import Activation

class Layer:
    def __init__(self, node_count, _type):
        """Layer in nn"""
        self.nodes = []
        self.bias = None
        self.input = 0
        self.output = 0
        self.type = _type
        #self.activation = activation
            
        # init nodes
        for i in range(node_count):
            self.nodes.append(Node())
        
        # init bias node
        if self.type != 'output':
            self.bias = Node()
    
    #------------
    # 
    #
    #
    #------------
    def connect(self, count):
        """connect layers to layers"""
        for i in range(len(self.nodes)):
            self.nodes[i].init_weights(count)

        if self.bias != None:
            self.bias.init_weights(count)
    
    #------------
    # 
    #
    #
    #------------
    def feed_forward(self, layer):
        """Feeds forward the layers values"""
        for i in range(len(self.bias.weights)):
            layer.nodes[i].value = 0
        
        for i in range(len(self.nodes)):
            for weight in range(len(self.nodes[i].weights)):
                layer.nodes[weight].value += self.nodes[i].value * self.nodes[i].weights[weight]
        
        for weight in range(len(self.bias.weights)):
            layer.nodes[weight].value += self.bias.weights[weight]
        
        for w in range(len(layer.nodes)):
            # use tanh as our activation function
            layer.nodes[w].value = Activation.tanh(layer.nodes[w].value)
        
        
    #------------
    # 
    #
    #
    #------------
    def set_value(self, ins):
        """set value of node"""
        for i in range(len(self.nodes)):
            self.nodes[i].value = ins[i]

    def get_values(self):
        """return value of nodes in array"""
        res = []
        for i in range(len(self.nodes)):
            res.append(self.nodes[i].value)
        return res