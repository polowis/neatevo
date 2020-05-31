import random
class Node:
    """Node in neural network"""
    def __init__(self):
        self.value = 0
        self.weights = []

    def init_weights(self, count):
        """initialize weights"""
        for i in range(count):
            self.weights.append((random.random() * 2) - 1)
    
    