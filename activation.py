import math


class Activation:
    @staticmethod
    def sigmoid(x):
        return (1 / (1 + math.exp(-x)))
    
    @staticmethod
    def relu(x):
        if (x > 0):
            return x
        else:
            return 0

    @staticmethod
    def tanh(x):
        return math.tanh(x)
    
    @staticmethod
    def softmax(array):
        _sum = 0
        res = []
        for i in range(len(array)):
            _sum += math.exp(array[i])

        for i in range(len(array)):
            res.append(math.exp(array[i]) / _sum)
        
        return res



