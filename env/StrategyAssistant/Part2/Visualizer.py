import matplotlib.pyplot as plt
import pandas

class Visualizer:
    def __init__(self, data):
        self.__data = data
        _, self.__plot = plt.subplots()

    def plot(self):
        length = len(self.__data)
        for i in range(0, length):
            if i + 1 == length:
                self.__plot.plot([i, i + 1], [self.__data[i], self.__data[i]],color = 'green')
                return
            self.__plot.plot([i,i+1],[self.__data[i],self.__data[i+1]],color = 'red' if self.__data[i] > self.__data[i + 1] else 'green')
    def save_picture(self, name):
        plt.savefig(name)