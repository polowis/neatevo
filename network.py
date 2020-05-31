from layer import Layer

class Network:
    """Neural network"""

    def __init__(self, model: list):
        self.layers = [] # layers in neural network
        self.model = model
        for i in range(len(model)):
            self.layers.append(Layer(model[i].get("nodeCount"), model[i].get("type")))

        for i in range(len(model) - 1):
            self.layers[i].connect(len(self.layers[i + 1].nodes))
        
    def feed_forward(self):
        """Feed forward the network"""
        for i in range(len(self.model) - 1):
            self.layers[i].feed_forward(self.layers[i + 1])
        