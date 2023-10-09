import matplotlib.pyplot as plt

class Visualizer:
    """create graph, can save and show"""
    def __init__(self, data:list[float]):
        if not (isinstance(data, list)):
            raise TypeError('data should have type "list"')
        self.__data = data
        _, self.__plot = plt.subplots()

    def plot(self):
        """create graph"""
        length = len(self.__data)
        # create every line with cpecial color
        for i in range(0, length):
            # if this is last line
            if i + 1 == length:
                self.__plot.plot([i, i + 1], [self.__data[i], self.__data[i]],color = 'green')
                return
            self.__plot.plot([i,i+1],[self.__data[i],self.__data[i+1]],color = 'red' if self.__data[i] > self.__data[i + 1] else 'green')

    def save_picture(self, name:str):
        """save png picure with name"""
        if not (isinstance(name, str)):
            raise TypeError('name should have type "str"')
        plt.savefig(name)